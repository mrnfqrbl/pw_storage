import os

from app.db import 上层数据操作
from fastapi import FastAPI
class api类(FastAPI):
    _实例 = None  # 私有类变量，用于存储单例实例
    数据库名称=os.environ.get("数据库名称","密码存储")
    数据库连接url=os.environ.get("数据库连接url","mongodb://localhost:27019")
    def __init__(self, **x):
        super().__init__(**x)
        self.静态资源目录 = None
        self.数据操作实例 = None  # 初始化数据操作实例
        self.文档数据模型 = None # 初始化文档数据模型


    @classmethod
    async def 创建api实例(cls,**x):
        """
        创建 Api数据库 的单例实例。

        Args:
            数据库名称: 数据库的名称.
            数据库连接url: 数据库连接的URL.

        Returns:
            Api数据库: Api数据库 的单例实例.
        """
        if cls._实例 is None:
            cls._实例 = api类(**x)  # 创建 api_db 实例
            cls._实例.数据操作实例 = await 上层数据操作.创建实例(cls.数据库名称, cls.数据库连接url)  # 执行异步操作
            from app.utils import 文档数据模型
            cls._实例.文档数据模型 = 文档数据模型
        return cls._实例  # 返回单例实例
    @classmethod
    def 获取api实例(cls):
        """
        获取 Api数据库 的单例实例。
        """
        return cls._实例