import inspect
import threading
import asyncio
from collections import defaultdict
from typing import Callable, List, Dict, Any
from pws.pkg.日志.日志事件生成工具 import 日志事件生成器 as 日志事件生成器类
# from pws.pkg.日志.日志事件生成工具 import _

class 事件总线:
    def __init__(self):
        self._订阅表: Dict[str, List[tuple[str, Callable]]] = defaultdict(list)
        self._锁 = threading.Lock()
        self.日志事件生成器=日志事件生成器类()


    async def _执行异步回调(self, fn, 数据, 订阅者):
        try:
            await fn(数据)
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

    def 发布(self, 事件名: str, 事件数据: Any):
        # if 事件名=="日志":
        #     调用帧=inspect.currentframe().f_back
        #     日志事件=self.日志事件生成器._生成事件(调用帧,事件数据)
        #

        with self._锁:
            订阅者列表 = self._订阅表[事件名]
            if not 订阅者列表:
                return




            订阅者列表 = self._订阅表[事件名]
        for 订阅者, 处理函数 in 订阅者列表:
            处理函数(事件数据)
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
    def 发布日志(self, 级别: str, 消息: str, ):
        调用帧=inspect.currentframe().f_back
        日志事件=self.日志事件生成器._生成事件(级别,消息,调用帧)
        self.发布("日志",日志事件)


