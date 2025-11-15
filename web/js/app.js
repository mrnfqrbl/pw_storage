

class app类{
    constructor() {

        // 构造函数，初始化 app 对象
        window.app = this;
        // globalThis.app=this;
        this.水印提示 =显示水印提示;
        this.模糊算法 =模糊算法;
        this.api =new api类({"api接口":"/api"});
        this.按钮绑定 =new 按钮绑定类();
        this.条目填充 =new 条目填充类();
        this.右键菜单处理 =new 右键菜单处理类();
        this.表单控制器=new 表单控制器类();
        this.搜索框 =new 搜索框类();



        this.顺序初始化()
        console.log("App 对象已创建");
    }
    async  顺序初始化() {
        // 等待 api 模块初始化完成
        await window.app.api.初始化();

        await window.app.api.创建新增文档模板()
        console.log("创建新增文档模板");
        await window.app.按钮绑定.初始化()


        console.log("初始化按钮绑定");

        // api 模块初始化完成后，再初始化 条目填充 模块
        await window.app.条目填充.初始化();
        console.log("初始化条目填充 "); // 输出提示信息


        // window.app.搜索框.初始化()
        // console.log("初始化搜索框");


    }

    添加app对象 = async (对象字典) => {
        console.log("对象参数", 对象字典);

        if (typeof 对象字典 !== 'object' || 对象字典 === null) {
            console.error("传入的参数必须是一个对象");
            return window.app.生成返回("失败", "参数不是对象");
        }

        let 成功列表 = [];

        for (const 属性名 in 对象字典) {
            if (对象字典.hasOwnProperty(属性名)) {
                this[属性名] = 对象字典[属性名]; // 把每个属性加到 app 上
                成功列表.push(属性名);
            }
        }

        if (成功列表.length > 0) {
            return window.app.生成返回("成功", `添加属性成功: ${成功列表.join("、")}`);
        } else {
            return window.app.生成返回("失败", "对象为空，未添加属性");
        }
    }
    async 生成返回(状态,数据){
        return {"状态":状态, "数据":数据}

    }

}



// window.onload = function() {
//     window.app = new app();
// }
