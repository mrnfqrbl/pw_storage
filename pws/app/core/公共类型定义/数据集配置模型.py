from dataclasses import dataclass
from datetime import datetime


@dataclass
class 集合配置模型:
    def __init__(self,集合名称:str,最大id:int=0):
        self.集合名称=集合名称
        self.最大id=最大id
        self.更新时间=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.状态:bool=True

