// 右键菜单处理类.js - 负责右键菜单的显示、隐藏和功能处理

class 右键菜单处理类 {
    constructor() {
        this.右键菜单 = document.getElementById('右键菜单'); // 获取右键菜单元素
        this.编辑值按钮 = document.getElementById('编辑值');
        this.复制条目按钮 = document.getElementById('复制');
        this.删除条目按钮 = document.getElementById('删除条目');
        this.当前目标元素 = null; // 保存当前右键点击的目标元素
        this.长按定时器 = null; // 长按定时器

        // 绑定事件
        this.绑定事件();

        console.log("初始化右键菜单");
    }

    绑定事件() {
        // 绑定右键菜单项事件
        this.编辑值按钮.addEventListener('click', this.编辑值.bind(this));
        this.复制条目按钮.addEventListener('click', this.复制条目.bind(this));
        this.删除条目按钮.addEventListener('click', this.删除条目.bind(this));

        // 点击页面其他区域隐藏右键菜单
        document.addEventListener('click', this.隐藏菜单.bind(this));

        // 移动端触摸事件
        document.addEventListener('touchstart', this.开始触摸.bind(this));
        document.addEventListener('touchend', this.结束触摸.bind(this));
        document.addEventListener('touchmove', this.移动触摸.bind(this));

        // 绑定 contextmenu 事件，用于显示自定义右键菜单
        document.addEventListener('contextmenu', this.显示菜单.bind(this));

        console.log('右键菜单处理初始化完成！');
    }

    // 触摸相关的事件
    开始触摸(事件) {
        let 目标元素 = 事件.target;

        while (目标元素 && !目标元素.classList.contains('单个内容项') && !目标元素.classList.contains('条目-标题')) {
            目标元素 = 目标元素.parentNode;
        }

        if (目标元素) {
            this.长按定时器 = setTimeout(() => {
                this.显示菜单(事件, 目标元素);
            }, 750); // 长按 750 毫秒
        }
    }

    结束触摸(事件) {
        clearTimeout(this.长按定时器);
    }

    移动触摸(事件) {
        clearTimeout(this.长按定时器);
    }

    // 显示菜单
    显示菜单(事件, 触摸目标元素 = null) {
        事件.preventDefault();

        let 目标元素 = 触摸目标元素 || 事件.target;
        console.log('触发显示菜单事件，目标元素：', 目标元素);

        // 向上查找直到找到 '条目-标题' 或 '单个内容项'
        while (目标元素 && !目标元素.classList.contains('单个内容项') && !目标元素.classList.contains('条目-标题')) {
            目标元素 = 目标元素.parentNode;
        }

        if (目标元素) {
            this.当前目标元素 = 目标元素; // 保存当前目标元素
            console.log('当前目标元素：', 目标元素);

            let 客户端X, 客户端Y;
            if (事件.touches && 事件.touches.length > 0) {
                客户端X = 事件.touches[0].clientX;
                客户端Y = 事件.touches[0].clientY;
            } else {
                客户端X = 事件.clientX;
                客户端Y = 事件.clientY;
            }

            // 显示右键菜单
            this.右键菜单.style.top = 客户端Y + 'px';
            this.右键菜单.style.left = 客户端X + 'px';
            this.右键菜单.style.display = 'block';

            // 根据触发元素决定显示的菜单项
            if (目标元素.classList.contains('条目-标题')) {
                this.编辑值按钮.style.display = 'none'; // 隐藏编辑按钮
                this.删除条目按钮.style.display = 'block'; // 显示删除按钮
            } else if (目标元素.classList.contains('单个内容项')) {
                this.编辑值按钮.style.display = 'block'; // 显示编辑按钮
                this.删除条目按钮.style.display = 'none'; // 隐藏删除按钮
            }

            console.log('显示右键菜单，位置：', 客户端X, 客户端Y);
        } else {
            console.warn('目标元素不是有效的右键菜单触发元素！');
        }
    }

    // 隐藏菜单
    隐藏菜单() {
        this.右键菜单.style.display = 'none';
        this.当前目标元素 = null;
    }

    // 编辑值
    async 编辑值() {
        if (this.当前目标元素) {
            let 当前值;
            let 键名;

            // 查找到对应的值容器
            let 值容器 = this.当前目标元素.querySelector('.值容器') || this.当前目标元素.parentNode.querySelector('.值容器');
            if (值容器) {
                当前值 = 值容器.textContent;
                键名 = 值容器.previousElementSibling.textContent; // 获取字段名称

                const 新值 = prompt('请输入新的值:', 当前值);

                if (新值 !== null) {
                    let uuid = this.当前目标元素.closest('.条目').dataset.uuid; // 获取条目的uuid

                    const 更新数据 = {
                        [uuid]: {
                            [键名]: 新值
                        }
                    };

                    console.log('要更新的数据:', 更新数据);
                    const 更新结果 = await window.app.api.后端交互("修改条目", [{"合集名称": window.app.当前合集名称}, {"修改内容": 更新数据}]);
                    console.log('更新结果:', 更新结果);

                    const 最新内容 = await window.app.api.后端交互("查询条目", [{"合集名称": window.app.当前合集名称}, {"查询条件": {"uuid": uuid}}]);
                    console.log('最新内容:', 最新内容);

                    const 最新值 = 最新内容[0]["文档内容"][键名];
                    console.log('最新值:', 最新值);

                    if (最新值 === 新值) {
                        window.app.水印提示("更新成功");
                    } else {
                        window.app.水印提示("更新失败");
                    }

                    await window.app.条目填充.软更新();
                }
            }
        }
        this.隐藏菜单();
    }

    // 复制条目
    async 复制条目() {
        if (this.当前目标元素) {
            let 值容器 = this.当前目标元素.querySelector('.值容器') || this.当前目标元素.parentNode.querySelector('.值容器');
            if (值容器) {
                const 条目值 = 值容器.textContent;
                navigator.clipboard.writeText(条目值)
                    .then(() => {
                        window.app.水印提示('条目已复制到剪贴板！');
                    })
                    .catch(err => {
                        console.error('复制失败: ', err);
                        window.app.水印提示('复制失败，请检查浏览器设置或使用HTTPS。');
                    });
            }
        }
        this.隐藏菜单();
    }

    // 删除条目
    async 删除条目() {
        if (this.当前目标元素) {
            const 条目元素 = this.当前目标元素.closest('.条目');
            const 条目uuid = 条目元素.dataset.uuid;
            const 删除数据 = [{
                合集名称: window.app.当前合集名称
            }, {
                uuid: 条目uuid
            }];

            console.log('要删除的数据:', 删除数据);

            await window.app.api.后端交互("删除条目", 删除数据);
            await window.app.条目填充.软更新();
            window.app.水印提示('条目已删除');
            this.隐藏菜单();
        }
    }
}
