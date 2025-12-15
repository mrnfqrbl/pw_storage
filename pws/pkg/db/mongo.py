# 文件路径: src/pkg/db/mongodb适配.py
# 中文说明：
# 本模块提供 MongoDB 的适配实现，继承自通用数据库接口
# 完全实现 CRUD、索引操作方法，可替换或扩展为其他数据库
import pymongo
from pymongo.collection import Collection
from typing import List, Dict, Any, Optional, Union, Tuple, cast
from pws.app.core.公共类型定义.数据库接口 import 数据库接口
from pws.app.core.公共类型定义.事件总线模型 import I事件总线
from pws.app.core.公共类型定义.函数通用返回模型 import 函数通用返回模型

class MongoDB数据库(数据库接口):
    """
    MongoDB 数据库实现，继承自通用数据库接口
    """



    # ----------------- 连接 -----------------
    def __init__(self, 连接字符串: str, 数据库名称: str,总线:I事件总线) -> None:
        self.连接字符串 = 连接字符串
        self.数据库名 = 数据库名称
        self.事件总线=总线


        返回=self._连接数据库(连接字符串,数据库名称)
        if 返回.状态 != 函数通用返回模型.成功:
            raise Exception(f"连接数据库 {self.数据库名} 失败，错误信息：{返回.错误信息}")
        else:
            self.事件总线.发布日志("INFO",f"连接数据库 {self.数据库名} 成功")
    # ----------------- 连接 -----------------
    def _连接数据库(self,连接字符串: str, 数据库名称: str) -> 函数通用返回模型:
        try:
            self._客户端 = pymongo.MongoClient(连接字符串)
            self.数据库 = self._客户端[数据库名称]
            return 函数通用返回模型(状态=函数通用返回模型.成功,数据={"数据库名称":self.数据库名,"消息":"数据库连接成功"})
        except Exception as e:
            self.事件总线.发布日志("error",f"连接数据库 {self.数据库名} 失败: {e}")
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息=str(e))

    def 关闭数据库(self) -> None:
        if self._客户端:
            self._客户端.close()
            self._客户端 = None
            self.数据库 = None
            self.事件总线.发布日志("info",f"关闭数据库 {self.数据库名} 成功")
        else:
            self.事件总线.发布日志("warning",f"数据库 {self.数据库名} 未初始化")
    # ----------------- 数据集操作 -----------------

    def 获取数据集列表(self) -> 函数通用返回模型:
        if self.数据库 is None:
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息="数据库未初始化")
        try:
            数据集列表 = self.数据库.list_collection_names()
            return 函数通用返回模型(状态=函数通用返回模型.成功,数据=数据集列表)
        except Exception as e:
            self.事件总线.发布日志("error",f"获取数据集列表失败: {e}")
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息=str(e))
    def 创建数据集(self, 数据集名称: str) -> 函数通用返回模型:
        if self.数据库 is None:
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息="数据库未初始化")
        try:
            self.数据库.create_collection(数据集名称)
            return 函数通用返回模型(状态=函数通用返回模型.成功,数据={"数据集名称":数据集名称,"消息":"数据集创建成功"})
        except Exception as e:
            if "already exists" in str(e):
                self.事件总线.发布日志("warning", f"数据集 {数据集名称} 已存在")
                return 函数通用返回模型(
                        状态=函数通用返回模型.失败,
                        错误信息=f"数据集 {数据集名称} 已存在"
                    )
            self.事件总线.发布日志("error",f"创建数据集 {数据集名称} 失败: {e}")
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息=str(e))
    def 删除数据集(self, 数据集名称: str) -> 函数通用返回模型:
        if self.数据库 is None:
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息="数据库未初始化")
        try:
            self.数据库.drop_collection(数据集名称)
            return 函数通用返回模型(状态=函数通用返回模型.成功,数据={"数据集名称":数据集名称,"消息":"数据集删除成功"})
        except Exception as e:
            self.事件总线.发布日志("error",f"删除数据集 {数据集名称} 失败: {e}")
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息=str(e))
    def 重命名数据集(self, 数据集名称: str, 新数据集名称: str) -> 函数通用返回模型:
        if self.数据库 is None:
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息="数据库未初始化")
        try:
            #判断目标名称是否已经存在
            if 新数据集名称 in self.数据库.list_collection_names():
                self.事件总线.发布日志("error", f"数据集 {新数据集名称} 已存在")
                return 函数通用返回模型(
                        状态=函数通用返回模型.失败,
                        错误信息=f"数据集 {新数据集名称} 已存在"
                    )
            self.数据库[数据集名称].rename(新数据集名称)
            return 函数通用返回模型(状态=函数通用返回模型.成功,数据={"数据集名称":数据集名称,"新数据集名称":新数据集名称,"消息":"数据集重命名成功"})
        except Exception as e:
            self.事件总线.发布日志("error",f"重命名数据集 {数据集名称} 为 {新数据集名称} 失败: {e}")
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息=str(e))
    #-----------------------------文档操作-------------------------------------------------
    def 插入文档(self, 数据集名称: str, 文档: Dict[str, Any]) -> 函数通用返回模型:
        if self.数据库 is None:
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息="数据库未初始化")
        try:
            数据集 = self.数据库[数据集名称]
            文档_id = 数据集.insert_one(文档).inserted_id
            return 函数通用返回模型(状态=函数通用返回模型.成功,数据={"数据集名称":数据集名称,"文档ID":str(文档_id),"消息":"文档插入成功"})
        except Exception as e:
            self.事件总线.发布日志("error",f"插入文档到数据集 {数据集名称} 失败: {e}")
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息=str(e))
    def 删除文档(
            self,
            数据集名称: str,
            条件: Dict[str, Any],
            多条: bool = False
    ) -> 函数通用返回模型:
        if self.数据库 is None:
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息="数据库未初始化")
        try:
            数据集 = self.数据库[数据集名称]
            删除结果 = 数据集.delete_many(条件) if 多条 else 数据集.delete_one(条件)
            return 函数通用返回模型(状态=函数通用返回模型.成功,数据={"数据集名称":数据集名称,"删除数量":删除结果.deleted_count,"消息":"文档删除成功"})
        except Exception as e:
            self.事件总线.发布日志("error",f"删除文档从数据集 {数据集名称} 失败: {e}")
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息=str(e))
    def 查询文档(
            self,
            数据集名称: str,
            条件: Dict[str, Any] = None,
            投影: Dict[str, Any] = None,
            排序: List[Tuple[str, int]] = None,
            限制: int = None
        ) -> 函数通用返回模型:
            if self.数据库 is None:
                return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息="数据库未初始化")
            try:
                数据集 = self.数据库[数据集名称]

                # 1. 动态构建 find 参数
                if 投影:
                    cursor = 数据集.find(条件 or {}, 投影)
                else:
                    cursor = 数据集.find(条件 or {})

                # 2. 排序
                if 排序:
                    cursor = cursor.sort(排序)

                # 3. 限制条数
                if 限制:
                    cursor = cursor.limit(限制)

                文档列表 = list(cursor)
                #过滤去除_id字段
                文档列表 = [{k: v for k, v in doc.items() if k != "_id"} for doc in 文档列表]
                return 函数通用返回模型(
                    状态=函数通用返回模型.成功,
                    数据={"数据集名称": 数据集名称, "文档数量": len(文档列表), "文档列表": 文档列表}
                )

            except Exception as e:
                self.事件总线.发布日志("error", f"查询数据集 {数据集名称} 失败: {e}")
                return 函数通用返回模型(状态=函数通用返回模型.失败, 错误信息=str(e))
    def 更新文档(
            self,
            数据集名称: str,
            条件: Dict[str, Any],
            更新内容: Dict[str, Any],
            多条: bool = False
    ) -> 函数通用返回模型:
        if self.数据库 is None:
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息="数据库未初始化")
        try:
            数据集 = self.数据库[数据集名称]
            更新结果 = 数据集.update_many(条件, {"$set": 更新内容}) if 多条 else 数据集.update_one(条件, {"$set": 更新内容})
            return 函数通用返回模型(状态=函数通用返回模型.成功,数据={"数据集名称":数据集名称,"更新数量":更新结果.modified_count,"消息":"文档更新成功"})
        except Exception as e:
            self.事件总线.发布日志("error",f"更新数据集 {数据集名称} 失败: {e}")
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息=str(e))



    # ---------------------------------索引操作-------------------------------------------------
    def 创建索引(self, 数据集名称: str, 索引字段: List[str], 唯一: bool = False) -> 函数通用返回模型:
        if self.数据库 is None:
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息="数据库未初始化")
        try:
            数据集 = self.数据库[数据集名称]
            索引名称 = 数据集.create_index(索引字段, unique=唯一)
            return 函数通用返回模型(状态=函数通用返回模型.成功,数据={"数据集名称":数据集名称,"索引字段":索引字段,"索引名称":索引名称,"消息":"索引创建成功"})
        except Exception as e:
            self.事件总线.发布日志("error",f"删除索引从数据集 {数据集名称} 失败: {e}")
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息=str(e))

    def 删除索引(self, 数据集名称: str, 索引名称: str = None) -> 函数通用返回模型:
        if self.数据库 is None:
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息="数据库未初始化")
        try:
            数据集 = self.数据库[数据集名称]
            if 索引名称:
                数据集.drop_index(索引名称)
            else:
                return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息="索引名称不能为空")
            return 函数通用返回模型(状态=函数通用返回模型.成功,数据={"数据集名称":数据集名称,"消息":"索引删除成功"})
        except Exception as e:
            self.事件总线.发布日志("error",f"删除索引从数据集 {数据集名称} 失败: {e}")
            return 函数通用返回模型(状态=函数通用返回模型.失败,错误信息=str(e))



    #---------------------------------辅助功能----------------------------------
    def 获取合集文档最大序号(self, 数据集名称: str):
        """
        从指定合集获取序号字段最大值（按序号倒序取第一条）
        """

        函数返回 = self.查询文档(
            数据集名称,
            {},                         # 条件
            None,                       # 投影
            [("序号", -1)],             # ✔ 正确的排序格式：列表 + 元组
            1                           # 限制条数
        )

        if 函数返回.状态 != 函数通用返回模型.成功:
            return 函数通用返回模型(
                状态=函数通用返回模型.失败,
                错误信息=f"数据库查询失败: {函数返回.错误信息}"
            )

        文档列表 = 函数返回.数据.get("文档列表", [])

        # 没有文档 → 最大序号默认为 0（业务可以用作首次插入序号=1）
        if not 文档列表:
            return 函数通用返回模型(
                状态=函数通用返回模型.成功,
                数据=0
            )

        # 第一条文档
        文档 = 文档列表[0]

        # 若序号不存在 → 返回失败
        if "序号" not in 文档:
            return 函数通用返回模型(
                状态=函数通用返回模型.失败,
                错误信息="文档未包含序号字段"
            )

        # 序号可能为 0 → 必须直接返回，而不能用 if 判断真假
        最大序号 = 文档["序号"]

        return 函数通用返回模型(
            状态=函数通用返回模型.成功,
            数据=最大序号
        )
