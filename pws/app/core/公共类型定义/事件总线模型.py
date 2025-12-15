# 文件路径: src/pkg/总线/事件总线接口.py
from typing import Protocol, Callable, Any
from abc import ABC, abstractmethod
from pws.app.core.公共类型定义.事件对象模型 import 总线通用事件模型


class I事件总线(ABC):

    @abstractmethod
    def 订阅(self, 事件名: str, 订阅者: str, 处理函数: Callable) -> None:
        ...

    @abstractmethod
    def 取消订阅(self, 事件名: str, 订阅者: str) -> None:
        ...

    @abstractmethod
    def 发布(self, 事件名: str, 事件数据: Any) -> 总线通用事件模型:
        ...
    @abstractmethod
    def 发布异步(self, 事件名: str, 事件数据: Any):
        ...
    @abstractmethod
    def 发布日志(self, 级别: str, 消息: str) -> None:
        ...