# AgenticBankAI

**A multi-layer autonomous AI agent system for banking applications.**

## Overview
AgenticBankAI demonstrates how **Agentic AI concepts** can be applied in banking:
- Multi-layer agent architecture (Perception → Planning → Execution → QA)
- MCP (Model Context Protocol) memory integration
- RAG (Retrieval-Augmented Generation) for knowledge retrieval
- A2A (Agent-to-Agent) handoff for seamless agent collaboration
- Simulated banking APIs for account balance, loans, and transactions

## Features
- Check account balance
- Apply for loans (with simulated approval logic)
- Fetch transaction history
- RAG-based fallback for unknown queries
- QA layer for validating responses
- Modular and extensible for new banking tasks

## Installation
```bash
pip install langgraph langchain openai faiss-cpu
