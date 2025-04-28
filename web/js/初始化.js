// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {

    // 调用其他模块的初始化函数

    // 定义一个异步函数来顺序执行初始化
    async function 顺序初始化() {
        // 等待 api 模块初始化完成
        await window.app.api.初始化();
        console.log("api 模块初始化完成"); // 输出提示信息
        await window.app.api.创建新增文档模板()
        console.log("创建新增文档模板");
        // window.按钮绑定实例 = new window.按钮绑定();
        // window.按钮绑定实例.初始化();
        (window.按钮绑定实例 = new window.app.按钮绑定()).初始化(); // 创建并初始化按钮绑定实例

        console.log("初始化按钮绑定");

        // api 模块初始化完成后，再初始化 条目填充 模块
        await window.app.条目填充.初始化();
        console.log("初始化条目填充 "); // 输出提示信息
        window.app.右键菜单处理.初始化()
        console.log("初始化右键菜单");
        window.app.搜索框.初始化()
        console.log("初始化搜索框");


    }

    // 调用顺序初始化函数
    顺序初始化();
});
