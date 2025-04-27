#/app/utils/文档数据模型.py
from typing import Optional, Dict, Any, Union
from typing import Literal, Dict, Any, Optional
from pydantic import BaseModel
from pydantic import BaseModel, validator


class 文档内容模型(BaseModel):
    """
    文档内容模型，用于存储文档的具体信息

    属性:

        名称 (Optional[str]): 名称，可选.
        应用 (Optional[str]): 应用，可选.
        账号 (Optional[str]): 账号，可选.
        密码 (Optional[str]): 密码，可选.
        邮箱 (Optional[str]): 邮箱，可选.
        邮箱密码 (Optional[str]): 邮箱密码，可选.
        网站 (Optional[str]): 网站，可选.
        备注 (Optional[str]): 备注，可选.
    """

    名称: Optional[str] = None  # 名称
    应用: Optional[str] = None  # 应用
    账号: Optional[str] = None  # 账号
    密码: Optional[str] = None  # 密码，可选
    邮箱: Optional[str] = None  # 邮箱，可选
    邮箱密码: Optional[str] = None  # 邮箱密码，可选
    网站: Optional[str] = None  # 网站，可选
    备注: Optional[str] = None  # 备注，可选


class 数据库文档修改模型(BaseModel):
    """
    数据库文档模型，表示存储在数据库中的文档

    属性:
        id (int): ID，唯一标识符.
        uuid (str): UUID，唯一标识符.
        创建时间 (str): 创建时间.
        更新时间 (str): 更新时间.
        文档内容 (文档内容模型): 文档内容.
    """
    id: Optional[str] = None  # ID
    uuid: str  # UUID，唯一标识符
    序号:  Optional[int] =None


    更新时间: str  # 更新时间
    文档内容: 文档内容模型  # 文档内容

class 数据库文档创建模型(BaseModel):
    """
    数据库文档创建模型，表示创建数据库文档的请求

    属性:
        id (Optional[int]): ID，可选.
        uuid (Optional[str]): UUID，唯一标识符，可选.
        文档内容 (文档内容模型): 文档内容.
    """
    id: str # ID
    uuid: str # UUID，唯一标识符
    序号: Optional[int] = None
    文档内容: 文档内容模型  # 文档内容

class 文档增加历史记录模型(BaseModel):
    """
    文档增加历史记录模型，用于记录文档的增加操作

    属性:
        文档id (int): 文档ID.
        文档uuid (str): 文档UUID.
        时间节点 (str): 时间节点，表示该版本的时间.
        历史记录序号 (int): 历史记录序号.
        修改时间 (str): 修改时间为文档修改前的原始时间而不是定义到历史记录后的时间.
        操作类型 (Literal["增加"]): 操作类型：增加，固定为 "增加".
        新增内容 (Dict[str, Any]): 新增内容，键为文档内容模型的键，值为字符串或其他类型的值.
    """
    文档id: str  # 文档ID
    文档uuid: str  # 文档UUID
    时间节点: str  # 时间节点，表示该版本的时间
    历史记录序号: int
    历史记录uuid: str  # 历史记录ID
    修改时间: str  # 修改时间为文档修改前的原始时间而不是定义到历史记录后的时间
    操作类型: Literal["增加"] = "增加"  # 操作类型：增加
    状态: Optional[Literal["成功", "失败"]] = "失败"
    新增内容: 文档内容模型

class 文档删除历史记录模型(BaseModel):
    """
    文档删除历史记录模型，用于记录文档的删除操作

    属性:
        文档id (int): 文档ID.
        文档uuid (str): 文档UUID.
        时间节点 (str): 时间节点，表示该版本的时间.
        历史记录序号 (int): 历史记录序号.
        修改时间 (str): 修改时间为文档修改前的原始时间而不是定义到历史记录后的时间.
        操作类型 (Literal["删除"]): 操作类型：删除，固定为 "删除".
        删除内容 (Dict[str, Any]): 删除内容，键为文档内容模型的键，值为字符串或其他类型的值.
    """
    文档id: str  # 文档ID
    文档uuid: str  # 文档UUID
    时间节点: str  # 时间节点，表示该版本的时间
    历史记录序号: int
    历史记录uuid: str

    操作类型: Literal["删除"] = "删除"  # 操作类型：删除
    状态: Optional[Literal["成功", "失败"]] = "失败"
    删除内容: 文档内容模型

class 文档修改历史记录模型(BaseModel):
    """
    文档修改历史记录模型，用于记录文档的修改操作

    属性:
        文档id (int): 文档ID.
        文档uuid (str): 文档UUID.
        时间节点 (str): 时间节点，表示该版本的时间.
        历史记录序号 (int): 历史记录序号.
        修改时间 (str): 修改时间为文档修改前的原始时间而不是定义到历史记录后的时间.
        操作类型 (Literal["修改"]): 操作类型：修改，固定为 "修改".
        修改内容 (Dict[str, Any]): 修改内容，键为文档内容模型的键，值为字符串或其他类型的值.
    """
    文档id: str  # 文档ID
    文档uuid: str  # 文档UUID
    时间节点: str  # 时间节点，表示该版本的时间
    历史记录序号: int
    历史记录uuid: str
    修改时间: str  # 修改时间为文档修改前的原始时间而不是定义到历史记录后的时间
    操作类型: Literal["修改"] = "修改"  # 操作类型：修改
    状态: Optional[Literal["成功", "失败"]] = "失败"
    修改内容: Dict[str, Dict[str, Union[str, None]]]

__all__ = [
    "文档内容模型",
    "数据库文档修改模型",
    "数据库文档创建模型",
    "文档增加历史记录模型",
    "文档删除历史记录模型",
    "文档修改历史记录模型",
]