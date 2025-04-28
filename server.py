# 主程序入口
import os
import sys
import threading
import signal
import servicemanager
import win32event
import win32service
import win32serviceutil
import time
import asyncio
import logging

from loguru import logger

# 获取当前脚本所在的目录
当前脚本路径 = os.path.dirname(__file__)
# 定义日志目录
日志目录 = os.path.join(当前脚本路径, "logs")
# 移除默认的logger配置
logger.remove()
# 添加INFO级别的日志文件
logger.add(os.path.join(日志目录, "server.log"), level="INFO")
# 添加ERROR级别的日志文件
logger.add(os.path.join(日志目录, "server_error.log"), level="ERROR")


# 定义服务类
class 应用服务(win32serviceutil.ServiceFramework):
    # 服务名称
    _svc_name_ = "pw_s"
    # 服务显示名称
    _svc_display_name_ = "密码存储服务"
    # 服务描述
    _svc_description_ = "提供密码存储服务。"

    def __init__(self, args):
        os.chdir(当前脚本路径)
        logger.info("服务初始化中...")

        win32serviceutil.ServiceFramework.__init__(self, args)
        # 创建停止事件，用于通知服务停止
        self.停止事件 = win32event.CreateEvent(None, 0, 0, None)
        self.线程停止事件 = threading.Event()
        # asyncio 任务
        self.asyncio_任务 = None
        self.服务器 = None  # 保存服务器实例
        self.停止_事件 = asyncio.Event()  # 创建 asyncio.Event
        self.服务器_线程 = None  # 保存服务器线程
        self.事件循环 = None  # 保存事件循环

        # 设置环境变量 (从这里设置，确保服务启动时生效)
        os.environ["数据库名称"] = "test_db"
        os.environ["数据库连接url"] = "mongodb://localhost:27019"

        logger.info("服务初始化完成。")

    # 服务停止处理函数
    def SvcStop(self):
        # 上报服务状态为停止挂起
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        logger.info("服务停止中...")
        # 设置停止事件
        win32event.SetEvent(self.停止事件)
        self.线程停止事件.set()
        if self.事件循环:
            asyncio.run_coroutine_threadsafe(self.停止_事件.set(), self.事件循环)

        # 等待服务器线程结束
        if self.服务器_线程 and self.服务器_线程.is_alive():
            self.服务器_线程.join()

        logger.info("服务已停止。")

    # 服务运行处理函数
    def SvcDoRun(self):
        logger.info("服务启动中...")

        # 启动 asyncio 任务
        def 启动_服务器():
            try:
                asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                self.事件循环 = asyncio.new_event_loop()
                asyncio.set_event_loop(self.事件循环)
                asyncio.set_event_loop(self.事件循环)

                async def 运行():
                    from app.api import 创建服务器

                    try:
                        self.服务器 = await 创建服务器()

                        await self.服务器.serve()
                    except Exception as e:
                        logger.error(f"服务器运行出错: {e}")
                    finally:
                        logger.info("服务器已停止运行。")

                self.事件循环.run_until_complete(运行())

            except Exception as e:
                logger.error(f"服务器运行出错: {e}")
            finally:
                logger.info("服务器已停止运行。")
                # 确保服务状态被设置为停止
                self.ReportServiceStatus(win32service.SERVICE_STOPPED)
                # 设置停止事件，通知主线程
                win32event.SetEvent(self.停止事件)
                if self.事件循环:
                    try:
                        tasks = asyncio.all_tasks(self.事件循环)
                        for task in tasks:
                            task.cancel()
                        self.事件循环.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
                    except asyncio.CancelledError:
                        pass
                    finally:
                        self.事件循环.close()

        # 创建并启动线程
        self.服务器_线程 = threading.Thread(target=启动_服务器, daemon=True)
        self.服务器_线程.start()

        # 主线程等待停止信号
        win32event.WaitForSingleObject(self.停止事件, win32event.INFINITE)
        logger.info("服务运行结束。")


# 主程序入口
if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(应用服务)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(应用服务)
