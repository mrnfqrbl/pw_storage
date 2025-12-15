from typing import Dict, Any


def 扁平化字典(原字典: dict, 父路径: str = "", 分隔符: str = ".") -> dict:
    """
    将嵌套字典展开成 {"a.b.c": 值} 格式的扁平字典。

    :param 原字典: 需要展开的字典
    :param 父路径: 当前递归路径（内部使用）
    :param 分隔符: 路径连接符
    :return: 扁平化后的字典
    """

    结果 = {}

    for 键, 值 in 原字典.items():
        # 生成当前路径
        当前路径 = f"{父路径}{分隔符}{键}" if 父路径 else 键

        if isinstance(值, dict):
            # 如果值还是字典 → 递归展开
            子结果 = 扁平化字典(值, 当前路径, 分隔符)
            结果.update(子结果)
        else:
            # 否则写入最终结果
            结果[当前路径] = 值

    return 结果
def 对比字典(字典1: Dict[str, Any], 字典2: Dict[str, Any]) -> Dict[str, str]:
    """
    返回值不同的项，格式为: 键: 旧值->新值
    """
    扁平字典1 = 扁平化字典(字典1)
    扁平字典2 = 扁平化字典(字典2)

    差异 = {}
    所有键 = set(扁平字典1.keys()) | set(扁平字典2.keys())

    for k in 所有键:
        值1 = 扁平字典1.get(k)
        值2 = 扁平字典2.get(k)
        if 值1 != 值2:
            差异[k] = f"{值1} -> {值2}"

    return 差异