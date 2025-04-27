// api.js - 负责与后端 API 的交互

// 基础URL：如果留空，则使用当前页面URL
// const 基础URL = 'http://127.0.0.1:8000';
const 基础URL = '';
// API URL：所有API请求都从这个URL开始
// 如果基础URL值为空或不存在，则使用页面基础URL
const apiURL = (基础URL ? 基础URL.replace(/\/+$/, '') : window.location.origin.replace(/\/+$/, '')) + '/api';

const api = {
    // 接口列表，用于存储从后端获取的接口信息
    接口列表: [],

    // 初始化函数 (从 /获取接口列表 并构建请求函数)
    初始化: async function () {
        try {
            const 接口列表URL = apiURL + '/获取接口列表'; // 获取接口列表的URL
            const 响应 = await fetch(接口列表URL);
            if (!响应.ok) {
                throw new Error(`获取接口列表失败: ${响应.status}`);
            }
            const 数据 = await 响应.json();

            // 存储接口列表
            this.接口列表 = 数据.接口列表;
            window.接口列表 = 数据.接口列表;


            console.log("API 模块已初始化，基础URL:", apiURL);


        } catch (错误) {
            console.error('初始化 API 模块时出错:', 错误);
        }
    },
    // 后端交互函数
    后端交互: async function (接收接口,参数列表) {
        // 接口列表 (你提供的接口定义)


        try {
            // 1. 查找匹配的接口定义
            const 匹配接口 = 接口列表.find(接口 => {
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

            console.log("匹配接口:", 匹配接口);

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

                            if (参数位置 === 'query') {
                                queryParams.append(参数名, 参数值);
                            } else if (参数位置 === 'body') {
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
            const url = new URL(apiURL + 匹配接口.路径);
            url.search = queryParams.toString();
            console.log("完整的 URL:", url.toString());

            console.log("发送请求的选项:", 请求选项);
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
    },




    发起请求: async function(请求) {
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
    },
    // 在初始化之后，遍历接口列表，查找 "增加条目" 接口，并创建全局对象
    创建新增文档模板: async function() {
        this.接口列表.forEach(接口 => {
            if (接口.路径 === "/增加条目") {
                接口.参数.forEach(参数 => {
                    if (参数.参数名 === "新增文档") {
                        window.新增文档模板 = 参数.参数类型;
                        console.log("创建全局对象 新增文档模板:", window.新增文档模板);
                    }
                });
            }
        });
    }
};

window.api = api; // 导出 api 对象，方便其他模块调用
