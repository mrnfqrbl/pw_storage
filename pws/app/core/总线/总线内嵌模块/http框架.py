# 文件路径：bus_compatible_framework.py
import obj2dict

from pws.app.core.公共类型定义.事件总线模型 import I事件总线 as 事件总线
from pws.app.core.公共类型定义.事件对象模型 import 总线通用事件模型
from .请求模型 import 请求对象, 响应对象, WebSocket对象
from .ws import WebSocket工具

class 总线内嵌http框架:

    def __init__(self, 总线:事件总线=None):
        self.路由表 = {}
        self.websocket路由表 = {}  # 新增WebSocket路由表
        self.注册的订阅者名称 = "总线内嵌http框架"
        self.总线 = 总线
        self.总线.订阅(事件名="http请求", 订阅者=self.注册的订阅者名称, 处理函数=self.处理总线调用)
        self.总线.订阅(事件名="websocket消息", 订阅者=self.注册的订阅者名称, 处理函数=self.处理websocket消息)
        self.响应对象 = 响应对象

    def 路由(self, 路径):
        """装饰器：注册HTTP路由"""
        def 装饰器(函数):
            print(f"🟠【框架层】注册路由: 路径 = {路径}, 处理函数 = {函数.__name__}")
            self.路由表[路径] = 函数
            return 函数
        return 装饰器

    def websocket路由(self, 路径):
        """新增：装饰器注册WebSocket路由"""
        def 装饰器(函数):
            print(f"🟠【框架层】注册WebSocket路由: 路径 = {路径}, 处理函数 = {函数.__name__}")
            self.websocket路由表[路径] = 函数
            return 函数
        return 装饰器

    def __call__(self, 请求: 请求对象) -> 响应对象:
        """原始调用入口（同步模式）"""
        return self.处理请求(请求)

    def 处理请求(self, 请求: 请求对象) -> 响应对象:
        """统一请求处理逻辑，适配总线和直接调用"""
        print(f"🟠【框架层】收到请求: 方法={请求.方法}, 路径={请求.路径}, 是否WebSocket={请求.是WebSocket}")

        if 请求.是WebSocket:
            # WebSocket握手请求处理
            处理函数 = self.websocket路由表.get(请求.路径)
            if 处理函数 is None:
                return 响应对象(404, 内容="404 WebSocket路由未找到")

            # 生成握手响应
            客户端密钥 = 请求.头部.get('Sec-WebSocket-Key')
            响应密钥 = WebSocket工具.生成握手响应密钥(客户端密钥)
            头部 = {
                'Upgrade': 'websocket',
                'Connection': 'Upgrade',
                'Sec-WebSocket-Accept': 响应密钥
            }
            return 响应对象(101, 头部=头部)

        # 普通HTTP请求处理
        处理函数 = self.路由表.get(请求.路径)
        if 处理函数 is None:
            print("🟠【框架层】未找到对应路由 -> 返回404")
            return 响应对象(404, 内容="404 未找到")

        print(f"🟠【框架层】匹配到路由 -> 调用函数 {处理函数.__name__}")
        响应 = 处理函数(请求)
        print(f"🟠【框架层】处理函数返回响应对象: 状态码={响应.状态码}")
        return 响应

    def 处理总线调用(self, 数据: dict, 事件: 总线通用事件模型) -> 响应对象:
        """处理来自事件总线的调用"""
        请求 = 事件.事件数据.get("请求")
        返回 = 事件.事件返回.get(self.注册的订阅者名称)
        if not isinstance(请求, 请求对象):
            print("🟠【框架层】无效请求对象 -> 返回400")
            返回.数据 = 响应对象(400, 内容="400 无效请求")
            返回.状态 = 返回.成功
            return

        返回.数据 = self.处理请求(请求)
        返回.状态 = 返回.成功

    def 处理websocket消息(self, 数据: dict, 事件: 总线通用事件模型):
        """新增：处理WebSocket消息"""
        ws = 数据.get('websocket')
        消息 = 数据.get('消息')
        opcode = 数据.get('opcode')

        if opcode == 8:  # 关闭帧
            ws.关闭()
            return

        处理函数 = self.websocket路由表.get(ws.路径)
        if 处理函数:
            数据=type('数据', (obj2dict.可序列化基类,), {
                'websocket': ws,
                '消息': 消息,
                'opcode': opcode
            })
            处理函数(数据)