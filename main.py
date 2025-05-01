import asyncio
import os
import gec
os.environ["数据库名称"] = "test_db"
os.environ["数据库连接url"] = "mongodb://localhost:27019"
os.environ["根目录"]=os.path.dirname(os.path.abspath(__file__))

from app.api import 创建服务器
静态资源目录 = os.path.join(os.environ.get("根目录", os.path.dirname(os.path.abspath(__file__))),  "web")
路由路径 = "/web"
async def main():
    服务器  =await 创建服务器(静态资源目录=静态资源目录,路由路径=路由路径)
    await 服务器.serve()

if __name__ == "__main__":
    # os.environ["数据库名称"] = "密码存储"

    asyncio.run( main())