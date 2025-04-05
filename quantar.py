#!/usr/bin/env python3
import os
import asyncio
import sys
import json
from dotenv import load_dotenv
from mcp_agent.core.fastagent import FastAgent

# Add webhook-sdk to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'webhook-sdk'))
from webhook_server import WebhookServer

# Load environment variables
load_dotenv()

# Create Fast-Agent application
fast = FastAgent("Farcaster Event Trader")

# Define trading limit (in USDC)
TRADE_LIMIT_USDC = 1.0

# Define authorized trading users
AUTHORIZED_USERS = ['0xhardman']

# Define common token addresses
TOKEN_ADDRESSES = {
    'USDC': '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359',  # Native USDC
    # WARNING: NEVER USE USDC.e FOR ANY TRANSACTIONS
    'USDC.e': 'DO_NOT_USE',  # USDC.e - Prohibited for any transactions
    'WETH': '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619',
    'WBTC': '0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6',
    'MATIC': '0x0000000000000000000000000000000000001010',
    'WMATIC': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270'
}

# Define agent using Polygon MCP server


@fast.agent(
    instruction="""You are an AI assistant specialized in analyzing Farcaster messages and executing cryptocurrency trades.

When you receive a Farcaster message, you need to:
1. Analyze the message content to determine if it contains trading intent (buy/sell a token)
2. If trading intent is detected, identify the trade type (buy/sell), token symbol, and amount (if specified)
3. Execute the appropriate trading operation, ensuring the trade amount does not exceed 1 USDC
4. Return the trade execution results

Trading style:
- Conservative: Do not execute trades unless explicitly instructed
- Precise: Execute trades strictly according to the message instructions
- Safe: Always adhere to trading limits
- Transparent: Clearly report all trading details

Important notes:
- STRICTLY PROHIBITED from using USDC.e for any transactions, always use only native USDC (0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359)
- Use token addresses defined in the TOKEN_ADDRESSES dictionary
- Only messages from authorized users will trigger trades
- PAY ATTENTION TO TOKEN DECIMALS when calculating amounts:
  * USDC: 6 decimals (1 USDC = 1,000,000 wei)
  * WBTC: 8 decimals (1 WBTC = 100,000,000 wei)
  * WETH/WMATIC: 18 decimals (1 token = 1,000,000,000,000,000,000 wei)
- Always use get_token_decimals tool to verify token decimals before calculating amounts

Always ensure trading safety and follow all restrictions.""",
    # Use Polygon MCP server defined in fastagent.config.yaml
    servers=["polygon"],
)
# Callback function to process Farcaster messages
async def process_farcaster_event(event_data):
    """Process events received from Farcaster webhook

    Args:
        event_data: Neynar webhook event data
    """
    if event_data.get('type') == 'cast.created':
        # Get cast data from data field
        cast_data = event_data.get('data', {})

        # Get author information
        author = cast_data.get('author', {})
        username = author.get('username', 'unknown')

        # Check if user is authorized
        if username not in AUTHORIZED_USERS:
            print(
                f"Received message from unauthorized user @{username}, ignoring")
            return

        # Get cast text
        text = cast_data.get('text', '')
        print(f"\nReceived message from @{username}: {text}")

        # Use Fast-Agent to analyze message and execute trade
        async with fast.run() as agent:
            # Send message to agent for analysis
            prompt = f"""Analyze this Farcaster message and decide whether to execute a trade (limit {TRADE_LIMIT_USDC} USDC): '{text}'

Notes:
1. STRICTLY PROHIBITED from using USDC.e for any transactions, always use only native USDC (address: {TOKEN_ADDRESSES['USDC']})
2. If trading BTC is needed, use WBTC (address: {TOKEN_ADDRESSES['WBTC']})
3. If trading ETH is needed, use WETH (address: {TOKEN_ADDRESSES['WETH']})
4. If trading MATIC is needed, use WMATIC (address: {TOKEN_ADDRESSES['WMATIC']})
5. PAY ATTENTION TO TOKEN DECIMALS when calculating amounts:
   - USDC uses 6 decimals (1 USDC = 1,000,000 wei)
   - WBTC uses 8 decimals (1 WBTC = 100,000,000 wei)
   - WETH uses 18 decimals (1 WETH = 1,000,000,000,000,000,000 wei)
   - WMATIC uses 18 decimals (1 WMATIC = 1,000,000,000,000,000,000 wei)
6. Always use get_token_decimals tool to verify token decimals before calculating amounts
"""
            response = await agent.send(prompt)

            print(f"\nAgent response: {response}\n")

# Define main function


async def main():
    print("\n=== Farcaster Event Trader ===\n")
    print("Starting Fast-Agent and Polygon MCP server...\n")

    # Create and start webhook server (run in background)
    webhook_server = WebhookServer(callback=process_farcaster_event)
    webhook_task = asyncio.create_task(
        asyncio.to_thread(webhook_server.run)
    )

    print(f"Webhook server started, listening on port 8000")
    print(f"Authorized users: {', '.join(AUTHORIZED_USERS)}")
    print(f"Trading limit: {TRADE_LIMIT_USDC} USDC")
    print("\nWaiting for Farcaster messages...\n")

    try:
        # Keep program running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down services...")
    finally:
        # Cancel webhook task
        webhook_task.cancel()
        try:
            await webhook_task
        except asyncio.CancelledError:
            pass
        print("Services shut down")

# Run main function
if __name__ == "__main__":
    asyncio.run(main())
