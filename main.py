import asyncio
import os
import gec
os.environ["数据库名称"] = "test_db"
os.environ["数据库连接url"] = "mongodb://localhost:27019"
from app.api import 创建服务器
async def main():
    服务器  =await 创建服务器()
    await 服务器.serve()

if __name__ == "__main__":
    # os.environ["数据库名称"] = "密码存储"

    asyncio.run( main())