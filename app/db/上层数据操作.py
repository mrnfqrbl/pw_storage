# /app/db/上层数据操作.py
"""
返回规范：{"结果":  "成功 or  失败 ", 其余字段}
"""

import asyncio
import datetime
import random
import string
from typing import Literal
from uuid import uuid4

from loguru import logger
from pydantic import ValidationError

from app.db.基础数据库操作 import 数据库操作
from app.utils.文档数据模型 import *


class 上层数据操作(数据库操作):
    _instance = None  # 单例模式的实例

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(上层数据操作, cls).__new__(cls)
        return cls._instance

    def __init__(self, 数据库名称: str, 数据库连接url: str):
        """
        初始化上层数据操作类。

        Args:
            数据库名称: 要连接的数据库的名称。
            数据库连接url: MongoDB 连接 URL。
        """
        if hasattr(self, '初始化完成'):  # 避免重复初始化
            return

        super().__init__(数据库名称, 数据库连接url)  # 调用父类的初始化方法
        self.数据库名称 = 数据库名称
        self.数据库连接url = 数据库连接url


        self.普通合集列表 = []  # 存储普通合集名称的列表
        self.历史记录合集列表 = []  # 存储历史记录合集名称的列表
        self.合集对象字典 = {}  # 存储合集对象的字典，键为合集名称，值为合集对象
        self.初始化完成 = True  # 标记初始化完成
    @classmethod
    async def 创建实例(cls, 数据库名称: str,  数据库连接url: str):
        类=cls(数据库名称, 数据库连接url)
        try:
            await 类.连接数据库()
        except  Exception as e:
            logger.error(f"连接数据库失败: {e}")
            raise
        return 类
    async def 获取数据库对象(self):
        if self.数据库 is None:
            self.数据库 = await self.连接数据库()
        return self.数据库
    async def 连接数据库(self):
        """
        连接到 MongoDB 数据库并获取所有合集信息。
        """
        await super().连接数据库()  # 调用父类的连接数据库方法
        await self.初始化合集列表()


    async def 初始化合集列表(self):
        """
        获取数据库中所有合集，并将其分为普通合集和历史记录合集。
        """


        try:
            合集名称列表 = await self.数据库.list_collection_names()
            for 合集名称 in 合集名称列表:
                if 合集名称.endswith("_历史记录"):
                    if 合集名称 not in self.历史记录合集列表:  # 检查是否已存在
                        self.历史记录合集列表.append(合集名称)
                else:
                    if 合集名称 not in self.普通合集列表:  # 检查是否已存在
                        self.普通合集列表.append(合集名称)

            logger.info(f"普通合集列表: {self.普通合集列表}")
            logger.info(f"历史记录合集列表: {self.历史记录合集列表}")

            # 初始化合集对象字典
            for 合集名称 in 合集名称列表:
                self.合集对象字典[合集名称] = self.数据库[合集名称]



        except Exception as e:
            logger.error(f"初始化合集列表失败: {e}")
            raise


    async def 获取合集对象(self, 合集名称: str):
        """
        根据合集名称获取合集对象。如果合集不存在，则自动创建。

        Args:
            合集名称: 要获取的合集名称。

        Returns:
            合集对象。如果获取失败，返回 None。
        """
        if 合集名称 in self.合集对象字典:
            return self.合集对象字典[合集名称]
        else:
            logger.warning(f"合集 {合集名称} 不存在，尝试自动创建")
            try:
                await self.创建合集(合集名称)
                # 创建成功后，将合集对象添加到字典中
                self.合集对象字典[合集名称] = self.数据库[合集名称]
                return self.合集对象字典[合集名称]
            except Exception as e:
                logger.error(f"自动创建合集 {合集名称} 失败: {e}")
                return None

    async def 创建合集(self, 合集名称: str):
        """
        创建一个新的合集。

        Args:
            合集名称: 要创建的合集名称。
        """
        await self.数据库.create_collection(合集名称)
        if 合集名称.endswith("_历史记录"):
            self.历史记录合集列表.append(合集名称)
            logger.info(f"成功创建历史记录合集: {合集名称}")
        else:
            self.普通合集列表.append(合集名称)
            logger.info(f"成功创建普通合集: {合集名称}")
        self.合集对象字典[合集名称] = self.数据库[合集名称]

    async def 获取最大序号(self, 合集名称: str,序号键:str) -> int:
        """
        获取指定合集中最大的序号。

        Args:
            合集名称: 要查询的合集名称。

        Returns:
            最大的序号，如果合集为空则返回 0。
        """
        合集对象 = await self.获取合集对象(合集名称)
        if 合集对象 is None:
            logger.error(f"合集 {合集名称} 不存在，无法获取最大序号")
            return 0

        try:
            最后一个文档 = await 合集对象.find_one(sort=[(序号键, -1)])  # 查找序号最大的文档
            if 最后一个文档 and 序号键 in 最后一个文档:
                最大序号 =最后一个文档[序号键]
                return 最大序号
            else:

                logger.warning(f"合集 {合集名称} 为空")
                return 0  # 合集为空或没有序号字段
        except Exception as e:
            logger.error(f"获取最大序号失败: {e}，合集: {合集名称}")
            return 0

    async def 插入文档(self, 合集名称: str, 文档: dict):
        """
        插入一个文档到指定的合集中。

        Args:
            合集名称: 要插入文档的合集名称。
            文档: 要插入的文档（字典）。

        Returns:
            插入结果。
        """

        合集对象 = await self.获取合集对象(合集名称)
        if 合集对象 is None:
            logger.error(f"无法获取合集对象，合集名称: {合集名称}")
            return None  # 如果获取合集对象失败，直接返回 None

        try:
            # 获取下一个可用的序号
            最大序号 = await self.获取最大序号(合集名称, "序号")
            # 文档["序号"] = 最大序号 + 1
            #id位随机生成5个字母数字大小写随机组合集对象
            id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

            uuid=str(uuid4())
            logger.info(f"初始文档:{文档}")
            文档内容=文档内容模型(**文档)
            logger.info(f"验证前文档内容:{文档内容}")
            文档={
                "id":id,
                "uuid":uuid,

                "文档内容":文档内容
            }
            logger.info(f"验证前文档:{文档}")
            验证后文档=数据库文档创建模型(**文档)


            # 记录增加历史记录
            # 增加历史记录文档=文档增加历史记录模型(
            #     修改时间=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            #     历史记录序号=最大序号 + 1,
            #     操作类型="增加",
            #     文档id=验证后文档.id,
            #     文档uuid=验证后文档.uuid,
            #     时间节点=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            #     状态="失败",
            #     新增内容=验证后文档.文档内容
            # )
            结果 = await self.记录增加历史记录(合集名称, 验证后文档,最大序号)
            if 结果:
                历史记录uuid = 结果.get("uuid")
            else:
                logger.error(f"插入文档失败，合集: {合集名称}")
                历史记录uuid =None
            # 历史记录状态 = 历史记录结果 is not None

            result = await 合集对象.insert_one(验证后文档.dict())
            插入成功 = result.inserted_id is not None

            if 插入成功:
                logger.info(f"文档插入成功，ID: {result.inserted_id}，合集: {合集名称}")
                if 历史记录uuid:
                    await self.更新历史记录状态(历史记录uuid, "成功", f"{合集名称}_历史记录")
                return {"结果":  "成功", "uuid": uuid}
            else:
                logger.error(f"插入文档失败，合集: {合集名称}")
                if 历史记录uuid:
                    await self.更新历史记录状态(历史记录uuid, "失败", f"{合集名称}_历史记录")
                return {"结果": "失败", "uuid": uuid}

        except Exception as e:
            raise


    async def 查询文档(self, 合集名称: str, 查询条件: dict):
        """
        根据查询条件查询指定合集中的文档。

        Args:
            合集名称: 要查询的合集名称。
            查询条件: 查询条件（字典）。

        Returns:
            查询结果（列表，每个元素是字典）。
        """
        logger.info(f"查询文档，查询条件: {查询条件}，合集: {合集名称}")
        合集对象 = await self.获取合集对象(合集名称)
        if 合集对象 is None:
            logger.error(f"合集 {合集名称} 不存在，无法查询文档")
            return None

        try:

            结果 = await 合集对象.find(查询条件,projection={"_id": 0}).to_list(length=None)
            logger.info(f"查询到 {len(结果)} 个文档，合集: {合集名称}")
            return 结果
        except Exception as e:
            logger.error(f"查询文档失败: {e}，合集: {合集名称}")
            return None

    async def 更新文档(self, 合集名称: str, uuid: str, 更新内容: dict):
        """
        根据查询条件更新指定合集中的文档，并自动记录历史记录。

        Args:
            合集名称: 要更新的合集名称。
            uuid: 文档的uuid
            更新内容: 更新内容（字典，使用 $set 操作符）。

        Returns:
            更新结果。
        """
        合集对象 = await self.获取合集对象(合集名称)
        if 合集对象 is None:
            logger.error(f"合集 {合集名称} 不存在，无法更新文档")
            return None

        # 1. 获取更新前的文档
        查询条件 = {"uuid": uuid}
        原始文档 = await 合集对象.find_one(查询条件)
        if not 原始文档:
            logger.warning(f"未找到符合条件的文档，合集: {合集名称}, UUID: {uuid}")
            return None
        记录内容={}
        # 2. 记录历史记录
        for 键, 值 in 更新内容.items():
            记录内容[键] = {
                "更新值": 值,
                "原始值": 原始文档["文档内容"].get(键, None)  # 使用 get 方法避免 KeyError
            }



        结果 = await self.记录修改历史记录(合集名称, 原始文档, 记录内容 )
        if not 结果:
            logger.error(f"记录历史记录失败，合集: {合集名称}")
            return None
        else:
            历史记录uuid = 结果.get("uuid")


        # 3. 更新文档
        def 清除空值(数据: dict) -> dict:
            """
            清除字典中值为空的键值对.

            Args:
                数据: 要清除空值的字典.

            Returns:
                清除空值后的字典.
            """
            return {键: 值 for 键, 值 in 数据.items() if 值}
        try:
            更新内容 = 文档内容模型(**更新内容).model_dump()
            更新内容 = 清除空值(更新内容)
            logger.info(f"更新内容: {更新内容}")
        except ValidationError as e:
            logger.error(f"更新文档失败: 类型检测失败: {e}，合集: {合集名称}")
            return {"结果 ":"失败", "返回":"更新文档失败,更新内容不符合规则"}
        except Exception as e:
            logger.error(f"更新文档失败: {e}，合集: {合集名称}")
            return {"结果":"失败", "返回":"更新文档失败,未知错误"}



        try:
            result = await 合集对象.update_one(查询条件, {"$set": {"文档内容": 更新内容}})
            更新成功 = result.modified_count > 0
            if 更新成功:
                logger.info(f"更新了 {result.modified_count} 个文档，合集: {合集名称}")
                logger.info(f"uuid：{历史记录uuid}")
                if 历史记录uuid:
                    await self.更新历史记录状态(历史记录uuid, "成功", f"{合集名称}_历史记录")
                    logger.info(f"历史记录状态跟新")
                return {"结果":"成功","返回":f"修改了{result.modified_count}个条目"}
            else:
                logger.warning(f"未找到符合条件的文档或文档内容未改变，合集: {合集名称}")
                if 历史记录uuid:
                    await self.更新历史记录状态(历史记录uuid, "失败", f"{合集名称}_历史记录")
                return {"结果":"失败","返回":"未找到符合条件的文档或文档内容未改变"}

        except Exception as e:
            logger.error(f"更新文档失败: {e}，合集: {合集名称}")
            if 历史记录uuid:
                await self.更新历史记录状态(历史记录uuid, "失败", f"{合集名称}_历史记录")
            return {"结果":"失败","返回":"未知错误"}


    async def 删除文档(self, 合集名称: str, 文档_uuid: str):
        """
        根据 UUID 删除指定合集中的文档。

        Args:
            合集名称: 要删除文档的合集名称。
            文档_uuid: 要删除的文档的 UUID。

        Returns:
            删除结果。
        """
        合集对象 = await self.获取合集对象(合集名称)
        if 合集对象 is None:
            logger.error(f"合集 {合集名称} 不存在，无法删除文档")
            return None

        # 1. 获取删除前的文档
        原始文档 = await 合集对象.find_one({"uuid": 文档_uuid})
        logger.info(f"原始文档: {原始文档}")
        if 原始文档:
            # 2. 记录历史记录
            结果 = await self.记录删除历史记录(合集名称, 原始文档)
            if 结果:
                历史记录uuid = 结果.get("uuid")
            else:
                历史记录uuid = None


            # 3. 删除文档
            try:
                result = await 合集对象.delete_one({"uuid": 文档_uuid})
                删除成功 = result.deleted_count > 0

                if 删除成功:
                    logger.info(f"删除了 {result.deleted_count} 个文档，UUID: {文档_uuid}，合集: {合集名称}")
                    if 历史记录uuid:
                        await self.更新历史记录状态(历史记录uuid, "成功", f"{合集名称}_历史记录")
                    return {"结果": "成功","返回":f"删除了{result.deleted_count}个条目"}
                else:
                    logger.warning(f"未找到符合条件的文档，UUID: {文档_uuid}，合集: {合集名称}")
                    if 历史记录uuid:
                        await self.更新历史记录状态(历史记录uuid, "失败", f"{合集名称}_历史记录")
                    return {"结果": "失败","返回":"未找到符合条件的文档"}

            except Exception as e:
                logger.error(f"删除文档失败: {e}，UUID: {文档_uuid}，合集: {合集名称}")
                if 历史记录uuid:
                    await self.更新历史记录状态(历史记录uuid, "失败", f"{合集名称}_历史记录")
                return {"结果": "失败","返回":"删除文档失败,未知错误"}
        else:
            logger.warning(f"未找到符合条件的文档，UUID: {文档_uuid}，合集: {合集名称}")
            return {"结果": "失败","返回":"未找到符合条件的文档"}

    async def 记录增加历史记录(self, 合集名称: str, 新增文档: 数据库文档创建模型,最大序号:int):
        """
        记录增加历史记录。

        Args:
            合集名称: 对应的普通合集名称。
            新增文档: 新增的文档。
        """
        历史记录合集名称 = f"{合集名称}_历史记录"
        历史记录合集对象 = await self.获取合集对象(历史记录合集名称)
        if 历史记录合集对象 is None:
            # 如果历史记录合集不存在，则创建
            await self.创建历史记录合集(合集名称)
            历史记录合集对象 = await self.获取合集对象(历史记录合集名称)  # 重新获取，确保已创建

        if 历史记录合集对象 is None:
            logger.error(f"历史记录合集 {历史记录合集名称} 不存在，无法插入增加历史记录文档")
            return None
        uuid=str(uuid4())
        # 构建历史记录模型
        序号=await self.获取最大序号(历史记录合集名称,"历史记录序号")
        logger.info(f"最大序号{序号}")
        历史记录数据 = 文档增加历史记录模型(
            文档id=新增文档.id,
            文档uuid=新增文档.uuid,
            时间节点=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            历史记录uuid=uuid,
            历史记录序号= 序号+1,


            修改时间=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            操作类型="增加",
            新增内容=新增文档.文档内容
        ).model_dump()

        try:
            result = await 历史记录合集对象.insert_one(历史记录数据)
            logger.info(f"增加历史记录文档插入成功，UUID: {uuid}，合集: {历史记录合集名称}")
            return {"结果": "成功", "uuid": uuid}
        except Exception as e:
            logger.error(f"插入增加历史记录文档失败: {e}，合集: {历史记录合集名称}")
            return None

    async def 记录删除历史记录(self, 合集名称: str, 原始文档: dict):
        """
        记录删除历史记录。

        Args:
            合集名称: 对应的普通合集名称。
            原始文档: 删除前的原始文档。
        """
        历史记录合集名称 = f"{合集名称}_历史记录"
        历史记录合集对象 = await self.获取合集对象(历史记录合集名称)
        uuid=str(uuid4())
        if 历史记录合集对象 is None:
            # 如果历史记录合集不存在，则创建
            await self.创建历史记录合集(合集名称)
            历史记录合集对象 = await self.获取合集对象(历史记录合集名称)  # 重新获取，确保已创建

        if 历史记录合集对象 is None:
            logger.error(f"历史记录合集 {历史记录合集名称} 不存在，无法插入删除历史记录文档")
            return None
        最大序号=await self.获取最大序号(历史记录合集名称,"历史记录序号")
        # 构建历史记录模型
        原始文档内容=原始文档.get("文档内容")
        文档实例=文档内容模型(**原始文档内容)

        logger.info(f"文档模型实例: {文档实例}")
        历史记录数据 = 文档删除历史记录模型(
            文档id=原始文档.get("id"),
            文档uuid=原始文档.get("uuid"),
            时间节点=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            历史记录序号=最大序号+1,
            历史记录uuid=uuid,

            操作类型="删除",
            删除内容=文档实例
        ).model_dump()

        try:
            result = await 历史记录合集对象.insert_one(历史记录数据)
            logger.info(f"删除历史记录文档插入成功，UUID: {uuid}，合集: {历史记录合集名称}")
            return {"结果": "成功", "uuid": uuid}
        except Exception as e:
            logger.error(f"插入删除历史记录文档失败: {e}，合集: {历史记录合集名称}")
            return None

    async def 记录修改历史记录(self, 合集名称: str, 原始文档: dict, 更新内容: dict):
        """
        记录修改历史记录。

        Args:
            合集名称: 对应的普通合集名称。
            原始文档: 更新前的原始文档。
            更新内容: 更新的内容（字典）。
        """
        历史记录合集名称 = f"{合集名称}_历史记录"
        历史记录合集对象 = await self.获取合集对象(历史记录合集名称)
        if 历史记录合集对象 is None:
            # 如果历史记录合集不存在，则创建
            await self.创建历史记录合集(合集名称)
            历史记录合集对象 = await self.获取合集对象(历史记录合集名称)  # 重新获取，确保已创建

        if 历史记录合集对象 is None:
            logger.error(f"历史记录合集 {历史记录合集名称} 不存在，无法插入修改历史记录文档")
            return None
        最大序号=await self.获取最大序号(历史记录合集名称,"历史记录序号")
        # 构建历史记录模型
        记录内容={}

        uuid=str(uuid4())
        历史记录数据 = 文档修改历史记录模型(
            文档id=原始文档.get("id"),
            文档uuid=原始文档.get("uuid"),
            时间节点=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            历史记录序号=最大序号+1,
            历史记录uuid=uuid,
            修改时间=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            操作类型="修改",
            修改内容=更新内容
        ).model_dump()

        try:
            result = await 历史记录合集对象.insert_one(历史记录数据)
            logger.info(f"修改历史记录文档插入成功，UUID: {uuid}，合集: {历史记录合集名称}")
            return {"结果": "成功", "uuid": uuid}
        except Exception as e:
            logger.error(f"插入修改历史记录文档失败: {e}，合集: {历史记录合集名称}")
            return None

    async def 更新历史记录状态(self, 历史记录uuid: str, 状态: Literal["成功", "失败"], 历史记录合集名称: str):
        """
        更新历史记录的状态。

        Args:

            状态: 状态（"成功" 或 "失败"）。
            历史记录合集名称: 历史记录合集名称。
        """
        历史记录合集对象 = await self.获取合集对象(历史记录合集名称)
        if 历史记录合集对象 is None:
            logger.error(f"历史记录合集 {历史记录合集名称} 不存在，无法更新历史记录状态")
            return

        try:
            result = await 历史记录合集对象.update_one(
                {"历史记录uuid": 历史记录uuid},
                {"$set": {"状态": 状态}}
            )
            if result.modified_count > 0:
                logger.info(f"历史记录 {历史记录uuid} 的状态已更新为 {状态}，合集: {历史记录合集名称}")
            else:
                logger.warning(f"未找到历史记录 {历史记录uuid}，或状态已是 {状态}，合集: {历史记录合集名称}")
        except Exception as e:
            logger.error(f"更新历史记录状态失败: {e}，合集: {历史记录合集名称}")

    async def 查询历史记录(self, 合集名称: str, 文档uuid: str):
        """
        查询指定合集的历史记录。

        Args:
            合集名称: 对应的普通合集名称。
            查询条件: 查询条件（字典）。

        Returns:
            查询结果（列表，每个元素是文档历史记录模型对象）。
        """
        历史记录合集名称 = f"{合集名称}_历史记录"
        历史记录合集对象 = await self.获取合集对象(历史记录合集名称)
        if 历史记录合集对象 is None:
            logger.error(f"历史记录合集 {历史记录合集名称} 不存在，无法查询历史记录文档")
            return None

        try:
            查询条件 = {"文档uuid": 文档uuid}
            结果 = await 历史记录合集对象.find(查询条件,projection={"_id": 0}).to_list(length=None)
            logger.info(f"查询到 {len(结果)} 个历史记录文档，合集: {历史记录合集名称}")
            return 结果  # 返回字典列表，而不是 Pydantic 模型
        except Exception as e:
            logger.error(f"查询历史记录文档失败: {e}，合集: {历史记录合集名称}")
            return None

    async def 创建历史记录合集(self, 合集名称: str):
        """
        为指定的普通合集创建一个历史记录合集。

        Args:
            合集名称: 对应的普通合集名称。
        """
        历史记录合集名称 = f"{合集名称}_历史记录"
        if 历史记录合集名称 not in self.历史记录合集列表:
            await self.创建合集(历史记录合集名称)
            self.历史记录合集列表.append(历史记录合集名称)
            self.合集对象字典[历史记录合集名称] = self.数据库[历史记录合集名称]
            logger.info(f"成功创建历史记录合集: {历史记录合集名称}")
        else:
            logger.warning(f"历史记录合集 {历史记录合集名称} 已存在")

    def 获取合集列表(self):
        """
        获取所有普通合集的列表。

        Returns:
            普通合集列表。
        """
        return self.普通合集列表

    async def 关闭连接(self):
        """
        关闭数据库连接。
        """
        await super().关闭连接()
        self.合集对象字典 = {}
        self.普通合集列表 = []
        self.历史记录合集列表 = []
        logger.info("数据库连接已关闭，所有合集对象已释放")
    async def  获取合集所有内容(self, 合集名称: str):
        合集对象 = await self.获取合集对象(合集名称)
        if 合集对象 is None:
            logger.error(f"合集 {合集名称} 不存在，无法获取内容")
            return None
        try:
            结果 = await 合集对象.find({},projection={"_id": 0}).to_list(length=None)
            logger.info(f"查询到 {len(结果)} 个文档，合集: {合集名称}")
            return 结果  # 返回字典列表，而不是 Pydantic 模型
        except:
            logger.error(f"查询文档失败，合集: {合集名称}")
            return {"结果": "失败", "原因": "数据库连接错误"}

