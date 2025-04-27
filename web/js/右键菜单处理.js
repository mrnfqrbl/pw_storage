// 右键菜单处理.js - 负责右键菜单的显示、隐藏和功能处理

document.addEventListener('DOMContentLoaded', function() {
    const 右键菜单 = document.getElementById('右键菜单'); // 获取右键菜单元素
    const 编辑值按钮 = document.getElementById('编辑值');
    const 复制条目按钮 = document.getElementById('复制条目');
    const 删除条目按钮 = document.getElementById('删除条目');

    // 检查是否成功获取了元素
    if (!右键菜单 || !编辑值按钮 || !复制条目按钮 || !删除条目按钮) {
        console.error('未能找到必要的 DOM 元素！');
        return; // 如果元素未找到，则停止执行
    }

    const 右键菜单处理 = {
        当前目标元素: null, // 保存当前右键点击的目标元素
        长按定时器: null, // 长按定时器

        初始化: function() {
            // 绑定右键菜单项事件
            编辑值按钮.addEventListener('click', this.编辑值.bind(this));
            复制条目按钮.addEventListener('click', this.复制条目.bind(this));
            删除条目按钮.addEventListener('click', this.删除条目.bind(this));

            // 点击页面其他区域隐藏右键菜单
            document.addEventListener('click', this.隐藏菜单.bind(this));

            // 移动端触摸事件
            document.addEventListener('touchstart', this.开始触摸.bind(this));
            document.addEventListener('touchend', this.结束触摸.bind(this));
            document.addEventListener('touchmove', this.移动触摸.bind(this));

            // 绑定 contextmenu 事件，用于显示自定义右键菜单
            document.addEventListener('contextmenu', this.显示菜单.bind(this));

            console.log('右键菜单处理初始化完成！');
        },

        开始触摸: function(事件) {
            // 检查是否是需要触发右键菜单的元素
            let 目标元素 = 事件.target;

            // 向上查找，直到找到 class 为 "条目-标题" 或 "条目-内容" 的元素
            while (目标元素 && !目标元素.classList.contains('条目-标题') && !目标元素.classList.contains('条目-内容') && !目标元素.tagName === 'P') {
                目标元素 = 目标元素.parentNode;
            }

            if (目标元素) {
                this.长按定时器 = setTimeout(() => {
                    this.显示菜单(事件, 目标元素);
                }, 750); // 长按 750 毫秒
            }
        },

        结束触摸: function(事件) {
            clearTimeout(this.长按定时器); // 清除定时器
        },

        移动触摸: function(事件) {
            clearTimeout(this.长按定时器); // 清除定时器
        },

        显示菜单: function(事件, 触摸目标元素 = null) {
            事件.preventDefault(); // 阻止默认的右键菜单

            let 目标元素 = 触摸目标元素 || 事件.target; // 如果是触摸事件，使用触摸目标元素

            console.log('触发显示菜单事件，目标元素：', 目标元素);

            // 向上查找，直到找到 class 为 "条目-标题" 或 "条目-内容" 的元素 或 P 元素
            while (目标元素 && !目标元素.classList.contains('条目-标题') && !目标元素.classList.contains('条目-内容') && 目标元素.tagName !== 'P') {
                目标元素 = 目标元素.parentNode;
            }

            // 检查是否是需要触发右键菜单的元素
            if (目标元素 && (目标元素.classList.contains('条目-标题') || 目标元素.classList.contains('条目-内容') || 目标元素.tagName === 'P')) {
                this.当前目标元素 = 目标元素; // 保存当前目标元素

                // 获取触摸位置
                let 客户端X, 客户端Y;
                if (事件.touches && 事件.touches.length > 0) {
                    客户端X = 事件.touches[0].clientX;
                    客户端Y = 事件.touches[0].clientY;
                } else {
                    客户端X = 事件.clientX;
                    客户端Y = 事件.clientY;
                }

                右键菜单.style.top = 客户端Y + 'px';
                右键菜单.style.left = 客户端X + 'px';
                右键菜单.style.display = 'block';

                console.log('显示右键菜单，位置：', 客户端X, 客户端Y);
            } else {
                console.warn('目标元素不是 class 为 "条目-标题" 或 "条目-内容" 的元素，不显示右键菜单！');
            }
        },

        隐藏菜单: function() {
            右键菜单.style.display = 'none';
            this.当前目标元素 = null; // 清空当前目标元素
        },

        编辑值: function() {
            if (this.当前目标元素) {
                let 当前值;
                let 键名; // 用于存储键名
                if (this.当前目标元素.tagName === 'P') {
                    const 文本内容 = this.当前目标元素.textContent;
                    const 分割结果 = 文本内容.split(': ');
                    键名 = 分割结果[0]; // 获取 <p> 标签中的键名
                    当前值 = 分割结果[1]; // 获取 <p> 标签中的值
                } else {
                    当前值 = this.当前目标元素.textContent;
                    键名 = '标题'; // 如果是标题，则键名为 '标题'
                }

                const 新值 = prompt('请输入新的值:', 当前值);

                if (新值 !== null) {
                    // 获取 UUID
                    let uuid;
                    if (this.当前目标元素.tagName === 'P') {
                        let 条目内容元素 = this.当前目标元素.parentNode; // 获取父元素 <div class="条目-内容">
                        let 条目元素 = 条目内容元素.parentNode; // 获取父元素 <div class="条目">
                        uuid = 条目元素.dataset.uuid; // 获取 data-uuid
                    } else {
                        let 条目元素 = this.当前目标元素.parentNode; // 获取父元素 <div class="条目">
                        uuid = 条目元素.dataset.uuid; // 获取 data-uuid
                    }

                    // 构建数据
                    const 更新数据 = {
                        [uuid]: {
                            [键名]: 新值
                        }
                    };

                    console.log('要更新的数据:', 更新数据); // 输出到控制台，方便查看

                    // 在这里，你可以将 更新数据 发送到服务器或其他地方进行处理
                    // 暂时什么也不做，只存储在变量中
                    当前合集名称=window.当前合集名称
                    更新结果=api.修改条目(合集名称=当前合集名称,修改内容=更新数据)

                    // 更新界面显示
                    if (this.当前目标元素.tagName === 'P') {
                        this.当前目标元素.textContent = 键名 + ': ' + 新值; // 更新 <p> 标签中的值
                    } else {
                        this.当前目标元素.textContent = 新值; // 更新标题
                    }
                }
            }
            this.隐藏菜单();
        },

        复制条目: function() {
            if (this.当前目标元素) {
                let 条目值;
                if (this.当前目标元素.tagName === 'P') {
                    条目值 = this.当前目标元素.textContent.split(': ')[1]; // 获取 <p> 标签中的值
                } else {
                    条目值 = this.当前目标元素.textContent;
                }
                navigator.clipboard.writeText(条目值)
                    .then(() => {
                        显示水印提示('条目已复制到剪贴板！'); // 使用水印提示
                    })
                    .catch(err => {
                        console.error('复制失败: ', err);
                        显示水印提示('复制失败，请检查浏览器设置或使用HTTPS。'); // 使用水印提示
                    });
            }
            this.隐藏菜单();
        },

        删除条目: function() {
            if (this.当前目标元素) {
                if (this.当前目标元素.tagName === 'P') {
                    this.当前目标元素.remove(); // 删除 <p> 元素
                } else {
                    this.当前目标元素.remove(); // 删除 "条目-标题" 或 "条目-内容" 元素
                }
            }
            this.隐藏菜单();
        }
    };

    // 导出初始化函数 (如果需要)
    window.右键菜单处理 = 右键菜单处理; // 为了方便其他模块调用
    右键菜单处理.初始化();
});
