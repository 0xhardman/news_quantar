#!/usr/bin/env python3
import os
import asyncio
import sys
import json
from dotenv import load_dotenv
from mcp_agent.core.fastagent import FastAgent

# 添加 webhook-sdk 到 Python 路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'webhook-sdk'))
from webhook_server import WebhookServer

# 加载环境变量
load_dotenv()

# 创建 Fast-Agent 应用
fast = FastAgent("Farcaster Event Trader")

# u5b9au4e49u4ea4u6613u9650u989duff08u4ee5 USDC u8ba1uff09
TRADE_LIMIT_USDC = 1.0

# u5b9au4e49u5141u8bb8u7684u4ea4u6613u7528u6237
AUTHORIZED_USERS = ['0xhardman']

# u5b9au4e49u5e38u7528u4ee3u5e01u5730u5740
TOKEN_ADDRESSES = {
    'USDC': '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359',  # u539fu751f USDC
    'USDC.e': '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',  # USDC.e
    'WETH': '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619',
    'WBTC': '0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6',
    'MATIC': '0x0000000000000000000000000000000000001010',
    'WMATIC': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270'
}

# u5b9au4e49 agentuff0cu4f7fu7528 Polygon MCP u670du52a1u5668
@fast.agent(
    instruction="""你是一个专门用于分析 Farcaster 消息并执行加密货币交易的 AI 助手。

当你收到 Farcaster 消息时，你需要：
1. 分析消息内容，判断是否包含交易意图（买入/卖出某种代币）
2. 如果检测到交易意图，确定交易类型（买入/卖出）、代币符号和金额（如果有指定）
3. 执行相应的交易操作，但确保交易金额不超过 1 USDC
4. 返回交易执行结果

交易风格：
- 保守：除非明确指示，否则不执行交易
- 精确：严格按照消息中的指示执行交易
- 安全：始终遵守交易限额
- 透明：清晰报告所有交易细节

重要说明：
- 只使用原生 USDC (0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359) 进行交易，不要使用 USDC.e
- 使用 TOKEN_ADDRESSES 字典中定义的代币地址
- 只有来自授权用户的消息才会触发交易

示例消息和响应：
消息："我觉得 ETH 要涨了，买一些"
分析：检测到买入 ETH 的意图
操作：使用原生 USDC 买入价值 1 USDC 的 ETH

消息："卖掉我的 MATIC"
分析：检测到卖出 MATIC 的意图
操作：卖出价值 1 USDC 的 MATIC，换成原生 USDC

消息："今天天气真好"
分析：未检测到交易意图
操作：不执行任何交易

请始终确保交易安全，并遵守所有限制。""",
    # 使用在 fastagent.config.yaml 中定义的 Polygon MCP 服务器
    servers=["polygon"],
)
# 处理 Farcaster 消息的回调函数
async def process_farcaster_event(event_data):
    """处理从 Farcaster webhook 接收到的事件
    
    Args:
        event_data: Neynar webhook 事件数据
    """
    if event_data.get('type') == 'cast.created':
        # 从 data 字段获取 cast 数据
        cast_data = event_data.get('data', {})
        
        # 获取作者信息
        author = cast_data.get('author', {})
        username = author.get('username', 'unknown')
        
        # 检查是否为授权用户
        if username not in AUTHORIZED_USERS:
            print(f"收到未授权用户 @{username} 的消息，忽略")
            return
        
        # 获取 cast 文本
        text = cast_data.get('text', '')
        print(f"\n收到来自 @{username} 的消息: {text}")
        
        # 使用 Fast-Agent 分析消息并执行交易
        async with fast.run() as agent:
            # 发送消息给 agent 进行分析
            prompt = f"""分析这条 Farcaster 消息并决定是否执行交易（限额 {TRADE_LIMIT_USDC} USDC）: '{text}'

需要说明：
1. 请使用原生 USDC（地址：{TOKEN_ADDRESSES['USDC']}）进行交易，不要使用 USDC.e
2. 如果需要交易 BTC，请使用 WBTC（地址：{TOKEN_ADDRESSES['WBTC']}）
3. 如果需要交易 ETH，请使用 WETH（地址：{TOKEN_ADDRESSES['WETH']}）
4. 如果需要交易 MATIC，请使用 WMATIC（地址：{TOKEN_ADDRESSES['WMATIC']}）
"""
            response = await agent.send(prompt)
            
            print(f"\nAgent 响应: {response}\n")

# 定义主函数
async def main():
    print("\n=== Farcaster Event Trader ===\n")
    print("启动 Fast-Agent 和 Polygon MCP 服务器...\n")

    # 创建并启动 webhook 服务器（在后台运行）
    webhook_server = WebhookServer(callback=process_farcaster_event)
    webhook_task = asyncio.create_task(
        asyncio.to_thread(webhook_server.run)
    )
    
    print(f"Webhook 服务器已启动，监听端口 8000")
    print(f"授权用户: {', '.join(AUTHORIZED_USERS)}")
    print(f"交易限额: {TRADE_LIMIT_USDC} USDC")
    print("\n等待 Farcaster 消息...\n")
    
    try:
        # 保持程序运行
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n正在关闭服务...")
    finally:
        # 取消 webhook 任务
        webhook_task.cancel()
        try:
            await webhook_task
        except asyncio.CancelledError:
            pass
        print("服务已关闭")

# 运行主函数
if __name__ == "__main__":
    asyncio.run(main())
