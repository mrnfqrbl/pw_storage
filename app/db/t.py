import asyncio
import uuid
import httpx  # 导入 httpx 库
from 上层数据操作 import 上层数据操作

async def main():
    # 初始化数据库连接
    实例 = await 上层数据操作.创建实例("test_db", "mongodb://localhost:27019/")
    await 实例.初始化合集列表()

    # 老合集
    老合集 = "test_collection"
    老合集轮数 = 3

    # 新合集
    新合集 = "new_collection"
    新合集轮数 = 4

    # 从 API 获取数据模型
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:8000/api/获取数据模型")  # 替换为你的 API 地址
        if response.status_code == 200:
            数据模型 = response.json()
            print(f"成功获取数据模型: {数据模型}")
        else:
            print(f"获取数据模型失败，状态码: {response.status_code}")
            return

    # 定义要使用的字段
    使用字段 = ["名称", "应用", "账号"]  # 替换为你要使用的字段

    # 老合集操作
    print(f"\n----- 老合集 {老合集} 操作 -----")
    await 执行合集操作(实例, 老合集, 老合集轮数, 数据模型, 使用字段)

    # 新合集操作
    print(f"\n----- 新合集 {新合集} 操作 -----")
    await 执行合集操作(实例, 新合集, 新合集轮数, 数据模型, 使用字段)

    # 打印最终结果
    print("\n----- 最终结果 -----")
    print(f"老合集 {老合集} 内容:")
    老合集最终结果 = await 实例.获取合集所有内容(老合集)
    for 文档 in 老合集最终结果:
        print(文档)

    print(f"\n新合集 {新合集} 内容:")
    新合集最终结果 = await 实例.获取合集所有内容(新合集)
    for 文档 in 新合集最终结果:
        print(文档)


async def 执行合集操作(实例: 上层数据操作, 合集名称: str, 轮数: int, 数据模型: dict, 使用字段: list):
    """执行合集操作的函数"""
    for 轮数 in range(轮数):
        print(f"----- {合集名称} 第 {轮数 + 1} 轮 -----")

        # 存储新插入文档的 UUID
        新插入文档UUID = []

        # 写入 3 个新的文档
        for i in range(3):
            文档内容 = {}
            for 字段 in 使用字段:
                if 字段 in 数据模型:
                    文档内容[字段] = f"{合集名称}{字段}测试{轮数 * 3 + i + 1}"  # 按照指定格式生成内容
                else:
                    文档内容[字段] = None  # 如果字段不存在，则设置为 None

            文档内容["轮数"] = 轮数 + 1
            文档内容["类型"] = "测试目的"

            插入结果 = await 实例.插入文档(合集名称, 文档内容)
            if 插入结果 and "uuid" in 插入结果:
                新插入文档UUID.append(插入结果["uuid"])
                print(f"已插入文档: {文档内容['名称']}，UUID: {插入结果['uuid']}")
            else:
                print(f"插入文档 {文档内容['名称']} 失败")

        # 修改第二个文档
        if len(新插入文档UUID) > 1:
            修改文档UUID = 新插入文档UUID[1]
            修改内容 = {}
            for 字段 in 使用字段:
                if 字段 in 数据模型:
                    修改内容[字段] = f"{合集名称}{字段}修改测试{轮数 + 1}"  # 按照指定格式生成内容
                else:
                    修改内容[字段] = None  # 如果字段不存在，则设置为 None
            修改内容["状态"] = "已修改"

            await 实例.更新文档(合集名称, 修改文档UUID, 修改内容)
            print(f"已修改文档: {修改文档UUID}")
        else:
            print("没有可修改的文档 (需要至少 2 个)")

        # 删除第三个文档
        if len(新插入文档UUID) > 2:
            删除文档UUID = 新插入文档UUID[2]
            await 实例.删除文档(合集名称, 删除文档UUID)
            print(f"已删除文档: {删除文档UUID}")
        else:
            print("没有可删除的文档 (需要至少 3 个)")


if __name__ == "__main__":
    asyncio.run(main())
