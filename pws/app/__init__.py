


from pws.app.core.总线.事件总线 import 事件总线
事件总线实例=事件总线()
from pws.app.core.总线.工具函数类 import 总线工具函数





from ..pkg.db import 数据库总线适配器
from ..pkg.日志 import 日志模块

#导入底层
from ..pkg.db.mongo import MongoDB数据库
from ..pkg.上层数据操作 import 数据操作适配器

class 应用模块:
    def __init__(self,数据库连接字符串:str,数据库名称:str):
        self.事件总线实例=事件总线实例
        self.日志模块=日志模块(事件总线实例=self.事件总线实例)

        self.数据库=MongoDB数据库(连接字符串=数据库连接字符串,数据库名称=数据库名称,总线=self.事件总线实例)
        self.数据库适配层实例=数据库总线适配器(总线=self.事件总线实例,数据库实例=self.数据库)
        self.数据操作适配实例=数据操作适配器(事件总线=self.事件总线实例)


