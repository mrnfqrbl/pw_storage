import base64
import hashlib

class WebSocket工具:
    @staticmethod
    def 生成握手响应密钥(客户端密钥):
        """根据WebSocket规范生成握手响应密钥"""
        GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        合并字符串 = (客户端密钥 + GUID).encode('utf-8')
        哈希值 = hashlib.sha1(合并字符串).digest()
        return base64.b64encode(哈希值).decode('utf-8')

    @staticmethod
    def 解析帧(数据):
        """解析WebSocket帧，返回 opcode 和 payload"""
        if not 数据:
            return None, None

        第一个字节 = 数据[0]
        opcode = 第一个字节 & 0x0F  # 操作码：1-文本，2-二进制，8-关闭
        第二个字节 = 数据[1]
        掩码标志 = (第二个字节 & 0x80) >> 7
        payload长度 = 第二个字节 & 0x7F

        偏移 = 2
        if payload长度 == 126:
            payload长度 = (数据[2] << 8) | 数据[3]
            偏移 += 2
        elif payload长度 == 127:
            payload长度 = 0
            for i in range(2, 10):
                payload长度 = (payload长度 << 8) | 数据[i]
            偏移 += 8

        掩码 = 数据[偏移:偏移+4] if 掩码标志 else None
        偏移 += 4 if 掩码标志 else 0

        payload = 数据[偏移:偏移+payload长度]

        # 应用掩码
        if 掩码:
            解码后 = []
            for i in range(len(payload)):
                解码后.append(payload[i] ^ 掩码[i % 4])
            payload = bytes(解码后)

        return opcode, payload

    @staticmethod
    def 构建帧(数据, opcode=1):
        """构建WebSocket帧，默认文本类型"""
        帧 = bytearray()
        帧.append(0x80 | opcode)  # FIN=1 + opcode

        长度 = len(数据)
        if 长度 <= 125:
            帧.append(长度)
        elif 长度 <= 65535:
            帧.append(126)
            帧.append((长度 >> 8) & 0xFF)
            帧.append(长度 & 0xFF)
        else:
            帧.append(127)
            for i in range(7, -1, -1):
                帧.append((长度 >> (8 * i)) & 0xFF)

        帧.extend(数据)
        return 帧
