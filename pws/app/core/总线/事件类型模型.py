import datetime
from typing import Dict, Any


class 日志事件:
    """
    日志事件数据结构，前端模块生成后发布到总线。
    """
    def __init__(self, 等级: str, 消息: str, 包名: str, 函数名: str, 行号: int, 时间戳: float):
        self.等级 = 等级
        self.消息 = 消息
        self.包名 = 包名
        self.函数名 = 函数名
        self.行号 = 行号
        self.时间戳 = 时间戳
        self.时间=datetime.datetime.fromtimestamp(时间戳).strftime("%Y-%m-%d %H:%M:%S")

    def 转字典(self) -> Dict[str, Any]:
        return {
            "等级": self.等级,
            "消息": self.消息,
            "包名": self.包名,
            "函数名": self.函数名,
            "行号": self.行号,
            "时间戳": self.时间戳
        }
