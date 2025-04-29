from typing import Dict, List, Any

from fastapi import APIRouter, Query, Depends, Body
from loguru import logger

from app.utils import 文档数据模型

db路由= APIRouter()
from app.api.封装api import api类
# 定义依赖项
# 修改后的 get_api 函数
async def get_api():
    # 假设你已经创建了 api类 实例
    api = api类.获取api实例() # 或者其他方式获取 api类 实例
    return api

@db路由.get("/创建合集")
async def 创建合集(
        合集名称: str = Query(..., title="合集名称", description="要创建的合集名称"),  # 使用 Query 显式声明
        api: api类 = Depends(get_api)
):
    """
    创建合集接口。

    Args:
        合集名称: 要创建的合集名称 (查询参数).

    Returns:
        创建结果: 创建结果.
    """
    创建结果 = await api.数据操作实例.创建合集(合集名称)  # 调用你的数据操作函数
    return 创建结果

@db路由.get("/获取合集列表")
async def 获取合集列表(api: api类 = Depends(get_api)):
    """
    获取合集列表接口。

    Returns:
        合集列表: 包含所有合集名称的列表.
    """
    合集列表 = api.数据操作实例.获取合集列表()  # 调用你的数据操作函数

    return {"合集列表": 合集列表}
@db路由.get("/获取合集内容")
async def 获取合集内容(
        合集名称: str = Query(..., title="合集名称", description="要查询的合集名称"),  # 使用 Query 显式声明
        api: api类 = Depends(get_api)
):
    """
    获取合集内容接口。

    Args:
        合集名称: 要查询的合集名称 (查询参数).

    Returns:
        合集内容: 合集内容.
    """
    合集内容 = await api.数据操作实例.获取合集所有内容(合集名称)  # 调用
    return {"合集内容": 合集内容}

@db路由.post("/查询条目", response_model=None)
async def 查询条目(
        合集名称: str = Query(..., title="合集名称", description="要查询的合集名称"),  # 使用 Query 显式声明
        请求体: Dict = Body({}, title="查询条件", description="查询条件 (JSON)"),  # 使用 Body 显式声明
        api: api类 = Depends(get_api)
) -> List[Dict[str, Any]]:
    """
    查询条目接口 (使用查询参数和请求体).

    Args:
        合集名称: 要查询的合集名称 (查询参数).
        查询条件: 查询条件 (JSON 格式，请求体).

    Returns:
        查询文档: 查询结果.
    """
    查询条件=请求体.get("查询条件",None)
    if not 查询条件:
        # return {"错误": "新增文档为空或请求体没有新增文档字段"}
        查询条件=请求体
    logger.info(f"查询条件: {查询条件}")
    数据模型=文档数据模型.文档内容模型().model_dump()
    #如果查询条件的键在数据模型中，则修改查询条件的键位 “文档内容.原键”值不变
    新的查询条件 = {}
    不符合数据格式的查询条件={}
    for 键, 值 in 查询条件.items():
        if 键 in 数据模型.keys():
            logger.info(f"{键}在数据模型中，但是没有正确嵌套数据库查询格式，以更正")
            新的键 = f"文档内容.{键}"  # 创建新的键
            新的查询条件[新的键] = 值  # 将键值对添加到新的字典中
        else:
            新的查询条件[键] = 值 # 将不在数据模型中的键值对也添加到新的字典中




    查询条件 = 新的查询条件  # 用新的字典替换旧的字典


    查询结果 = await api.数据操作实例.查询文档(合集名称, 查询条件)
    return 查询结果 if 查询结果 else {"错误": "查询结果为空"}





@db路由.get("/查询历史记录")
async def 查询历史记录(
        合集名称: str = Query(..., title="合集名称", description="要查询的合集名称"),  # 使用 Query 显式声明并添加描述
        uuid: str = Query(..., title="uuid", description="要查询的文档UUID"),
        api: api类 = Depends(get_api)
) -> List[Dict[str, Any]]:
    """
    查询历史记录接口。

    Args:
        合集名称: 要查询的合集名称 (查询参数).
        uuid: 要查询的UUID (查询参数).

    Returns:
        查询历史记录: 查询结果.
    """
    查询历史记录结果 = await api.数据操作实例.查询历史记录(合集名称, uuid)  # 调用你的数据操作函数

    return 查询历史记录结果

@db路由.post("/增加条目")
async def 增加条目(
        请求体: Dict[str, Dict[str,str]] = Body(...,  title="新增文档", description="要增加的文档 (JSON 格式)") ,  # FastAPI 会自动从请求体中获取
        # 新增文档: 文档数据模型.文档内容模型 = Body(..., title="新增文档", description="要增加的文档 (JSON 格式)"),

        api: api类 = Depends(get_api),

        合集名称: str = Query(..., title="合集名称", description="要增加条目的合集名称")


):
    """
    增加条目接口 (使用查询参数和请求体).

    Args:
        合集名称: 要增加条目的合集名称 (查询参数).
        新增文档: 要增加的文档 (JSON 格式，请求体).

    Returns:
        新增文档: 插入后的文档.
    """

    logger.info(f"请求体: {请求体}")

    新增文档=请求体.get("新增文档",None)
    if not 新增文档:
        # return {"错误": "新增文档为空或请求体没有新增文档字段"}
        新增文档=请求体
    新增文档=文档数据模型.文档内容模型(**新增文档).model_dump()
    for 字段, 值 in 新增文档.items():
        if 值 is not None:
            新增文档结果 = await api.数据操作实例.插入文档(合集名称, 新增文档)
            return 新增文档结果
        else:
            return {"错误": "尝试获取请求体字段新增文档和将请求体作为字段进行模型验证后值均为空"}




    # 提取插入文档的 _id 并返回



