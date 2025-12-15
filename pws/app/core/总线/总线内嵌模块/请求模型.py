from pws.app.core.总线.总线内嵌模块.ws import WebSocket工具


class 请求对象():
    """封装解析后的HTTP请求数据."""
    def __init__(self, 方法, 路径, 头部, 请求体, 查询参数=None, 是WebSocket=False):
        if 查询参数 is None:
            查询参数 = {}
        self.方法 = 方法
        self.路径 = 路径
        self.查询参数 = 查询参数
        self.头部 = 头部
        self.请求体 = 请求体
        self.是WebSocket = 是WebSocket  # 新增标记是否为WebSocket请求


class 响应对象:
    """框架返回的响应对象，由服务器转换为HTTP字节流."""
    def __init__(self, 状态码=200, 头部=None, 内容=""):
        self.状态码 = 状态码
        self.头部 = 头部 or {"Content-Type": "text/plain; charset=utf-8"}
        self.内容 = 内容


class WebSocket对象:
    """WebSocket连接对象，用于帧通信"""
    def __init__(self, 客户端_socket, 路径):
        self.客户端_socket = 客户端_socket
        self.路径 = 路径
        self.已连接 = True

    def 发送消息(self, 内容, 是文本=True):
        """发送消息到客户端"""
        if not self.已连接:
            return False
        opcode = 1 if 是文本 else 2
        try:
            帧 = WebSocket工具.构建帧(内容.encode('utf-8') if 是文本 else 内容,  opcode)
            self.客户端_socket.sendall(帧)
            return True
        except:
            self.已连接 = False
            return False

    def 关闭(self):
        """关闭WebSocket连接"""
        if self.已连接:
            try:
                # 发送关闭帧
                self.客户端_socket.sendall(WebSocket工具.构建帧(b'', 8))
            except:
                pass
            self.已连接 = False
            self.客户端_socket.close()