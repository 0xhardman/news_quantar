#!/usr/bin/env python3
import os
import asyncio
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
    servers=["polygon"],  # Use the Polygon MCP server defined in fastagent.config.yaml
)

# Define main function
async def main():
    print("\n=== Polygon MCP Fast-Agent Example ===\n")
    print("Starting Fast-Agent and Polygon MCP server...\n")
    
    # Start Fast-Agent and begin interaction
    async with fast.run() as agent:
        # Test wallet address retrieval
        print("Testing connection with Polygon MCP...")
        response = await agent.send("Please tell me my wallet address")
        print(f"\nResponse: {response}\n")
        
        # Start interactive session
        print("Now you can start interacting with the AI assistant...\n")
        await agent()

# Program entry point
if __name__ == "__main__":
    asyncio.run(main())
