


import asyncio
import websockets

async def 发送消息():
    # 连接到 WebSocket 服务器
    async with websockets.connect('ws://127.0.0.1:8080/ws') as websocket:
        print("成功连接到 WebSocket 服务器")

        # 发送消息
        消息 = "你好，WebSocket 服务器！"
        await websocket.send(消息)
        print(f"发送消息: {消息}")

        # 接收服务器的回应
        响应 = await websocket.recv()
        print(f"接收到服务器消息: {响应}")

# 运行异步事件循环
asyncio.run(发送消息())