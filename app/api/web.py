import asyncio

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.api.封装api import api类
import os

# # app = api类.获取api实例()
# loop=asyncio.get_event_loop()
# 任务=loop.create_task(api类.创建api实例())
# app = loop.run_until_complete(任务)
def 挂载资源(app):
    app.mount("/web", StaticFiles(directory="web"), name="静态资源")
当前文件路径 = os.path.abspath(__file__)

# 获取当前脚本所在的目录
当前目录 = os.path.dirname(当前文件路径)

# 使用 os.path.join 构建相对路径
相对路径 = os.path.join(当前目录, "../../")

# 使用 os.path.abspath 获取相对路径的绝对路径
根目录 = os.path.abspath(相对路径)
网页目录 = os.path.join(根目录, "web")
print(f"根目录: {根目录}")
print(f"网页目录: {网页目录}")

web路由 = APIRouter()

# app.mount("/web", StaticFiles(directory="web"), name="静态资源")

# @web路由.get("/web/{file_path:path}")
# async def 获取_静态文件(file_path: str, request: Request):
#     """
#     动态返回 /web 路径下的静态文件
#     :param file_path:  /web 之后的路径，例如 js/api.js
#     :param request: 请求对象
#     :return: 静态文件内容
#     """
#     文件路径 = os.path.join(网页目录, file_path)
#     if not os.path.exists(文件路径):
#         raise HTTPException(status_code=404, detail=f"文件未找到: {文件路径}")
#
#     文件内容 = 读取文件(文件路径)
#
#     # 根据文件扩展名设置 Content-Type
#     if 文件路径.endswith(".js"):
#         media_type = "application/javascript"
#     elif 文件路径.endswith(".css"):
#         media_type = "text/css"
#     elif 文件路径.endswith(".html"):
#         media_type = "text/html"
#     else:
#         media_type = "text/plain"  # 默认
#
#     return PlainTextResponse(content=文件内容, media_type=media_type)
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
async def 根路由():
    """根路由，返回 index.html 的内容"""
    模板文件路径 = os.path.join(网页目录, "index.html")
    html_内容 = 读取文件(模板文件路径)
    return HTMLResponse(content=html_内容)
