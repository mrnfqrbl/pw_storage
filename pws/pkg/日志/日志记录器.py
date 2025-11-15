# 文件路径: src/utils/custom_logger.py
# 中文说明：
# 本模块提供一个独立日志模块，支持：
# 1. 可选依赖 Python logging（可替换为自定义处理器）
# 2. 精细控制日志级别（Logger/Handler级别独立控制）
# 3. 多 Handler 输出（文件/控制台/网络/自定义）
# 4. 自动注入包名/函数名/行号
# 5. 彩色控制台输出
# 6. 可简易扩展新 Handler 或输出方式

import os
import inspect
from typing import Dict, Optional, Callable

try:
    import logging
    from colorama import init as _colorama_init, Fore, Style
    _colorama_init()
    _USE_LOGGING = True
except ImportError:
    _USE_LOGGING = False

_USE_LOGGING = False
# ----------------------------------------------------------------------
# 工具函数
# ----------------------------------------------------------------------

def _获取调用信息(depth: int = 3) -> Dict[str, object]:
    stack = inspect.stack()
    if len(stack) <= depth:
        frame = stack[-1]
    else:
        frame = stack[depth]
    module = inspect.getmodule(frame.frame)
    包名 = module.__name__ if module else frame.filename
    return {
        '包名': 包名,
        '函数名': frame.function,
        '行号': frame.lineno
    }

# ----------------------------------------------------------------------
# 日志模块核心
# ----------------------------------------------------------------------

class BaseLogger:
    def debug(self, msg: str, **kwargs):
        raise NotImplementedError
    def info(self, msg: str, **kwargs):
        raise NotImplementedError
    def warning(self, msg: str, **kwargs):
        raise NotImplementedError
    def error(self, msg: str, **kwargs):
        raise NotImplementedError
    def critical(self, msg: str, **kwargs):
        raise NotImplementedError

# ----------------------------------------------------------------------
# Logging实现
# ----------------------------------------------------------------------

if _USE_LOGGING:
    class 中文格式化器(logging.Formatter):
        def __init__(self, fmt=None, 彩色: bool = False):
            self.彩色 = 彩色
            if fmt is None:
                fmt = '%(asctime)s %(levelname)s [%(包名)s:%(函数名)s:%(行号)s] %(message)s'
            super().__init__(fmt)

        def format(self, record):
            record.包名 = getattr(record, '包名', record.module)
            record.函数名 = getattr(record, '函数名', record.funcName)
            record.行号 = getattr(record, '行号', record.lineno)
            text = super().format(record)
            if not self.彩色:
                return text
            if record.levelno >= logging.ERROR:
                return Fore.RED + text + Style.RESET_ALL
            elif record.levelno >= logging.WARNING:
                return Fore.YELLOW + text + Style.RESET_ALL
            elif record.levelno >= logging.INFO:
                return Fore.GREEN + text + Style.RESET_ALL
            else:
                return Fore.CYAN + text + Style.RESET_ALL

    class CustomLogger(BaseLogger):
        def __init__(self, name: str, level: int = logging.INFO, log_dir: str = 'logs', console: bool = True):
            os.makedirs(log_dir, exist_ok=True)
            self.logger = logging.getLogger(name)
            self.logger.setLevel(level)
            self.logger.propagate = False

            if not self.logger.handlers:
                # 文件 Handler
                fh = logging.FileHandler(os.path.join(log_dir, f'{name}.log'), encoding='utf-8')
                fh.setLevel(level)
                fh.setFormatter(中文格式化器(彩色=False))
                self.logger.addHandler(fh)
                # 控制台 Handler
                if console:
                    sh = logging.StreamHandler()
                    sh.setLevel(level)
                    sh.setFormatter(中文格式化器(彩色=True))
                    self.logger.addHandler(sh)

        def _process(self, kwargs):
            调用 = _获取调用信息(depth=4)
            extra = kwargs.get('extra', {}) or {}
            extra.setdefault('包名', 调用['包名'])
            extra.setdefault('函数名', 调用['函数名'])
            extra.setdefault('行号', 调用['行号'])
            kwargs['extra'] = extra
            return kwargs

        def debug(self, msg, **kwargs):
            self.logger.debug(msg, **self._process(kwargs))
        def info(self, msg, **kwargs):
            self.logger.info(msg, **self._process(kwargs))
        def warning(self, msg, **kwargs):
            self.logger.warning(msg, **self._process(kwargs))
        def error(self, msg, **kwargs):
            self.logger.error(msg, **self._process(kwargs))
        def critical(self, msg, **kwargs):
            self.logger.critical(msg, **self._process(kwargs))

# ----------------------------------------------------------------------
# 简易管理器
# ----------------------------------------------------------------------

class 日志管理器:
    def __init__(self, log_dir='logs', use_logging=True):
        self.log_dir = log_dir
        self._缓存: Dict[str, BaseLogger] = {}
        self._use_logging = use_logging and _USE_LOGGING

    def 获取日志器(self, 名称: str, level='INFO', console=True) -> BaseLogger:
        key = f'{名称}:{level}:{console}'
        if key in self._缓存:
            return self._缓存[key]

        if self._use_logging:
            import logging
            lvl = getattr(logging, level.upper(), logging.INFO) if isinstance(level, str) else int(level)
            logger = CustomLogger(名称, lvl, log_dir=self.log_dir, console=console)
        else:
            # 自定义简单 Logger，不依赖 logging
            logger = SimpleLogger(名称)
        self._缓存[key] = logger
        return logger

# ----------------------------------------------------------------------
# 简易扩展接口示例
# ----------------------------------------------------------------------

class SimpleLogger(BaseLogger):
    def __init__(self, name: str):
        self.name = name

    def _输出(self, level: str, msg: str):
        调用 = _获取调用信息(depth=4)
        print(f'[{level}] {调用["包名"]}:{调用["函数名"]}:{调用["行号"]} {msg}')

    def debug(self, msg, **kwargs): self._输出('DEBUG', msg)
    def info(self, msg, **kwargs): self._输出('INFO', msg)
    def warning(self, msg, **kwargs): self._输出('WARNING', msg)
    def error(self, msg, **kwargs): self._输出('ERROR', msg)
    def critical(self, msg, **kwargs): self._输出('CRITICAL', msg)

# ----------------------------------------------------------------------
# 全局管理器
# ----------------------------------------------------------------------

全局日志管理器 = 日志管理器(log_dir='logs', use_logging=True)

获取日志器 = 全局日志管理器.获取日志器

# ----------------------------------------------------------------------
# 使用示例
# ----------------------------------------------------------------------

if __name__ == '__main__':
    日志 = 获取日志器('示例模块', level='DEBUG', console=True)
    日志.debug('调试信息')
    日志.info('普通信息')
    日志.warning('警告信息')
    日志.error('错误信息')
    日志.critical('严重错误')