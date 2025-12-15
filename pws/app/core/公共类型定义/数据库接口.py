from typing import Dict, Any, List, Tuple

from pws.app.core.公共类型定义.事件总线模型 import I事件总线
from pws.app.core.公共类型定义.函数通用返回模型 import 函数通用返回模型



class 数据库接口():
    # ----------------- 连接 -----------------
    def __init__(self, 连接字符串: str, 数据库名称: str, 总线: I事件总线) -> None:
        """
        初始化数据库连接参数，实际连接由子类实现
        """
        self.连接字符串 = 连接字符串
        self.数据库名 = 数据库名称
        self.事件总线 = 总线
        self.数据库 = None
        self.客户端 = None

    def _连接数据库(self, 连接字符串: str, 数据库名称: str) -> 函数通用返回模型:
        """
        内部方法：连接数据库，返回连接状态
        子类必须实现
        """
        raise NotImplementedError

    def 关闭数据库(self) -> None:
        """
        关闭数据库连接
        子类必须实现
        """
        raise NotImplementedError

    # ----------------- 数据集操作 -----------------
    def 获取数据集列表(self) -> 函数通用返回模型:
        """
        获取当前数据库中所有数据集名称
        """
        raise NotImplementedError

    def 创建数据集(self, 数据集名称: str) -> 函数通用返回模型:
        """
        创建数据集
        """
        raise NotImplementedError

    def 删除数据集(self, 数据集名称: str) -> 函数通用返回模型:
        """
        删除指定数据集
        """
        raise NotImplementedError
    def 重命名数据集(self, 数据集名称: str, 新数据集名称: str) -> 函数通用返回模型:
        """
        重命名数据集
        """
        raise NotImplementedError
    # ----------------- 文档操作 -----------------
    def 插入文档(self, 数据集名称: str, 文档: Dict[str, Any]) -> 函数通用返回模型:
        """
        向指定数据集插入单条文档
        """
        raise NotImplementedError

    def 删除文档(self, 数据集名称: str, 条件: Dict[str, Any], 多条: bool = False) -> 函数通用返回模型:
        """
        删除指定条件的文档，可选择删除多条
        """
        raise NotImplementedError

    def 查询文档(
            self,
            数据集名称: str,
            条件: Dict[str, Any] = None,
            投影: Dict[str, Any] = None,
            排序: List[Tuple[str, int]] = None,
            限制: int = None
    ) -> 函数通用返回模型:
        """
        查询文档，支持条件、投影、排序和限制
        """
        raise NotImplementedError

    def 更新文档(
            self,
            数据集名称: str,
            条件: Dict[str, Any],
            更新内容: Dict[str, Any],
            多条: bool = False
    ) -> 函数通用返回模型:
        """
        更新指定条件的文档，可选择更新多条
        """
        raise NotImplementedError

    # ----------------- 索引操作 -----------------
    def 创建索引(self, 数据集名称: str, 索引字段: List[str], 唯一: bool = False) -> 函数通用返回模型:
        """
        创建索引，可选择唯一索引
        """
        raise NotImplementedError

    def 删除索引(self, 数据集名称: str, 索引名称: str = None) -> 函数通用返回模型:
        """
        删除指定索引
        """
        raise NotImplementedError

#---------------------------------辅助功能----------------------------------
    def 获取合集文档最大序号(self, 数据集名称: str) -> 函数通用返回模型:
        """
        获取指定数据集的文档最大序号
        """
        raise NotImplementedError

