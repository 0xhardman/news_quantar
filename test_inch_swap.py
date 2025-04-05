#!/usr/bin/env python3
import os
import json
import asyncio
import subprocess
from time import sleep

# 测试1inch Swap功能
async def test_inch_swap():
    # 启动MCP服务器
    print("启动Polygon MCP服务器...")
    process = subprocess.Popen(
        ["node", "./polygon-mcp/build/index.js"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # 等待服务器启动
    print("等待服务器启动...")
    sleep(2)
    
    # 准备1inch Swap请求
    swap_request = {
        "id": "swap-test",
        "type": "call_tool",
        "params": {
            "name": "inch_swap",
            "arguments": {
                "fromTokenAddress": "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",  # MATIC
                "toTokenAddress": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",  # USDC
                "amount": "10000000000000000",  # 0.01 MATIC
                "slippage": 1  # 1%滑点
            }
        }
    }
    
    # 发送请求
    print("发送1inch Swap请求...")
    process.stdin.write(json.dumps(swap_request) + "\n")
    process.stdin.flush()
    
    # 读取并处理响应
    print("等待响应...")
    while True:
        line = process.stdout.readline().strip()
        if not line:
            continue
            
        try:
            response = json.loads(line)
            print(f"收到响应: {json.dumps(response, indent=2, ensure_ascii=False)}")
            
            # 检查是否是我们的swap-test响应
            if response.get("id") == "swap-test" and response.get("type") == "response":
                content = json.loads(response["response"]["content"][0]["text"])
                print("\n===== 交易结果 =====")
                print(json.dumps(content, indent=2, ensure_ascii=False))
                print(f"\n交易查看链接: {content.get('url')}")
                break
        except json.JSONDecodeError:
            print(f"非JSON输出: {line}")
        except Exception as e:
            print(f"处理响应时出错: {e}")
    
    # 关闭服务器
    print("\n测试完成，关闭服务器...")
    process.terminate()
    process.wait()

# 运行测试
if __name__ == "__main__":
    asyncio.run(test_inch_swap())
