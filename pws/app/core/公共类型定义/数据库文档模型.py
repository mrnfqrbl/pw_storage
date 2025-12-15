#/app/utils/文档数据模型.py
import datetime
from dataclasses import dataclass
from typing import Optional, Dict, Any, Union, List
from typing import Literal, Dict, Any, Optional
from pydantic import BaseModel
from pydantic import BaseModel, validator

from obj2dict import 可序列化基类 as 可序列化类基础模型
import uuid as _uuid

class 文档内容模型(可序列化类基础模型):
    def __init__(self,**kwargs):
        self.名称: Optional[str] = kwargs.get("名称",None)  # 名称
        self.应用: Optional[str] = kwargs.get("应用",None)  # 应用
        self.账号: Optional[str] = kwargs.get("账号",None)  # 账号
        self.密码: Optional[str] = kwargs.get("密码",None)  # 密码，可选
        self.邮箱: Optional[str] = kwargs.get("邮箱",None)  # 邮箱，可选
        self.邮箱密码: Optional[str] = kwargs.get("邮箱密码",None)  # 邮箱密码，可选
        self.网站: Optional[str] = kwargs.get("网站",None)  # 网站，可选
        self.备注: Optional[str] = kwargs.get("备注",None)  # 备注，可选


class 文档模型(可序列化类基础模型):
    def __init__(self,**kwargs):
        self.uuid:str=kwargs.get("uuid",_uuid.uuid4().hex[:8])
        self.序号:Union[int,None]=kwargs.get("序号",None)
        #同时判断是否是文档内容模型否则还是创建实例
        #文档内容为文档内容模型或者字典
        文档内容:Union[文档内容模型,Dict[str,Any]]=kwargs.get("文档内容",{})
        if 文档内容:

            if isinstance(文档内容,文档内容模型):
                self.文档内容:文档内容模型=文档内容
            else:
                self.文档内容:文档内容模型=文档内容模型(**文档内容)
        else:
            self.文档内容:文档内容模型=文档内容模型(**kwargs)





@dataclass
class 历史记录模型(可序列化类基础模型):
    创建 = "创建"
    修改 = "修改"
    删除 = "删除"
    查询 = "查询"
    成功 = "成功"
    失败 = "失败"

    def __init__(self, **kwargs):
        self.序号: Optional[int] = kwargs.get("序号")
        self.文档序号: Optional[int] = kwargs.get("文档序号")
        self.文档uuid: Optional[str] = kwargs.get("文档uuid")
        self.uuid: str = kwargs.get("uuid", _uuid.uuid4().hex[:8])

        # 事件类型必须提供
        self.事件类型: str = kwargs.get("事件类型")
        if self.事件类型 not in ("创建","修改","删除","查询"):
            raise ValueError("事件类型必须提供: '创建','修改','删除','查询'")

        # 状态默认失败
        self.状态: str = kwargs.get("状态", self.失败)
        if self.状态 not in ("成功","失败"):
            raise ValueError(f"状态只能是 '成功' 或 '失败', 当前值: {self.状态}")

        # 根据事件类型生成对应字段
        if self.事件类型 in ("创建","修改"):
            操作后文档 = kwargs.get("操作后文档")
            self.操作后文档: Optional[文档内容模型] = 文档内容模型(**操作后文档) if isinstance(操作后文档, dict) else 操作后文档
        if self.事件类型 == "修改":
            操作前文档 = kwargs.get("操作前文档")
            self.操作前文档: Optional[文档内容模型] = 文档内容模型(**操作前文档) if isinstance(操作前文档, dict) else 操作前文档
            self.变化字段: Optional[Dict[str, Any]] = kwargs.get("变化字段")
        if self.事件类型 == "删除":
            操作前文档 = kwargs.get("操作前文档")
            self.操作前文档: Optional[文档内容模型] = 文档内容模型(**操作前文档) if isinstance(操作前文档, dict) else 操作前文档
        if self.事件类型 == "查询":
            self.查询条件: Optional[Dict[str, Any]] = kwargs.get("查询条件")
            self.查询结果: Optional[Dict[str, Any]] = kwargs.get("查询结果")
__all__ = [
    "文档内容模型",

    "文档模型",
    "历史记录模型",

]


if __name__ == "__main__":
    字典={
        "序号":1,
        "文档内容":{
            "名称":"测试文档",

            "密码":"测试密码",
            "邮箱":"测试邮箱",
            "邮箱密码":"测试邮箱密码",
            "网站":"测试网站",
            "备注":"测试备注",
        }
    }
    文档=文档模型(**字典)
    print(type(文档.文档内容))
