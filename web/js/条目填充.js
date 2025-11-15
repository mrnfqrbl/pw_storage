// 文件路径：条目填充.js
// 模块职责：管理“元素总容器”中条目的填充、更新与合集选择，依赖后端数据。
// 中文版本：将页面中的条目模块封装为类，供其他模块（如 UI 控制或数据交互）调用。
// 示例调用：window.app.条目填充.初始化();

class 条目填充类 {
    constructor() {
        this.元总容器 = document.getElementById('一级-元总-顶级-body');
        this.合集选择框 = document.getElementById('合集选择框');

        if (!this.元总容器 || !this.合集选择框) {
            console.error('未能找到必要的 DOM 元素！');
            return;
        }
    }

    // 生成每个内容项
    生成内容项(字段, 值) {
        // 创建内容项容器
        const 内容项 = document.createElement('div');
        内容项.classList.add('单个内容项');

        // 创建字段容器
        const 字段容器 = document.createElement('div');
        字段容器.classList.add('字段容器');
        字段容器.textContent = 字段;  // 设置值，默认'无'

        // 创建值容器
        const 值容器 = document.createElement('div');
        值容器.classList.add('值容器');
        值容器.textContent = 值 || '无';  // 设置值，默认'无'

        // 将字段容器和值容器添加到内容项容器中
        内容项.appendChild(字段容器);
        内容项.appendChild(值容器);

        return 内容项;
    }

    // 创建条目元素
    创建条目(数据) {
        const 条目元素 = document.createElement('div');
        条目元素.classList.add('条目');

        const 标题元素 = document.createElement('div');
        标题元素.classList.add('条目-标题');
        标题元素.textContent = 数据.文档内容.名称;

        const 内容元素 = document.createElement('div');
        内容元素.classList.add('条目-内容');
        内容元素.style.display = 'none';

        // 动态生成内容项
        Object.entries(数据.文档内容).forEach(([字段, 值]) => {
            内容元素.appendChild( this.生成内容项(字段, 值));
        });

        标题元素.addEventListener('click', () => {
            内容元素.style.display = 内容元素.style.display === 'none' ? 'block' : 'none';
        });

        条目元素.appendChild(标题元素);
        条目元素.appendChild(内容元素);

        条目元素.dataset.id = 数据.id;
        条目元素.dataset.uuid = 数据.uuid;
        条目元素.dataset.序号 = 数据.序号;

        return 条目元素;
    }

    // 更新条目内容
    更新条目(条目元素, 数据) {
        条目元素.querySelector('.条目-标题').textContent = 数据.文档内容.名称;
        const 内容元素 = 条目元素.querySelector('.条目-内容');
        内容元素.innerHTML = ''; // 清空现有内容

        // 动态生成内容项
        Object.entries(数据.文档内容).forEach(([字段, 值]) => {
            内容元素.appendChild(this.生成内容项(字段, 值));
        });

        条目元素.dataset.id = 数据.id;
        条目元素.dataset.uuid = 数据.uuid;
        条目元素.dataset.序号 = 数据.序号;
    }

    填充条目(合集数据, 是否更新当前合集内容列表 = true) {
        if (!Array.isArray(合集数据)) {
            console.error('条目数据格式不正确！', 合集数据);
            return;
        }

        const 新条目数据 = 合集数据;
        const 现有条目元素 = Array.from(this.元总容器.children);
        const 旧条目数据 = window.app.当前合集内容列表 || [];

        新条目数据.forEach(数据 => {
            const 条目元素 = 现有条目元素.find(元素 => 元素.dataset.uuid === 数据.uuid);
            const 旧数据 = 旧条目数据.find(item => item.uuid === 数据.uuid);

            if (条目元素) {
                if (!this.深比较(数据, 旧数据)) {
                    this.更新条目(条目元素, 数据);
                    console.log('更新条目:', 数据);
                } else {
                    console.log('条目数据未变:', 数据);
                }
            } else {
                const 新条目 = this.创建条目(数据);
                this.元总容器.appendChild(新条目);
            }
        });

        现有条目元素.forEach(元素 => {
            const 条目存在 = 新条目数据.find(数据 => 数据.uuid === 元素.dataset.uuid);
            if (!条目存在) {
                this.元总容器.removeChild(元素);
                // console.log('删除条目:', 元素.dataset.uuid);
            }
        });

        if (是否更新当前合集内容列表) {
            window.app.当前合集内容列表 = 新条目数据;
        } else {
            console.log('当前合集内容列表未更新:', 是否更新当前合集内容列表);
        }
    }

    填充合集选择框(合集列表) {
        this.合集选择框.innerHTML = '';
        合集列表.forEach(合集名称 => {
            const 选项 = document.createElement('option');
            选项.value = 合集名称;
            选项.textContent = 合集名称;
            this.合集选择框.appendChild(选项);
        });
    }

    防抖(func, 延迟) {
        let 定时器;
        return (...参数) => {
            clearTimeout(定时器);
            定时器 = setTimeout(() => {
                func.apply(this, 参数);
            }, 延迟);
        };
    }

    深比较(obj1, obj2) {
        if (typeof obj1 !== 'object' || obj1 === null || typeof obj2 !== 'object' || obj2 === null) {
            return obj1 === obj2;
        }

        const keys1 = Object.keys(obj1);
        const keys2 = Object.keys(obj2);

        if (keys1.length !== keys2.length) {
            return false;
        }

        for (let key of keys1) {
            if (!obj2.hasOwnProperty(key) || !this.深比较(obj1[key], obj2[key])) {
                return false;
            }
        }

        return true;
    }

    async 初始化() {
        const 响应数据 = await window.app.api.后端交互("获取合集列表");
        const 合集列表 = 响应数据.合集列表 || [];

        console.log('合集列表:', 合集列表);
        this.填充合集选择框(合集列表);

        this.合集选择框.addEventListener('change', this.防抖(async () => {
            const 当前合集名称 = this.合集选择框.value;
            window.app.当前合集名称 = 当前合集名称;
            const 条目数据 = await window.app.api.后端交互("获取合集内容", [{ 合集名称: 当前合集名称 }]);
            this.填充条目(条目数据.合集内容);
        }, 300));

        if (合集列表.length > 0) {
            const 默认合集名称 = 合集列表[0];
            this.合集选择框.value = 默认合集名称;
            window.app.当前合集名称 = 默认合集名称;

            const 条目数据 = await window.app.api.后端交互("获取合集内容", [{ 合集名称: 默认合集名称 }]);
            this.填充条目(条目数据.合集内容);
        }
    }

    async 软更新(合集数据, 是否更新当前合集内容列表 = true) {
        if (!合集数据) {
            const 当前合集名称 = this.合集选择框.value;
            window.app.当前合集名称 = 当前合集名称;
            const 条目数据 = await window.app.api.后端交互("获取合集内容", [{ 合集名称: 当前合集名称 }]);
            console.warn('传递合集数据为空，自动获取:', 条目数据);
            this.填充条目(条目数据.合集内容);

            return window.app.生成返回("成功",  "成功软更新");
        }

        this.填充条目(合集数据, 是否更新当前合集内容列表);
        console.log('软更新完成');
    }
}