@db路由.put("/修改条目")
async def 修改条目(
        请求体: Any = Body(..., title="修改内容", description="要修改的文档 (JSON 格式)"),  # FastAPI 会自动从请求体中获取
        合集名称: str = Query(..., title="合集名称", description="要修改条目的合集名称"),  # 使用 Query 显式声明
        api: api类 = Depends(get_api),
):
    修改内容=请求体.get("修改内容",None)
    if not 修改内容:
        # return {"错误": "新增文档为空或请求体没有新增文档字段"}
        修改内容=请求体
    logger.info(f"修改内容:{修改内容}")
    for 键,值 in 修改内容.items():

        uuid=键
        修改内容=值
        修改结果 = await api.数据操作实例.更新文档(合集名称, uuid, 修改内容)



        return 修改结果



@db路由.delete("/删除条目")
async def 删除条目(
        合集名称: str = Query(..., title="合集名称", description="要删除条目的合集名称"),  # 使用 Query 显式声明
        uuid: str = Query(..., title="uuid", description="要删除的UUID") , # 使用 Query 显式声明
        api: api类 = Depends(get_api),
):
    删除结果 = await api.数据操作实例.删除文档(合集名称, uuid)
    return 删除结果



@db路由.get("/获取数据模型")
async def 获取数据模型():
    数据模型=文档数据模型.文档内容模型().model_dump()

    return 数据模型




# 手动构建接口信息
接口列表数据 = [
    {
        "路径": "/",
        "方法": "GET",
        "描述": "根路由，返回 Hello World",
        "参数": []
    },
    {
        "路径":"/创建合集",
        "方法": "POST",
        "描述": "创建一个新的合集",
        "参数": [
            {
                "参数名": "合集名称",
                "参数类型": "str",
                "参数位置": "query",
                "描述": "要创建的合集名称"
            }
        ],


    },
    {
        "路径": "/获取合集列表",
        "方法": "GET",
        "描述": "获取所有合集名称的列表",
        "参数": []
    },
    {
        "路径": "/获取合集内容",
        "方法": "GET",
        "描述": "获取指定合集的内容",
        "参数": [
            {
                "参数名": "合集名称",
                "参数类型": "str",
                "参数位置": "query",
                "描述": "要查询的合集名称"
            }
        ]
    },
    {
        "路径": "/查询条目",
        "方法": "POST",
        "描述": "根据条件查询合集中的条目",
        "参数": [
            {
                "参数名": "合集名称",
                "参数类型": "str",
                "参数位置": "query",
                "描述": "要查询的合集名称"
            },
            {
                "参数名": "查询条件",
                "参数类型": "Dict",
                "参数位置": "body",
                "描述": "查询条件，JSON 格式"
            }
        ]
    },
    {
        "路径": "/查询历史记录",
        "方法": "GET",
        "描述": "查询指定文档的历史记录",
        "参数": [
            {
                "参数名": "合集名称",
                "参数类型": "str",
                "参数位置": "query",
                "描述": "要查询的合集名称"
            },
            {
                "参数名": "uuid",
                "参数类型": "str",
                "参数位置": "query",
                "描述": "要查询的文档 UUID"
            }
        ]
    },
    {
        "路径": "/增加条目",
        "方法": "POST",
        "描述": "向指定合集增加一个条目",
        "参数": [
            {
                "参数名": "合集名称",
                "参数类型": "str",
                "参数位置": "query",
                "描述": "要增加条目的合集名称"
            },
            {
                "参数名": "新增文档",
                "参数类型": 文档数据模型.文档内容模型().model_dump(),
                "参数位置": "body",
                "描述": "要增加的文档，JSON 格式"
            }
        ]
    },
    {
        "路径": "/修改条目",
        "方法": "PUT",
        "描述": "修改指定合集中的一个条目",
        "参数": [
            {
                "参数名": "合集名称",
                "参数类型": "str",
                "参数位置": "query",
                "描述": "要修改条目的合集名称"
            },
            {
                "参数名": "修改内容",
                "参数类型": "Dict[str, Dict[str, str]]",
                "参数位置": "body",
                "描述": "要修改的内容，JSON 格式"
            }
        ]
    },
    {
        "路径": "/删除条目",
        "方法": "DELETE",
        "描述": "删除指定合集中的一个条目",
        "参数": [
            {
                "参数名": "合集名称",
                "参数类型": "str",
                "参数位置": "query",
                "描述": "要删除条目的合集名称"
            },
            {
                "参数名": "uuid",
                "参数类型": "str",
                "参数位置": "query",
                "描述": "要删除的文档 UUID"
            }
        ]
    },
    {
        "路径": "/获取数据模型",
        "方法": "GET",
        "描述": "获取文档数据模型",
        "参数": []
    }
]


@db路由.get("/获取接口列表")
async def 获取接口列表() -> Dict[str, List[Dict[str, Any]]]:
    """
    手动构建所有接口列表，包含参数类型、位置和描述信息。

    Returns:
        接口列表: 包含所有接口路径和参数信息的列表。
    """
    # logger.info(f"接口列表: {接口列表数据}")
    return {"接口列表": 接口列表数据}
