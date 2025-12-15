import datetime
import inspect
import threading
import asyncio
from collections import defaultdict
from typing import Callable, List, Dict, Any
from .工具函数类 import 总线工具函数
from pws.app.core.公共类型定义.事件对象模型 import 总线通用事件模型
from pws.app.core.总线.日志事件生成工具 import 日志事件生成器 as 日志事件生成器类
from pws.app.core.总线.总线内嵌模块.http框架 import 总线内嵌http框架
from pws.app.core.总线.总线内嵌模块.http服务器 import 总线内嵌http服务器


class 事件总线:
    def __init__(self):
        self._订阅表: Dict[str, List[tuple[str, Callable]]] = defaultdict(list)
        self._锁 = threading.Lock()
        self.日志事件生成器=日志事件生成器类()
        self.总线工具函数=总线工具函数
        self.总线内嵌http框架=总线内嵌http框架(总线=self)
        self.总线内嵌http服务器=总线内嵌http服务器



    async def _执行异步回调(self, fn, 订阅者,*args, **kwargs):
        try:
            await fn(*args, **kwargs)
        except Exception as e:
            print(f"异步事件回调异常: {订阅者} -> {e}")
    def 订阅(self, 事件名: str, 订阅者: str, 处理函数: Callable):
        with self._锁:
            self._订阅表[事件名].append((订阅者, 处理函数))
    def 取消订阅(self, 事件名: str, 订阅者: str):
        with self._锁:
            self._订阅表[事件名] = [
                (sub, fn) for sub, fn in self._订阅表[事件名] if sub != 订阅者
            ]

    def 发布(self, 事件名: str, 事件数据: Any) :


        事件=总线通用事件模型(事件名=事件名)
        事件.事件提交时间=self.总线工具函数.获取当前时间()

        with self._锁:
            if not self._订阅表[事件名]:
                # raise ValueError(f"事件名 {事件名} 没有订阅者")
                self.发布日志(级别="warning",消息=f"事件名 {事件名} 没有订阅者")
                return 事件


            订阅者映射  = self._订阅表[事件名]
            事件.重新初始化(订阅者列表=[订阅者 for 订阅者, _ in 订阅者映射],事件数据=事件数据)




        for 订阅者, 处理函数 in 订阅者映射 :
            #如果处理函数是异步函数，使用异步执行
            if asyncio.iscoroutinefunction(处理函数):
                loop=asyncio.get_event_loop()
                loop.create_task(self._执行异步回调(fn=处理函数,订阅者=订阅者,数据=事件数据,事件=事件))
            处理函数(数据=事件数据,事件=事件)


            # self.发布日志(级别="调试",消息=f"{操作结果.生成通用事件消息()}")

        # 事件.生成耗时()

        事件.事件结束时间=self.总线工具函数.获取当前时间()
        事件.时间总耗时=(事件.事件结束时间-事件.事件提交时间).total_seconds()
        self.发布事件记录(事件)

        return 事件
    def 发布异步(self, 事件名: str, 事件数据: Any):
        with self._锁:
            订阅者列表 = self._订阅表[事件名]

            loop = asyncio.get_event_loop()
            for 订阅者, 处理函数 in 订阅者列表:
                if asyncio.iscoroutinefunction(处理函数):
                    loop.create_task(self._执行异步回调(处理函数, 事件数据, 订阅者))
                else:
                    # 同步函数也可以用线程池异步执行
                    loop.run_in_executor(None, 处理函数, 事件数据)








    #总线日志区域
    def 发布日志(self, 级别: str, 消息: str, ):
        调用帧=inspect.currentframe().f_back
        日志事件=self.日志事件生成器._生成事件(级别,消息,调用帧)
        订阅者映射 = self._订阅表["日志"]
        for 订阅者, 处理函数 in 订阅者映射:
            处理函数(日志事件)
    def 发布事件记录(self,事件:总线通用事件模型):
        订阅者映射 = self._订阅表["记录事件"]
        for 订阅者, 处理函数 in 订阅者映射:
            处理函数(事件)

    def 获取订阅者列表(self, 事件名: str) -> List[str]:
        with self._锁:
            return [订阅者 for 订阅者, _ in self._订阅表[事件名]]

    def 获取所有事件名(self) -> List[str]:
        with self._锁:
            return list(self._订阅表.keys())
