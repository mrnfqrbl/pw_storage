from datetime import datetime


def 获取当前时间字符串():
    """
    获取当前时间字符串
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def 获取当前时间():
    """
    获取当前时间
    """
    return datetime.now()
