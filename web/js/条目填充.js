// 条目填充.js - 负责“元素总容器”下条目的填充

document.addEventListener('DOMContentLoaded', function() {
    const 元总容器 = document.getElementById('一级-元总-顶级-body'); // 获取元素总容器
    const 合集选择框 = document.getElementById('合集选择框'); // 获取合集选择框

    // 检查是否成功获取了元素
    if (!元总容器 || !合集选择框) {
        console.error('未能找到必要的 DOM 元素！');
        return; // 如果元素未找到，则停止执行
    }

    function 创建条目(数据) {
        const 条目元素 = document.createElement('div');
        条目元素.classList.add('条目'); // 添加条目样式类

        // 创建标题元素
        const 标题元素 = document.createElement('div');
        标题元素.classList.add('条目-标题'); // 添加标题样式类
        标题元素.textContent = 数据.文档内容.名称; // 设置标题文本

        // 创建内容元素
        const 内容元素 = document.createElement('div');
        内容元素.classList.add('条目-内容'); // 添加内容样式类
        内容元素.style.display = 'none'; // 默认隐藏内容

        // 构建内容
        内容元素.innerHTML = `
        <p><strong>名称:</strong> ${数据.文档内容.名称 || '无'}</p>
        <p><strong>应用:</strong> ${数据.文档内容.应用 || '无'}</p>
        <p><strong>账号:</strong> ${数据.文档内容.账号 || '无'}</p>
        <p><strong>密码:</strong> ${数据.文档内容.密码 || '无'}</p>
        <p><strong>邮箱:</strong> ${数据.文档内容.邮箱 || '无'}</p>
        <p><strong>邮箱密码:</strong> ${数据.文档内容.邮箱密码 || '无'}</p>
        <p><strong>网站:</strong> ${数据.文档内容.网站 || '无'}</p>
        <p><strong>备注:</strong> ${数据.文档内容.备注 || '无'}</p>
    `;

        // 添加点击事件，切换内容显示状态
        标题元素.addEventListener('click', function() {
            内容元素.style.display = 内容元素.style.display === 'none' ? 'block' : 'none';
        });

        // 将标题和内容添加到条目元素
        条目元素.appendChild(标题元素);
        条目元素.appendChild(内容元素);

        // 将外层属性存储到 dataset 中
        条目元素.dataset.id = 数据.id; // 存储条目ID
        条目元素.dataset.uuid = 数据.uuid; // 存储条目UUID
        条目元素.dataset.序号 = 数据.序号; // 存储条目序号

        return 条目元素;
    }

    function 更新条目(条目元素, 数据) {
        // 更新条目内容
        条目元素.querySelector('.条目-标题').textContent = 数据.文档内容.名称;
        条目元素.querySelector('.条目-内容').innerHTML = `
            <p><strong>名称:</strong> ${数据.文档内容.名称 || '无'}</p>
            <p><strong>应用:</strong> ${数据.文档内容.应用 || '无'}</p>
            <p><strong>账号:</strong> ${数据.文档内容.账号 || '无'}</p>
            <p><strong>密码:</strong> ${数据.文档内容.密码 || '无'}</p>
            <p><strong>邮箱:</strong> ${数据.文档内容.邮箱 || '无'}</p>
            <p><strong>邮箱密码:</strong> ${数据.文档内容.邮箱密码 || '无'}</p>
            <p><strong>网站:</strong> ${数据.文档内容.网站 || '无'}</p>
            <p><strong>备注:</strong> ${数据.文档内容.备注 || '无'}</p>
        `;

        // 更新 dataset (如果需要)
        条目元素.dataset.id = 数据.id;
        条目元素.dataset.uuid = 数据.uuid;
        条目元素.dataset.序号 = 数据.序号;
    }


    function 填充条目(合集数据,是否更新当前合集内容列表) {
        是否更新当前合集内容列表 = (typeof 是否更新当前合集内容列表 === 'undefined' || 是否更新当前合集内容列表 === true);

        // 确保条目数据是一个对象，并且包含 "合集内容" 属性
        if (合集数据 && Array.isArray(合集数据)) {
            const 新条目数据 = 合集数据;
            const 现有条目元素 = Array.from(元总容器.children);
            const 旧条目数据 = window.app.当前合集内容列表 || []; // 获取旧的条目数据，如果不存在则使用空数组

            // 1. 更新或创建条目
            新条目数据.forEach(数据 => {
                const 条目元素 = 现有条目元素.find(元素 => 元素.dataset.uuid === 数据.uuid); // 使用 uuid 作为唯一标识符
                const 旧数据 = 旧条目数据.find(item => item.uuid === 数据.uuid); // 查找旧数据中是否存在该条目

                if (条目元素) {
                    // 如果条目存在，并且数据发生了变化，则更新条目
                    if (!深比较(数据, 旧数据)) { // 使用深比较函数判断数据是否发生变化
                        更新条目(条目元素, 数据);
                        console.log('更新条目:', 数据);
                    } else {
                        console.log('条目数据未发生变化，无需更新:', 数据);
                    }
                } else {
                    // 如果条目不存在，则创建新条目
                    const 新条目 = 创建条目(数据);
                    元总容器.appendChild(新条目);
                    console.log('创建条目:', 数据);
                }
            });

            // 2. 删除不存在的条目
            现有条目元素.forEach(元素 => {
                const 条目数据存在 = 新条目数据.find(数据 => 数据.uuid === 元素.dataset.uuid);
                if (!条目数据存在) {
                    元总容器.removeChild(元素);
                    console.log('删除条目:', 元素.dataset.uuid);
                }
            });

            // 在条目填充完成后，更新全局属性
            if (是否更新当前合集内容列表) {
                window.app.当前合集内容列表 = 新条目数据;
            }else {
                console.log('当前合集内容列表未更新,因为是否更新当前合集内容列表为:', 是否更新当前合集内容列表);
            }

        } else {
            console.error('条目数据格式不正确！', 条目数据);
        }
    }

    // 深比较函数，用于判断两个对象是否相等
    function 深比较(obj1, obj2) {
        if (typeof obj1 !== 'object' || obj1 === null || typeof obj2 !== 'object' || obj2 === null) {
            return obj1 === obj2;
        }

        const keys1 = Object.keys(obj1);
        const keys2 = Object.keys(obj2);

        if (keys1.length !== keys2.length) {
            return false;
        }

        for (let key of keys1) {
            if (!obj2.hasOwnProperty(key) || !深比较(obj1[key], obj2[key])) {
                return false;
            }
        }

        return true;
    }

    function 填充合集选择框(合集列表) {
        // 清空合集选择框
        合集选择框.innerHTML = '';

        合集列表.forEach(合集名称 => {
            const 选项 = document.createElement('option');
            选项.value = 合集名称;
            选项.textContent = 合集名称;
            合集选择框.appendChild(选项);
        });
    }

    // 防抖函数
    function 防抖(func, 延迟) {
        let 定时器;
        return function(...参数) {
            clearTimeout(定时器);
            定时器 = setTimeout(() => {
                func.apply(this, 参数);
            }, 延迟);
        };
    }

    const 条目填充 = {
        初始化: async function() {
            // 获取合集列表
            const 响应数据 = await api.后端交互("获取合集列表"); // 使用 api.js 中的函数
            const 合集列表 = 响应数据.合集列表 || []; // 从字典中提取合集列表，如果不存在则使用空数组

            // 检查合集列表的值和类型
            console.log('合集列表:', 合集列表);
            console.log('合集列表的类型:', typeof 合集列表);

            // 填充合集选择框
            填充合集选择框(合集列表);

            // 监听合集选择框的 change 事件
            合集选择框.addEventListener('change', 防抖(async function() {
                const 当前合集名称 = 合集选择框.value;
                window.app.当前合集名称=  当前合集名称;
                const 条目数据 = await window.app.api.后端交互("获取合集内容",[{"合集名称":当前合集名称}]);
                const 合集数据 = 条目数据.合集内容;
                填充条目(合集数据);

            }, 300)); // 300 毫秒的防抖延迟

            // 首次加载时，默认显示第一个合集的内容
            console.log('合集列表长度:', 合集列表.length);
            if (合集列表.length > 0) {
                const 默认合集名称 = 合集列表[0];
                合集选择框.value = 默认合集名称;
                const 当前合集名称 = 合集选择框.value;
                window.app.当前合集名称=  当前合集名称;
                const 条目数据  = await window.app.api.后端交互("获取合集内容",[{"合集名称":当前合集名称}]);

                const 合集数据 = 条目数据.合集内容;
                填充条目(合集数据);
                console.log('默认合集名称:', 默认合集名称);
            }
        },
        软更新: async function(合集数据,是否更新当前合集内容列表) {
            if (!合集数据) {
                const 当前合集名称 = 合集选择框.value;
                window.app.当前合集名称 = 当前合集名称;
                const 条目数据 = await window.app.api.后端交互("获取合集内容", [{"合集名称": 当前合集名称}]);
                console.error('调用传递合集数据为空，可能为搜索函数问题,使用获取数据！');
                return;
            }

            填充条目(合集数据,是否更新当前合集内容列表);
            console.log('软更新完成');
        }
    };

    window.app.条目填充 = 条目填充; // 为了方便其他模块调用

});
