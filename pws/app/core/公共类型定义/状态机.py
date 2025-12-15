from typing import Literal


class 状态机:
    成功="成功"
    失败="失败"
    def __init__(self,初始状态:Literal["成功", "失败"]=失败):

        self.前:Literal["成功", "失败"]=初始状态

        self.中:Literal["成功", "失败"]=初始状态

        self.后:Literal["成功", "失败"]=初始状态
