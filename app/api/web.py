import asyncio

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.api.封装api import api类
import os

# # app = api类.获取api实例()
# loop=asyncio.get_event_loop()
# 任务=loop.create_task(api类.创建api实例())
# app = loop.run_until_complete(任务)
def 挂载资源(app,路径,路由路径):
    if not os.path.exists(路径):
        raise ValueError(f"路径不存在: {路径}")
    print(f"挂载静态资源: {路径}")
    app.mount(路由路径, StaticFiles(directory=路径), name="静态资源")

# 使用 os.path.join 构建相对路径


web路由 = APIRouter()


def 读取文件(文件路径: str) -> str:
    """读取文件内容并返回字符串"""
    try:
        with open(文件路径, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"文件未找到: {文件路径}"
    except Exception as e:
        return f"读取文件出错: {e}"


@web路由.get("/", response_class=HTMLResponse)
async def 根路由(api: api类 = Depends(api类.获取api实例)):
    """根路由，返回 index.html 的内容"""
    模板文件路径 = os.path.join(api.静态资源目录, "index.html")
    html_内容 = 读取文件(模板文件路径)
    return HTMLResponse(content=html_内容)
