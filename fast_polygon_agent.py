#!/usr/bin/env python3
import os
import asyncio
from time import sleep
from dotenv import load_dotenv
from mcp_agent.core.fastagent import FastAgent

# Load environment variables
load_dotenv()

# Print SEED_PHRASE environment variable
print(f"SEED_PHRASE: {'*' * 5 if os.getenv('SEED_PHRASE') else 'Not found'}")

# Create Fast-Agent application
fast = FastAgent("Polygon MCP Example")

# Define agent using Polygon MCP server


@fast.agent(
    instruction="You are an AI assistant specialized in Polygon blockchain operations. Help users query wallet addresses, Gas prices, token balances, and other information.",
    # Use the Polygon MCP server defined in fastagent.config.yaml
    servers=["polygon"],
)
# Define main function
async def main():
    print("\n=== Polygon MCP Fast-Agent Example ===\n")
    print("Starting Fast-Agent and Polygon MCP server...\n")

    # Start Fast-Agent and begin interaction
    async with fast.run() as agent:
        # Test wallet address retrieval
        # print("Testing connection with Polygon MCP...")
        # response = await agent.send("Please tell me my wallet address")
        # print(f"\nResponse: {response}\n")

        # 测试1inch Swap功能
        print("\n=== 测试1inch Swap功能 ===\n")
        swap_prompt = (
            "Please swap 0.01 MATIC to USDC using 1inch. "
            "MATIC address is 0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270 and "
            "USDC address is 0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174. "
            "Use 1% slippage."
        )
        print(f"Sending request: {swap_prompt}")
        swap_response = await agent.send(swap_prompt)
        print(f"\nSwap Response: {swap_response}\n")

        # Start interactive session
        # print("Now you can start interacting with the AI assistant...\n")
        # await agent()
        # while True:
        #     print("\n=== Always check gas price ===\n")
        #     await agent.send("Please tell me the current gas price")
        #     await asyncio.sleep(10)

# Program entry point
if __name__ == "__main__":
    asyncio.run(main())
