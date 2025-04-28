from typing import Any, MutableMapping
from urllib.parse import urlparse

import uvicorn
from fastapi import Request
from starlette.middleware import Middleware
from starlette.types import ASGIApp, Receive, Scope, Send
from app.api.web import web路由, 挂载资源
from app.api.api_db import db路由
from app.api.封装api import api类
from loguru import logger
import logging

# class CORSAllowAllMiddleware:
#     def __init__(self, app: ASGIApp) -> None:
#         self.app = app
#
#     async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
#         if scope["type"] == "http":
#             request = Request(scope, receive=receive)
#             origin = request.headers.get("origin")
#
#             if origin:
#                 parsed_origin = urlparse(origin)
#                 hostname = parsed_origin.hostname
#
#                 if hostname and (hostname == "localhost" or hostname.startswith("192.168.1.")):
#                     async def send_wrapper(message: MutableMapping[str, Any]) -> None:
#                         if message["type"] == "http.response.start":
#                             message["headers"] += [
#                                 (b"access-control-allow-origin", origin.encode("utf-8")),
#                                 (b"access-control-allow-credentials", b"true"),
#                                 (b"access-control-allow-methods", b"*"),
#                                 (b"access-control-allow-headers", b"*"),
#                             ]
#                         await send(message)
#                     await self.app(scope, receive, send_wrapper)
#                     return
#
#         await self.app(scope, receive, send)

async def 创建服务器():
    """
    创建并配置 FastAPI 服务器。
    """

    api = await api类.创建api实例()  # 创建 FastAPI 应用实例
    # api.add_middleware(CORSAllowAllMiddleware)
    api.include_router(db路由, prefix="/api")  # 包含数据库相关的路由
    api.include_router(web路由)  # 包含 Web 相关的路由
    挂载资源(api)  # 挂载静态资源

    # 创建 logging 对象http_logger  传递给服务器但是 http_logger的输出转发到logger
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.error").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.asgi").handlers = [InterceptHandler()]

    配置 = uvicorn.Config(api, host="0.0.0.0", port=8000, log_level="info",log_config=None)  # 配置 Uvicorn 服务器
    服务器 = uvicorn.Server(配置)  # 创建 Uvicorn 服务器实例
    # await server.serve()
    return 服务器

class InterceptHandler(logging.Handler):
    """
    拦截标准 logging 模块的输出，并将其转发到 Loguru。
    """

    def emit(self, record):
        # 根据日志级别将日志消息转发到 Loguru
        try:
            level = logger.level(record.levelname).name

        except ValueError:
            level = record.levelname


        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())
