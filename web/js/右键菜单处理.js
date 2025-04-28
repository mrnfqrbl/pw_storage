// 右键菜单处理.js - 负责右键菜单的显示、隐藏和功能处理

document.addEventListener('DOMContentLoaded', function() {
    const 右键菜单 = document.getElementById('右键菜单'); // 获取右键菜单元素
    const 编辑值按钮 = document.getElementById('编辑值');
    const 复制条目按钮 = document.getElementById('复制');
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

                // 根据目标元素类型显示/隐藏删除按钮
                if (目标元素.classList.contains('条目-内容') || 目标元素.parentNode.classList.contains('条目-内容')) {
                    删除条目按钮.style.display = 'none'; // 隐藏删除按钮
                } else {
                    删除条目按钮.style.display = 'block'; // 显示删除按钮
                }
                if (目标元素.classList.contains('条目-标题')) {
                    编辑值按钮.style.display = 'none'; // 隐藏编辑按钮
                } else {
                    编辑值按钮.style.display = 'block'; // 显示编辑按钮
                }
                console.log('显示右键菜单，位置：', 客户端X, 客户端Y);
            } else {
                console.warn('目标元素不是 class 为 "条目-标题" 或 "条目-内容" 的元素，不显示右键菜单！');
            }
        },

        隐藏菜单: function() {
            右键菜单.style.display = 'none';
            this.当前目标元素 = null; // 清空当前目标元素
        },

        编辑值: async function() {
            if (this.当前目标元素) {
                let 当前值;
                let 键名; // 用于存储键名

                // 判断当前目标元素是否为 <p> 标签
                if (this.当前目标元素.tagName === 'P') {
                    // 获取 <p> 标签中的 <strong> 标签
                    const strong元素 = this.当前目标元素.querySelector('strong');

                    // 检查是否存在 <strong> 标签
                    if (strong元素) {
                        键名 = strong元素.textContent.slice(0, -1); // 获取 <strong> 标签的文本内容作为键名 (去掉冒号)
                    } else {
                        键名 = '未知键名'; // 如果没有 <strong> 标签，则使用默认键名
                    }

                    当前值 = this.当前目标元素.textContent.split(': ')[1]; // 获取 <p> 标签中的值
                } else {
                    // 如果当前目标元素不是 <p> 标签，则认为是标题
                    当前值 = this.当前目标元素.textContent;
                    键名 = '名称'; // 如果是标题，则键名为 '名称'
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
                    const 更新结果= await window.app.api.后端交互("修改条目",[{"合集名称":window.当前合集名称},{"修改内容": 更新数据}])
                    console.log('更新结果:', 更新结果);
                    const 最新内容 = await window.app.api.后端交互("查询条目",[{"合集名称":window.当前合集名称},{"查询条件": {"uuid":uuid}}]);
                    console.log('最新内容:', 最新内容);
                    console.log('键名:', 键名);
                    最新值=最新内容[0]["文档内容"][键名];
                    console.log('最新值:', 最新值);
                    if (最新值 == 新值) {
                        window.app.水印提示("更新成功");
                    } else {
                        window.app.水印提示("更新失败");
                    }
                    await window.app.条目填充.软更新()


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
                        window.app.水印提示('条目已复制到剪贴板！'); // 使用水印提示
                    })
                    .catch(err => {
                        console.error('复制失败: ', err);
                        window.app.水印提示('复制失败，请检查浏览器设置或使用HTTPS。'); // 使用水印提示
                    });
            }
            this.隐藏菜单();
        },

        删除条目: async function() {
            if (this.当前目标元素) {
                // 获取 UUID
                let 条目元素;
                if (this.当前目标元素.tagName === 'P') {
                    let 条目内容元素 = this.当前目标元素.parentNode; // 获取父元素 <div class="条目-内容">
                    条目元素 = 条目内容元素.parentNode; // 获取父元素 <div class="条目">
                } else {
                    条目元素 = this.当前目标元素.parentNode; // 获取父元素 <div class="条目">
                }
                const 条目uuid = 条目元素.dataset.uuid; // 获取 data-uuid

                // 构建删除数据
                const 删除数据 = [{
                    合集名称: window.app.当前合集名称
                }, {
                    uuid: 条目uuid
                }];

                console.log('要删除的数据:', 删除数据); // 输出到控制台，方便查看

                // 调用后端交互
                window.app.api.后端交互("删除条目", 删除数据)

                    .then(result => {
                    });

                // 从 DOM 中移除条目
                await window.app.条目填充.软更新()

            }
            this.隐藏菜单();
        }
    };

    // 导出初始化函数 (如果需要)
    window.app.右键菜单处理 = 右键菜单处理; // 为了方便其他模块调用
    // 右键菜单处理.初始化();
});
