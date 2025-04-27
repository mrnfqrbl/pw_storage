import requests
import json

# 基础 URL，替换成你的 FastAPI 应用的实际地址
BASE_URL = "http://127.0.0.1:8000"  # 假设你的应用运行在本地 8000 端口
合集名称="test_collection"
# 1. 测试 根路由
def 测试根路由():
    response = requests.get(BASE_URL + "/")
    print("测试根路由:")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    assert response.status_code == 200

# 2. 测试 查询条目
def 测试查询条目():
    url = BASE_URL + "/查询条目"
    params = {"合集名称": 合集名称}  # 替换成你的实际合集名称
    data = {"文档内容.名称":"123"}  # 替换成你的实际查询条件
    response = requests.post(url, params=params, data=json.dumps(data))
    print("\n测试查询条目:")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    assert response.status_code == 200

# 3. 测试 查询历史记录
def 测试查询历史记录():
    url = BASE_URL + "/查询历史记录"
    params = {"合集名称": 合集名称, "uuid": "a964560d-adf7-4971-81e7-d2b98b2be837"}  # 替换成你的实际合集名称和 UUID
    response = requests.get(url, params=params)
    print("\n测试查询历史记录:")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    assert response.status_code == 200

# 4. 测试 增加条目
def 测试增加条目():
    url = BASE_URL + "/增加条目"
    params = {"合集名称": 合集名称}  # 替换成你的实际合集名称
    data = {"名称": "121111111113", "密码": "30"}  # 替换成你的实际新增数据
    response = requests.post(url, params=params, data=json.dumps(data))
    print("\n测试增加条目:")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    assert response.status_code == 200

# 5. 测试 修改条目
def 测试修改条目():
    url = BASE_URL + "/修改条目"
    params = {"合集名称": 合集名称}  # 替换成你的实际合集名称
    data = {"81531fdd-c16e-4a74-b4f8-5169071e4368": {"名称": "111114545645611修改后的值1"}}  # 替换成你的实际 UUID 和修改内容
    response = requests.put(url, params=params, data=json.dumps(data))
    print("\n测试修改条目:")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    assert response.status_code == 200

# 6. 测试 删除条目
def 测试删除条目():
    url = BASE_URL + "/删除条目"
    params = {"合集名称": 合集名称, "uuid": "d62cea9a-65d2-4fbd-bad2-e7c16bd55714"}  # 替换成你的实际合集名称和 UUID
    response = requests.delete(url, params=params)
    print("\n测试删除条目:")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    assert response.status_code == 200

# 运行所有测试
if __name__ == "__main__":
    # 测试根路由()
    # 测试查询条目()
    # 测试查询历史记录()
    # 测试增加条目()
    测试修改条目()
    测试删除条目()

    print("\n所有测试完成!")
