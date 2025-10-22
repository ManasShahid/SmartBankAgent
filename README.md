# Streaming Agent

A multi-agent banking system built with LangGraph.

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Set up OpenAI API key:
   - Create a `.env` file with: `OPENAI_API_KEY=your_api_key_here`
   - Or set the environment variable: `export OPENAI_API_KEY=your_api_key_here`

3. Run the application:
```bash
uv run python main.py
```

## Features

- Multi-agent workflow for banking queries
- Account balance checking
- Loan application processing
- Transaction history retrieval
- RAG-based knowledge retrieval

## Architecture

The system uses LangGraph with a state-based workflow:
1. Query Agent - Understands customer queries
2. Planner Agent - Determines next steps
3. Response Agent - Generates responses using APIs and RAG
4. QA Agent - Validates response quality