# 示例用法 (需要异步运行)
async def main():
    数据库名称 = "你的数据库名称"
    数据库连接url = "mongodb://localhost:27017/"

    # 获取单例实例
    数据操作1 = 上层数据操作(数据库名称, 数据库连接url)
    数据操作2 = 上层数据操作(数据库名称, 数据库连接url)  # 再次获取，应该返回同一个实例

    print(f"数据操作1 is 数据操作2: {数据操作1 is 数据操作2}")  # 验证单例模式

    await 数据操作1.连接数据库()

    # 示例：创建普通文档
    await 数据操作1.创建合集("用户")
    用户数据 = {"用户名": "赵六", "年龄": 35, "城市": "北京"}
    result = await 数据操作1.插入文档("用户", 用户数据)
    if result:
        print(f"用户数据插入成功: {result.inserted_id}")
    else:
        print("用户数据插入失败")

    # 示例：更新文档 (会自动记录历史记录)
    更新结果 = await 数据操作1.更新文档("用户", "some-uuid-123", {"年龄": 36, "职业": "工程师"})
    if 更新结果:
        print(f"用户数据更新成功: {更新结果.modified_count} 个文档被修改")
    else:
        print("用户数据更新失败")

    # 示例：删除文档 (会自动记录历史记录)
    删除结果 = await 数据操作1.删除文档("用户", "some-uuid-123")
    if 删除结果:
        print(f"用户数据删除成功: {删除结果.deleted_count} 个文档被删除")
    else:
        print("用户数据删除失败")

    # 示例：查询历史记录
    历史记录查询结果 = await 数据操作1.查询历史记录("用户", {})
    if 历史记录查询结果:
        print(f"查询到的历史记录数量: {len(历史记录查询结果)}")
        #print(f"查询到的历史记录: {历史记录查询结果[0]}")

    # 示例：获取合集列表
    合集列表 = 数据操作1.获取合集列表()
    print(f"合集列表: {合集列表}")

    await 数据操作1.关闭连接()

if __name__ == "__main__":
    asyncio.run(main())
