# How It's Made

## Architecture Overview

Our News Quantar project is built on a three-tier architecture that combines blockchain interaction capabilities with natural language processing and social media monitoring:

1. **Polygon MCP (Modified Client for Polygon)**: A forked and enhanced version of the official Polygon MCP that serves as our blockchain interaction layer
2. **Fast-Agent Framework**: The intelligence layer that processes natural language and makes trading decisions
3. **Webhook SDK**: A lightweight service that monitors Farcaster for real-time social signals

## Technical Implementation

### Polygon MCP Enhancements with 1inch Integration

We forked the official Polygon MCP and made several critical enhancements. The Polygon MCP serves as the essential execution layer for our agent - functioning as its "hands and feet" in the blockchain world. Without this component, our intelligent agent would be unable to interact with the blockchain or execute trades, making it the foundational element that enables the entire system to function effectively.

- **1inch Swap Integration**: We implemented a comprehensive swap handler (`inchSwapHandler`) that connects to the 1inch API for optimal trading routes and best execution prices. The integration includes:
  - Automatic slippage management
  - Gas estimation with safety buffers
  - Token approval checks
  - USDC/USDC.e safety mechanisms to prevent using deprecated tokens
  - Optimized routing through 1inch's aggregation API, which significantly reduces trading costs by finding the most efficient paths across multiple DEXes while maintaining full decentralization

- **Token Management Tools**: We added specialized handlers for:
  - `checkAllowanceHandler`: Verifies if sufficient token approvals exist
  - `approveTokenHandler`: Streamlines the token approval process
  - `getTokenDecimalsHandler`: Ensures accurate decimal handling across different tokens

### Fast-Agent Framework Implementation

We built our agent using the Fast-Agent framework, which provides a clean abstraction for LLM-powered applications. Our implementation includes:

- **Dual-mode Operation**:
  - `chat.py`: A direct interface for manual blockchain interactions through natural language
  - `quantar.py`: An automated trading agent that processes Farcaster messages and executes trades based on social signals

- **Prompt Engineering**: We carefully crafted system instructions that:
  - Enforce trading limits (max 1 USDC per trade)
  - Implement strict token address validation
  - Prevent the use of deprecated tokens (USDC.e)
  - Handle token decimal precision correctly

- **Claude 3.7 Sonnet Integration**: We integrated with Claude's API for advanced natural language understanding, using the endpoint at `https://chat.cloudapi.vip/v1`

### Webhook SDK for Farcaster Monitoring

We developed a lightweight but robust webhook service using FastAPI that:

- Provides a `/webhook` endpoint to receive Farcaster events
- Implements event deduplication to prevent double-processing
- Uses an asynchronous callback system to process events without blocking
- Logs all activities for audit and debugging purposes

## Security and Configuration Management

We implemented a comprehensive security approach:

- **Environment Variable Management**: Sensitive data like API keys and seed phrases are stored in `.env` files and excluded from git
- **Configuration Separation**: We use `fastagent.config.yaml` for non-sensitive configuration and load sensitive data from environment variables
- **Token Address Safety**: We maintain a `TOKEN_ADDRESSES` dictionary with verified addresses to prevent using incorrect or deprecated tokens
- **Trading Limits**: Hard-coded maximum trade size of 1 USDC to limit risk exposure
- **Authorized User Restrictions**: Only specified Farcaster accounts can trigger trades

## Hacky But Effective Solutions

1. **USDC.e Protection**: We implemented multiple safeguards to prevent the use of USDC.e, including:
   - Setting the USDC.e address to `DO_NOT_USE` in the token dictionary
   - Adding automatic replacement of USDC.e with native USDC in the swap handler
   - Including explicit warnings in agent instructions
   - Avoiding USDC.e entirely due to its persistent liquidity issues, which often lead to failed trades, higher slippage, and suboptimal execution prices

2. **Webhook Event Deduplication**: We created a simple but effective event ID generation system using `event_type_created_at` to prevent duplicate processing without needing a database

3. **Decimal Precision Handling**: We added explicit reminders about token decimal differences in agent instructions and implemented a dedicated tool to verify token decimals before calculations

The combination of these components creates a system that can monitor social media for trading signals, analyze them using advanced AI, and execute trades automatically with built-in safety mechanisms.
