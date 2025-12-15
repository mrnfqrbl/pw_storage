class 请求对象:
    """封装解析后的HTTP请求数据."""
    def __init__(self, 方法, 路径, 头部, 请求体):
        self.方法 = 方法
        self.路径 = 路径
        self.头部 = 头部
        self.请求体 = 请求体


# ============================
#  简易【响应对象】
# ============================
class 响应对象:
    """框架返回的响应对象，由服务器转换为HTTP字节流."""
    def __init__(self, 状态码=200, 头部=None, 内容=""):
        self.状态码 = 状态码
        self.头部 = 头部 or {"Content-Type": "text/plain; charset=utf-8"}
        self.内容 = 内容





class http请求对象模型:
    pass



class http响应对象模型:
    pass




