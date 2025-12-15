import asyncio
import datetime
import json
import logging
import random
import unittest
from typing import List, Dict, Any

from app.db.上层数据操作 import 上层数据操作  # 假设你的上层数据操作类在这个位置
from app.utils.文档数据模型 import 文档内容模型

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Test上层数据操作(unittest.IsolatedAsyncioTestCase):  # 使用 IsolatedAsyncioTestCase
    数据库名称 = "test_db"  # 测试数据库名称
    数据库连接url = "mongodb://localhost:27019/"  # MongoDB 连接 URL
    合集名称列表 = ["test_collection_1", "test_collection_2", "test_collection_3"]  # 测试合集名称列表
    测试结果文件 = "test_results.json"  # 测试结果文件

    async def asyncSetUp(self):
        """
        异步设置测试环境，包括连接数据库和创建合集。
        """
        self.数据操作 = 上层数据操作(self.数据库名称, self.数据库连接url)
        await self.数据操作.连接数据库()

        # 初始化测试结果
        self.测试结果 = {}
        for 合集名称 in self.合集名称列表:
            self.测试结果[合集名称] = {"创建合集": False, "插入": False, "修改": False, "删除": False, "历史记录": False}

        # 清空并创建测试合集
        for 合集名称 in self.合集名称列表:
            await self.清空合集(合集名称)
            # await self.数据操作.创建合集(合集名称)

    async def asyncTearDown(self):
        """
        异步清理测试环境，包括关闭数据库连接和写入测试结果。
        """
        await self.数据操作.关闭连接()
        await self.写入测试结果()

    async def 清空合集(self, 合集名称: str):
        """
        清空指定合集中的所有文档。
        """
        合集对象 = await self.数据操作.获取合集对象(合集名称)
        if 合集对象 is not None:
            await 合集对象.delete_many({})
            logging.info(f"已清空合集: {合集名称}")
        else:
            logging.warning(f"合集 {合集名称} 不存在，无法清空")

    async def 获取合集数据(self, 合集名称: str) -> List[Dict[str, Any]]:
        """
        获取指定合集中的所有数据。

        Args:
            合集名称: 要获取数据的合集名称。

        Returns:
            包含合集数据的列表。
        """
        查询结果 = await self.数据操作.查询文档(合集名称, {})
        return 查询结果 if 查询结果 else []

    async def 插入测试数据(self, 合集名称: str, 数据: List[Dict[str, Any]]):
        """
        批量插入测试数据到指定合集。

        Args:
            合集名称: 要插入数据的合集名称。
            数据: 要插入的数据列表。
        """
        for 文档 in 数据:
            await self.数据操作.插入文档(合集名称, 文档)

    def 生成随机数据(self) -> List[Dict[str, Any]]:
        """
        生成随机测试数据。

        Returns:
            包含随机数据的列表。
        """
        数据 = []
        for i in range(3):
            数据.append({
                "名称": f"条目{i + 1}-{random.randint(1, 100)}",
                "应用": f"应用{i + 1}-{random.randint(1, 100)}",
                "账号": f"账号{i + 1}-{random.randint(1, 100)}",
                "uuid": f"uuid{i + 1}-{random.randint(1, 100)}",
            })
        return 数据

    async def 写入测试结果(self):
        """
        将测试结果写入 JSON 文件。
        """
        try:
            with open(self.测试结果文件, "w", encoding="utf-8") as f:
                json.dump(self.测试结果, f, indent=4, ensure_ascii=False)
            logging.info(f"测试结果已写入文件: {self.测试结果文件}")
        except Exception as e:
            logging.error(f"写入测试结果文件失败: {e}")

    async def test_创建合集_插入_修改_删除(self):
        """
        测试创建合集、插入、修改和删除操作。
        """
        for 合集名称 in self.合集名称列表:
            logging.info(f"开始测试合集: {合集名称}")

            # 1. 准备测试数据
            测试数据 = self.生成随机数据()
            await self.插入测试数据(合集名称, 测试数据)
            self.测试结果[合集名称]["插入"] = True

            # 2. 获取插入后的数据
            插入后数据 = await self.获取合集数据(合集名称)
            self.assertEqual(len(插入后数据), 3)

            # 3. 记录修改前的数据
            修改前数据1 = await self.数据操作.查询文档(合集名称, {"uuid": 测试数据[0]["uuid"]})
            修改前数据2 = await self.数据操作.查询文档(合集名称, {"uuid": 测试数据[1]["uuid"]})
            修改前数据3 = await self.数据操作.查询文档(合集名称, {"uuid": 测试数据[2]["uuid"]})
            self.assertIsNotNone(修改前数据1)
            self.assertIsNotNone(修改前数据2)
            self.assertIsNotNone(修改前数据3)

            # 4. 修改数据
            # 4.1 修改条目1 (通键值三次)
            await self.数据操作.更新文档(合集名称, {"uuid": 测试数据[0]["uuid"]}, {"应用": f"应用1-修改1-{random.randint(1, 100)}"})
            await self.数据操作.更新文档(合集名称, {"uuid": 测试数据[0]["uuid"]}, {"应用": f"应用1-修改2-{random.randint(1, 100)}"})
            await self.数据操作.更新文档(合集名称, {"uuid": 测试数据[0]["uuid"]}, {"应用": f"应用1-修改3-{random.randint(1, 100)}"})

            # 4.2 修改条目2 (两次不通键值，一次和前两次其中一个相同的键值)
            await self.数据操作.更新文档(合集名称, {"uuid": 测试数据[1]["uuid"]}, {"账号": f"账号2-修改1-{random.randint(1, 100)}"})
            await self.数据操作.更新文档(合集名称, {"uuid": 测试数据[1]["uuid"]}, {"备注": f"备注2-修改1-{random.randint(1, 100)}"})
            await self.数据操作.更新文档(合集名称, {"uuid": 测试数据[1]["uuid"]}, {"账号": f"账号2-修改2-{random.randint(1, 100)}"})  # 和第一次相同

            # 4.3 修改条目3 (全部不同键值)
            await self.数据操作.更新文档(合集名称, {"uuid": 测试数据[2]["uuid"]}, {"名称": f"条目3-修改1-{random.randint(1, 100)}"})
            await self.数据操作.更新文档(合集名称, {"uuid": 测试数据[2]["uuid"]}, {"邮箱": f"邮箱3-修改1-{random.randint(1, 100)}"})
            await self.数据操作.更新文档(合集名称, {"uuid": 测试数据[2]["uuid"]}, {"网站": f"网站3-修改1-{random.randint(1, 100)}"})
            self.测试结果[合集名称]["修改"] = True

            # 5. 获取修改后的数据
            修改后数据1 = await self.数据操作.查询文档(合集名称, {"uuid": 测试数据[0]["uuid"]})
            修改后数据2 = await self.数据操作.查询文档(合集名称, {"uuid": 测试数据[1]["uuid"]})
            修改后数据3 = await self.数据操作.查询文档(合集名称, {"uuid": 测试数据[2]["uuid"]})

            # 6. 验证修改是否成功
            self.assertNotEqual(修改后数据1[0]["应用"], 测试数据[0]["应用"])
            self.assertNotEqual(修改后数据2[0]["账号"], 测试数据[1]["账号"])
            self.assertNotEqual(修改后数据2[0]["备注"], 测试数据[1]["备注"])
            self.assertNotEqual(修改后数据3[0]["名称"], 测试数据[2]["名称"])
            self.assertNotEqual(修改后数据3[0]["邮箱"], 测试数据[2]["邮箱"])
            self.assertNotEqual(修改后数据3[0]["网站"], 测试数据[2]["网站"])

            # 7. 记录删除前的数据
            删除前数据1 = await self.数据操作.查询文档(合集名称, {"uuid": 测试数据[0]["uuid"]})
            删除前数据2 = await self.数据操作.查询文档(合集名称, {"uuid": 测试数据[1]["uuid"]})
            删除前数据3 = await self.数据操作.查询文档(合集名称, {"uuid": 测试数据[2]["uuid"]})
            self.assertIsNotNone(删除前数据1)
            self.assertIsNotNone(删除前数据2)
            self.assertIsNotNone(删除前数据3)

            # 8. 删除数据
            await self.数据操作.删除文档(合集名称, 测试数据[0]["uuid"])
            await self.数据操作.删除文档(合集名称, 测试数据[1]["uuid"])
            await self.数据操作.删除文档(合集名称, 测试数据[2]["uuid"])
            self.测试结果[合集名称]["删除"] = True

            # 9. 获取删除后的数据
            删除后数据 = await self.获取合集数据(合集名称)
            self.assertEqual(len(删除后数据), 0)

            # 10. 验证历史记录 (这里可以添加更详细的历史记录验证)
            历史记录1 = await self.数据操作.查询历史记录(合集名称, {"文档uuid": 测试数据[0]["uuid"]})
            历史记录2 = await self.数据操作.查询历史记录(合集名称, {"文档uuid": 测试数据[1]["uuid"]})
            历史记录3 = await self.数据操作.查询历史记录(合集名称, {"文档uuid": 测试数据[2]["uuid"]})
            self.assertGreater(len(历史记录1), 0)
            self.assertGreater(len(历史记录2), 0)
            self.assertGreater(len(历史记录3), 0)
            self.测试结果[合集名称]["历史记录"] = True

            logging.info(f"完成测试合集: {合集名称}")

# 运行测试
if __name__ == "__main__":
    asyncio.run(unittest.main())
