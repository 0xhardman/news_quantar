# AI Event Trader

## Background
It's well-known that cryptocurrency prices are highly susceptible to influential figures' (such as Vitalik Buterin, Donald Trump) statements on social media platforms. For example, on April 3rd, when Justin Sun suddenly criticized FUSDT, it caused significant de-pegging. However, after the FUSDT team clarified the situation, the price quickly returned to its pegged value. This demonstrates that monitoring key opinion leaders' (KOLs) statements on-chain presents substantial arbitrage opportunities. Unfortunately, a single person cannot constantly monitor every KOL's statements, which often leads to missed opportunities.

## Introduction
AI Event Trader aims to solve this problem through AI Agents that monitor KOLs' statements and autonomously make decisions to go long or short on specific tokens for arbitrage purposes.

## How It Works

### Polygon MCP
This project is built on Polygon MCP, using Python scripts to automatically monitor specific Farcaster accounts' messages and determine whether to buy or sell.

### 1inch
We use 1inch for trading and querying on-chain account status.

### ENS Subnames
Different agents under different subnames have varied trading styles.

### Circle
Quantitative trading users should minimize holding stablecoins and don't need to worry about gas token price fluctuations.

## Frequently Asked Questions

### Why Trade On-Chain?
TODO