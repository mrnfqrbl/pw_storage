
from dataclasses import dataclass
from typing import Any, Optional, Dict, ClassVar

from pws.app.core.公共类型定义.事件对象模型 import 可序列化类基础模型


@dataclass
class 函数通用返回模型(可序列化类基础模型):
    状态: Optional[str]=None
    数据: Optional[Any] = None
    错误信息: Optional[str] = None
    #类字段（不会在实例中出现，不会被序列化）
    成功: ClassVar[str] = "成功"
    失败: ClassVar[str] = "失败"



if __name__ == "__main__":
    a=函数通用返回模型(状态=函数通用返回模型.成功,数据={"名称":"测试文档1"})

    print("打印一次：", a)
    print("a")
