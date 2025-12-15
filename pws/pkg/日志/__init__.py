import datetime
import logging
import os

from ...app.core.公共类型定义.事件总线模型 import I事件总线
from ...app.core.公共类型定义.事件对象模型 import 总线通用事件模型
from loguru import logger
class 日志模块:
    def __init__(self,事件总线实例:I事件总线):
        self.事件总线实例=事件总线实例
        self.等级映射 = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "warn": logging.WARNING,  # 兼容 warn
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }
        self.事件总线实例.订阅("日志","日志模块",self.输出日志)
        self.事件总线实例.订阅("记录事件","记录模块",self.事件记录)
    def 事件记录(self, 总线事件:总线通用事件模型):
        """
        事件日志输出到文件
        """
        日志目录 = r"D:\xm\pw_storage\pws\logs"
        # 如果目录不存在则创建
        if not os.path.exists(日志目录):
            os.makedirs(日志目录)

        # 时间格式用于文件名，避免非法字符
        事件时间 = datetime.datetime.now().strftime("%Y-%m-%d")
        日志文件名 = f"{事件时间}.log"
        日志文件路径 = os.path.join(日志目录, 日志文件名)

        # 使用追加模式写日志
        with open(日志文件路径, "a", encoding="utf-8") as f:
            f.write(f"{总线事件.转字典()}\n")
    def 输出日志(self,日志事件):
        """
        事件日志输出
        自动处理等级为字符串（小写或大写）情况
        """
        # 获取事件等级，如果是字符串，则转换为整数
        等级 = getattr(logging, 日志事件.等级.upper(), None) if isinstance(日志事件.等级, str) else 日志事件.等级
        if 等级 is None:
            # 尝试从映射表转换
            等级 = self.等级映射.get(日志事件.等级.lower(), logging.INFO)  # 默认 INFO

        # 输出日志
        if 等级<=logging.DEBUG:
            logger.debug(f"{日志事件.时间}|{日志事件.等级}|{日志事件.包名} {日志事件.函数名} {日志事件.行号}|{日志事件.消息}")
        elif 等级<=logging.INFO:
            logger.info(f"{日志事件.时间}|{日志事件.等级}|{日志事件.包名} {日志事件.函数名} {日志事件.行号}|{日志事件.消息}")
        elif 等级<=logging.WARNING:
            logger.warning(f"{日志事件.时间}|{日志事件.等级}|{日志事件.包名} {日志事件.函数名} {日志事件.行号}|{日志事件.消息}")
        elif 等级<=logging.ERROR:
            logger.error(f"{日志事件.时间}|{日志事件.等级}|{日志事件.包名} {日志事件.函数名} {日志事件.行号}|{日志事件.消息}")
        elif 等级<=logging.CRITICAL:
            logger.critical(f"{日志事件.时间}|{日志事件.等级}|{日志事件.包名} {日志事件.函数名} {日志事件.行号}|{日志事件.消息}")
        else:
             logger.log(等级,f"{日志事件.时间}|{日志事件.等级}|{日志事件.包名} {日志事件.函数名} {日志事件.行号}|{日志事件.消息}")

