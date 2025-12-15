# 文件路径：bus_embedded_server.py
from .请求模型 import 请求对象, 响应对象, WebSocket对象
from .ws import WebSocket工具
import socket
import threading
from pws.app.core.公共类型定义.事件总线模型 import I事件总线 as 事件总线

class 总线内嵌http服务器:

    def __init__(self, 主机="127.0.0.1", 端口=8080, 框架=None, 总线: 事件总线=None):
        self.主机 = 主机
        self.端口 = 端口
        self.框架 = 框架
        self.总线 = 总线
        if not 框架 and not 总线:
            raise ValueError("未注入框架也未提供总线，服务器无法工作")

    def 启动(self):
        """启动TCP监听并循环处理连接"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as 服务端:
            服务端.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            服务端.bind((self.主机, self.端口))
            服务端.listen(5)

            print(f"🔵【服务器层】HTTP/WS服务器已启动: http://{self.主机}:{self.端口}")

            while True:
                客户端, 地址 = 服务端.accept()
                print(f"🔵【服务器层】收到客户端连接: {地址}")
                threading.Thread(target=self.处理连接, args=(客户端, 地址)).start()

    def 处理连接(self, 客户端, 地址):
        """接收请求、解析、调用框架或总线、发送响应"""
        with 客户端:
            数据 = 客户端.recv(4096)
            if not 数据:
                print("🔵【服务器层】空数据包，关闭连接")
                return

            报文 = 数据.decode("utf-8", errors="ignore")
            行们 = 报文.split("\r\n")
            请求行 = 行们[0]
            try:
                方法, 路径, 协议 = 请求行.split(" ")
            except ValueError:
                print("🔵【服务器层】请求行解析失败，返回400")
                客户端.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
                return

            # 解析头部
            头部 = {}
            i = 1
            while i < len(行们) and 行们[i] != "":
                if ":" in 行们[i]:
                    k, v = 行们[i].split(":", 1)
                    头部[k.strip()] = v.strip()
                i += 1

            # 请求体
            请求体 = "\r\n".join(行们[i+1:])

            # 检测是否为WebSocket升级请求
            是WebSocket = (头部.get('Upgrade', '').lower() == 'websocket' and
                           头部.get('Connection', '').lower() == 'upgrade')
            请求 = 请求对象(方法, 路径, 头部, 请求体, 是WebSocket=是WebSocket)
            print(f"🔵【服务器层】构建请求对象: 方法={方法}, 路径={路径}, 是WebSocket={是WebSocket}")

            # 处理WebSocket握手
            if 是WebSocket:
                self.处理websocket连接(客户端, 请求, 地址)
                return

            # 处理普通HTTP请求
            if self.框架:
                响应 = self.框架(请求)
            else:
                返回事件 = self.总线.发布("http请求", 事件数据={"请求": 请求})
                if 返回事件.事件返回:
                    响应 = list(返回事件.事件返回.values())[0].数据
                if not isinstance(响应, 响应对象):
                    响应 = 响应对象(500, 内容="总线处理错误")

            # 构建HTTP响应报文
            响应行 = f"HTTP/1.1 {响应.状态码} OK\r\n"
            响应头 = "".join([f"{k}: {v}\r\n" for k, v in 响应.头部.items()])
            响应体 = 响应.内容
            完整响应 = (响应行 + 响应头 + "\r\n" + 响应体).encode("utf-8")

            客户端.sendall(完整响应)
            print(f"🔵【服务器层】请求处理完毕，已发送响应，长度={len(响应体)}\n")

    def 处理websocket连接(self, 客户端, 请求, 地址):
        """新增：处理WebSocket连接生命周期"""
        # 处理握手
        if self.框架:
            响应 = self.框架(请求)
        else:
            返回事件 = self.总线.发布("http请求", 事件数据={"请求": 请求})
            响应 = list(返回事件.事件返回.values())[0].数据 if 返回事件.事件返回 else None

        if not 响应 or 响应.状态码 != 101:
            客户端.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            return

        # 发送握手响应
        响应行 = f"HTTP/1.1 101 Switching Protocols\r\n"
        响应头 = "".join([f"{k}: {v}\r\n" for k, v in 响应.头部.items()])
        客户端.sendall((响应行 + 响应头 + "\r\n").encode("utf-8"))

        # 创建WebSocket对象
        ws = WebSocket对象(客户端, 请求.路径)
        print(f"🔵【服务器层】WebSocket握手成功: {地址}, 路径={请求.路径}")

        # 持续处理WebSocket消息
        try:
            while ws.已连接:
                数据 = 客户端.recv(4096)
                if not 数据:
                    break

                opcode,  payload = WebSocket工具.解析帧(数据)
                if  opcode == 8:  # 关闭帧
                    ws.关闭()
                    break

                # 发布消息事件
                if self.总线:
                    self.总线.发布("websocket消息", 事件数据={
                        'websocket': ws,
                        '消息':  payload.decode('utf-8') if  opcode == 1 else  payload,
                        'opcode':  opcode
                    })
                elif self.框架:
                    self.框架.处理websocket消息({
                        'websocket': ws,
                        '消息':  payload.decode('utf-8') if  opcode == 1 else  payload,
                        'opcode':  opcode
                    }, None)

        except Exception as e:
            print(f"🔵【服务器层】WebSocket错误: {e}")
        finally:
            ws.关闭()
            print(f"🔵【服务器层】WebSocket连接关闭: {地址}")