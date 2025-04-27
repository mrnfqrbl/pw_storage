from typing import Any, MutableMapping
from urllib.parse import urlparse

import uvicorn
from fastapi import Request
from starlette.middleware import Middleware
from starlette.types import ASGIApp, Receive, Scope, Send
from app.api.web import web路由,挂载资源
from app.api.api_db import db路由
from app.api.封装api import api类


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

async def main():
    api =await api类.创建api实例()
    # api.add_middleware(CORSAllowAllMiddleware)
    api.include_router(db路由,  prefix="/api")
    api.include_router(web路由)
    挂载资源(api)
    config = uvicorn.Config(api, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()






