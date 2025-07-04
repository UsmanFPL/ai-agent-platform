# AI Agent Platform Architecture

## Overview
The AI Agent Platform is designed to support two types of agents:
- **Automation Agents**: Deterministic workflow execution using state machines
- **Assistive Agents**: Flexible, conversational interactions using ReAct patterns

## Core Components

### 1. Agent Core (`src/core/`)
- **Database**: SQLAlchemy models and connection management
- **LLM**: Multi-provider abstraction (OpenAI, Anthropic)
- **Prompts**: Centralized prompt management and versioning
- **Memory**: Redis-based conversation memory
- **Graph**: LangGraph workflow orchestration

### 2. Agents (`src/agents/`)
- **Base Agent**: Abstract base class with lifecycle management
- **Automation Agent**: State machine-based workflow execution
- **Assistive Agent**: ReAct-style conversational agent

### 3. Tools (`src/tools/`)
- **Base Tool**: Abstract tool interface with validation
- **Database Tool**: SQL query execution with security constraints
- **API Tool**: HTTP API call functionality
- **Tool Registry**: Central tool discovery and management

### 4. API (`src/api/`)
- **FastAPI**: REST API with automatic documentation
- **Routers**: Modular endpoint organization
- **Schemas**: Pydantic models for request/response validation
- **Health Checks**: System monitoring endpoints

## Data Flow

### Automation Agent Flow
1. Receive input data
2. Validate against workflow requirements
3. Execute LangGraph state machine
4. Use registered tools for each step
5. Return structured results

### Assistive Agent Flow
1. Receive user message
2. Load conversation memory
3. Execute ReAct reasoning loop
4. Use tools as needed
5. Generate response and save to memory

## Security
- SQL injection prevention (SELECT-only queries)
- Input validation at all layers
- Environment-based configuration
- Tool execution sandboxing

## Scalability
- Async/await throughout
- Redis for distributed memory
- PostgreSQL for persistent storage
- Docker containerization