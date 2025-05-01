class 表单控制器类 {
    constructor() {
        this.已创建表单 = {};  // 存储已创建的表单
    }

    创建表单对象(表单id, 表单项列表) {
        // 如果表单已经创建过，直接返回
        if (this.已创建表单[表单id]) {
            return this.已创建表单[表单id];
        }

        // 创建新的表单元素
        const 表单 = document.createElement('form');
        表单.id = 表单id;
        表单.className = '表单';

        // 遍历表单项列表，动态创建表单项
        表单项列表.forEach(表单项 => {
            // 创建一个新的表单项容器
            const 表单项容器 = document.createElement('div');
            表单项容器.classList.add('表单项');  // 给每个表单项容器添加一个通用类

            // 根据表单项类型添加不同的中文类名
            switch (表单项.type) {
                case 'text':
                    表单项容器.classList.add('文本输入项');  // 文本输入类型
                    break;
                case 'select':
                    表单项容器.classList.add('选择框项');  // 下拉选择框
                    break;
                case 'button':
                    表单项容器.classList.add('按钮项');  // 按钮类型
                    break;
                case 'checkbox':
                    表单项容器.classList.add('复选框项');  // 复选框
                    break;
                case 'radio':
                    表单项容器.classList.add('单选框项');  // 单选框
                    break;
                case 'textarea':
                    表单项容器.classList.add('文本区域项');  // 文本区域
                    break;
                default:
                    return;  // 未知类型不处理
            }

            let 表单元素;

            // 根据表单项类型创建不同的表单元素
            switch (表单项.type) {
                case 'text':
                    表单元素 = document.createElement('input');
                    表单元素.type = 'text';
                    break;
                case 'select':
                    表单元素 = document.createElement('select');
                    表单项.options.forEach(option => {
                        const optionElement = document.createElement('option');
                        optionElement.value = option.value;
                        optionElement.textContent = option.text;
                        表单元素.appendChild(optionElement);
                    });
                    break;
                case 'button':
                    表单元素 = document.createElement('button');
                    break;
                case 'checkbox':
                    表单元素 = document.createElement('input');
                    表单元素.type = 'checkbox';
                    break;
                case 'radio':
                    表单元素 = document.createElement('input');
                    表单元素.type = 'radio';
                    break;
                case 'textarea':
                    表单元素 = document.createElement('textarea');
                    break;
                default:
                    return;  // 未知类型不处理
            }

            // 设置表单项的通用属性
            表单元素.id = 表单项.id || '';
            表单元素.name = 表单项.name || '';
            表单元素.value = 表单项.value || '';
            表单元素.required = 表单项.required || false;
            表单元素.placeholder = 表单项.placeholder || '';

            // 为表单元素添加label
            if (表单项.type !== 'button') {
                const 标签 = document.createElement('label');
                标签.setAttribute('for', 表单元素.id);
                标签.textContent = 表单项.label || '';
                表单项容器.appendChild(标签);
            }

            // 将表单元素添加到表单项容器中
            表单项容器.appendChild(表单元素);

            // 如果是按钮类型，可能需要绑定事件
            if (表单项.type === 'button' && 表单项.onClick) {
                表单元素.addEventListener('click', 表单项.onClick);
            }

            // 将表单项容器添加到表单中
            表单.appendChild(表单项容器);
        });

        // 存储表单到已创建表单对象中
        this.已创建表单[表单id] = 表单;

        return 表单;
    }
}
