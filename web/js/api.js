







class api类  {
    constructor({基础url, api接口}) {
        // 如果未传入 api接口，则抛出错误
        if (!api接口) {
            throw new Error("api接口不能为空！");
        }

        // 如果基础url为空，使用当前页面的基础URL（例如 http://127.0.0.1:8000）
        this.基础URL = 基础url ? 基础url.replace(/\/+$/, '') : window.location.origin;

        // 去除 api接口 前缀的斜杠（防止双斜杠）
        this.api接口 = api接口.replace(/^\/+/, '').replace(/\/+$/, '');

        // 拼接最终URL
        this.apiurl = this.基础URL + '/' + this.api接口;
        this.apiurl = this.apiurl.replace(/\/+$/, '');
        console.log("api实例已创建，apiURL:", this.apiurl);

        // 初始化接口列表
        this.接口列表 = [];
    }
    async 初始化() {
        try {
            const 接口列表URL = this.apiurl + '/获取接口列表'; // 获取接口列表的URL
            const 响应 = await fetch(接口列表URL);
            if (!响应.ok) {
                throw new Error(`获取接口列表失败: ${响应.status}`);
            }
            const 数据 = await 响应.json();

            // 存储接口列表
            this.接口列表 = 数据.接口列表;
            window.app.接口列表 = 数据.接口列表;


            // console.log("API 模块已初始化，apiURL:", this.apiurl);


        } catch (错误) {
            console.error('初始化 API 模块时出错:', 错误);
        }

    }
    async 后端交互 (接收接口,参数列表) {
        // 接口列表 (你提供的接口定义)


        try {
            // 1. 查找匹配的接口定义
            const 匹配接口 = window.app.接口列表.find(接口 => {
                if (接口.路径 === 接收接口) {
                    return true; // 完全匹配
                } else if (!接收接口.startsWith('/') && 接口.路径 === '/' + 接收接口) {
                    return true; // 添加 / 前缀后匹配
                }
                return false
            });
            if (!匹配接口) {
                throw new Error(`接口 "${接收接口}" 未找到`);
            }

            // 2. 验证参数数量
            console.log("正在验证参数数量...");

            // console.log("匹配接口:", 匹配接口);

            if (匹配接口.参数.length !== 0) { // 只有当接口需要参数时才进行验证
                if (参数列表.length !== 匹配接口.参数.length) {
                    throw new Error(`接口 "${接收接口}" 需要 ${匹配接口.参数.length} 个参数，但传入了 ${参数列表.length} 个`);
                }
            } else {
                console.log(`接口 "${接收接口}" 不需要参数，跳过参数数量验证`);
            }
            // 3. 验证每个参数的类型和位置 (这里可以根据你的需要进行更详细的类型检查)
            for (let i = 0; i < 匹配接口.参数.length; i++) {
                const 预期参数位置=  匹配接口.参数[i]["参数位置"];

                //3.1 检查参数名是否存在于传入的参数对象中
                const 参数名 = 匹配接口.参数[i]["参数名"];



            }

            // 4.  发送请求 (这里只是一个示例，你需要使用 fetch 或其他 HTTP 客户端)
            console.log(`所有参数验证通过，准备发送请求到 ${接收接口}，参数：`, 参数列表);

            //  构建请求选项 (示例，需要根据你的实际情况修改)
            const 请求选项 = {
                method: 匹配接口.方法, // 使用接口定义中的方法
                headers: {
                    'Content-Type': 'application/json' //  通常使用 JSON
                },
                //  根据接口定义和参数位置构造请求体

            };
            const 接口参数字典 = {};
            匹配接口.参数.forEach(参数 => {
                接口参数字典[参数.参数名] = 参数.参数位置;
            });
            let queryParams = new URLSearchParams(); // 用于存储 query 参数
            let bodyParams = {}; // 用于存储 body 参数
            if (参数列表 && 参数列表.length > 0) {
                参数列表.forEach(参数 => {
                    for (const 参数名 in 参数) {
                        if (接口参数字典.hasOwnProperty(参数名)) {

                            const 参数位置 = 接口参数字典[参数名];
                            const 参数值 = 参数[参数名];
                            console.log(`参数位置为 ${参数位置}，参数名: ${参数名}，参数值: ${参数值}`);

                            if (参数位置 === 'query') {
                                queryParams.append(参数名, 参数值);
                            } else if (参数位置 === 'body') {
                                console.log(`参数位置为 body，参数名: ${参数名}，参数值: ${参数值}`);
                                bodyParams[参数名] = 参数值;
                            }
                        }
                    }
                });
            }



            //  发送请求

            if (Object.keys(bodyParams).length > 0) {
                请求选项.body = JSON.stringify(bodyParams);
            }

            // 7. 构建完整的 URL (包含 query 参数)
            const url = new URL(this.apiurl + 匹配接口.路径);
            url.search = queryParams.toString();
            // console.log("完整的 URL:", url.toString());

            console.log("发送请求的选项:", 请求选项);
            console.log("发送请求的 URL:", url.toString());
            console.log("发送请求的body",  请求选项.body);
            // 8. 发送请求
            const 响应 = await fetch(url.toString(), 请求选项);

            //  处理响应
            if (!响应.ok) {
                throw new Error(`HTTP 错误! 状态: ${响应.status}`);
            }

            const 响应数据 = await 响应.json();
            console.log('收到响应:', 响应数据);
            return 响应数据; // 返回响应数据

        } catch (错误) {
            console.error('请求失败:', 错误);
            throw 错误; //  重新抛出错误，让调用者处理
        }
    }
    async 发起请求(请求){
        try {
            const 响应 = await fetch(请求);
            if (!响应.ok) {
                throw new Error(`HTTP 错误! 状态码: ${响应.status}`);
            }
            const 数据 = await 响应.json(); // 或者 response.text()，取决于响应类型
            return 数据; // 返回响应数据
        } catch (错误) {
            console.error("发起请求时出错:", 错误);
            throw 错误; // 重新抛出错误，让调用者处理
        }
    }
    async 创建新增文档模板() {
        this.接口列表.forEach(接口 => {
            if (接口.路径 === "/增加条目") {
                接口.参数.forEach(参数 => {
                    if (参数.参数名 === "新增文档") {
                        window.app.新增文档模板 = 参数.参数类型;
                        console.log("创建全局对象 新增文档模板:", window.app.新增文档模板);
                    }
                });
            }
        });
    }

}






