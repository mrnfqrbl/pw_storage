// 按钮绑定.js

/**
 * 按钮绑定类 (单例模式)
 * @param {object} api - 包含后端交互函数的对象
 */
class 按钮绑定类 {

    static instance = null;
    constructor(api) {
        if (按钮绑定类.instance) {
            return 按钮绑定类.instance; // 如果已经存在实例，则直接返回
        }

        this.api = api ? api : window.app.api; // 如果 api 存在则使用 api，否则使用 window.api

        this.添加文档按钮 = document.getElementById('添加文档'); // 获取添加文档按钮
        this.创建合集按钮 = document.getElementById('创建合集');

        this.元总容器 = document.getElementById('元素总容器'); // 获取元素总容器

        按钮绑定类.instance = this; // 保存实例
    }

    async 初始化() {
        if (this.添加文档按钮) { // 确保按钮存在
            this.添加文档按钮.addEventListener('click', this.弹出新增文档悬浮窗.bind(this)); // 使用 bind 绑定事件处理函数
        } else {
            console.error('未找到添加文档按钮，请确保按钮的 id 是 "添加文档"'); // 错误处理
        }

        // 初始化 window.新增文档模板
        this.初始化新增文档模板();
        if (this.创建合集按钮){
            this.创建合集按钮.addEventListener('click', this.弹出创建合集悬浮窗.bind(this));
        } else {
            console.error('未找到创建合集按钮，请确保按钮的 id 是 "创建合集"'); // 错误处理
        }
    }

    async 初始化新增文档模板() {
        if (!window.新增文档模板) {
            window.新增文档模板 = await this.api.后端交互("获取数据模型");
            console.warn("window.新增文档模板 未定义，已使用默认值。");
        }
    }
    弹出创建合集悬浮窗() {
        const 悬浮窗 = document.createElement('div');
        悬浮窗.id = '创建合集悬浮窗';
        const 表单参数= [{type:'text',id:'合集名称',label:'合集名称', name:'合集名称', placeholder:'请输入合集名称'},
            
            ]
        const 表单=window.app.表单控制器.创建表单对象("创建合集表单",表单参数)
        悬浮窗.appendChild(表单)



    }
    弹出新增文档悬浮窗() {
        // 1. 创建悬浮窗和表单
        const 悬浮窗 = document.createElement('div');
        悬浮窗.id = '新增文档悬浮窗';
        悬浮窗.className = '新增文档悬浮窗';
        // 悬浮窗.style.cssText = `
        //     position: fixed;
        //     top: 50%;
        //     left: 50%;
        //     transform: translate(-50%, -50%);
        //     background-color: white;
        //     padding: 20px;
        //     border: 1px solid black;
        //     z-index: 1000;
        // `;

        const 表单 = document.createElement('form');
        表单.id = '新增文档表单';

        // 2. 根据 window.app.新增文档模板 创建表单项
        for (const 键 in window.app.新增文档模板) {
            if (window.app.新增文档模板.hasOwnProperty(键)) {
                const 标签 = document.createElement('label');
                标签.textContent = `${键}:`;
                标签.htmlFor = 键;

                const 输入框 = document.createElement('input');
                输入框.type = 'text';
                输入框.id = 键;
                输入框.name = 键;
                输入框.value = window.app.新增文档模板[键] || ''; // 默认值

                表单.appendChild(标签);
                表单.appendChild(输入框);
                表单.appendChild(document.createElement('br')); // 换行
            }
        }

        // 3. 创建确定和取消按钮
        const 确定按钮 = document.createElement('button');
        确定按钮.type = 'button';
        确定按钮.textContent = '确定';
        确定按钮.addEventListener('click', () => {
            // 3.1 获取表单数据
            const 新条目数据 = {};
            for (const 键 in window.app.新增文档模板) {
                if (window.app.新增文档模板.hasOwnProperty(键)) {
                    新条目数据[键] = document.getElementById(键).value;
                }
            }

            // // 3.2 创建新条目
            // const 新条目 = this.创建条目(新条目数据); // 使用条目填充模块的创建条目函数
            // this.元总容器.appendChild(新条目); // 将新条目添加到总容器中

            // 3.3 调用 api.后端交互
            this.api.后端交互("增加条目", [{"合集名称":window.app.当前合集名称},{"新增文档": 新条目数据}])
                .then(结果 => {
                    // 3.4 处理 api.后端交互 的结果
                    if (结果 && 结果.结果 === '成功') {
                        // 成功的情况，可以留空，或者显示成功消息
                        console.log("条目添加成功！");
                        window.app.条目填充.软更新()

                    } else {
                        // 失败的情况，显示错误消息
                        console.error("条目添加失败！", 结果);
                        alert("条目添加失败，请检查控制台！"); // 可以用更友好的方式提示
                    }
                })
                .catch(error => {
                    console.error("API 调用出错！", error);
                    alert("API 调用出错，请检查控制台！");
                });

            // 3.5 关闭悬浮窗
            document.body.removeChild(悬浮窗);

        });

        const 取消按钮 = document.createElement('button');
        取消按钮.type = 'button';
        取消按钮.textContent = '取消';
        取消按钮.addEventListener('click', () => {
            // 关闭悬浮窗
            document.body.removeChild(悬浮窗);
        });

        表单.appendChild(确定按钮);
        表单.appendChild(取消按钮);

        悬浮窗.appendChild(表单);

        // 4. 将悬浮窗添加到 body 中
        document.body.appendChild(悬浮窗);
    }






}
