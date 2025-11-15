import time

from pws.app.core.总线.事件总线 import 事件总线 as 事件总线类
from pws.app.core.总线.事件类型模型 import 日志事件
# 当前时间=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
from loguru import logger
# print(当前时间)
事件总线=事件总线类()
def 输出日志(事件:日志事件):

    logger.log(事件.等级, f"{事件.时间}|{事件.等级}|{事件.包名} {事件.函数名} {事件.行号}|{事件.消息}")

事件总线.订阅("日志","日志模块",输出日志)

def 测试():
    事件总线.发布日志("INFO", "这是一条INFO日志")

测试()



