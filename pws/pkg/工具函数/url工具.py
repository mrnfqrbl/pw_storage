


def url编码(s:str):
    """
    自实现 URL 编码
    将非字母数字字符转换为 %XX 形式，空格转为 +
    """
    result = []
    for c in s:
        # 安全字符不用编码
        if c.isalnum() or c in "-_.~":
            result.append(c)
        elif c == " ":
            result.append("+")  # 空格使用 + 代替
        else:
            # 转为 %XX 十六进制形式
            result.append("%{:02X}".format(ord(c)))
    return "".join(result)




def url解码(s:str):
    result = []
    i = 0
    length = len(s)
    while i < length:
        if s[i] == "%":
            # 取后面两个字符作为十六进制
            hex_value = s[i+1:i+3]
            try:
                result.append(chr(int(hex_value, 16)))
                i += 3
            except ValueError:
                # 如果不是有效的十六进制就原样保留
                result.append("%")
                i += 1
        elif s[i] == "+":
            result.append(" ")
            i += 1
        else:
            result.append(s[i])
            i += 1
    return "".join(result)


class url解析模型():



    def url解析(self):
        pass