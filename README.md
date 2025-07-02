# AI Agent Platform

An internal AI Agent Platform built with LangChain, LangGraph, FlowiseAI, and CrewAI for automating workflows and providing intelligent assistance.

## Architecture

- **Foundation:** LangChain for LLM orchestration
- **Orchestration:** LangGraph for agent workflows
- **Visual Builder:** FlowiseAI for no-code/low-code interface
- **Multi-Agent:** CrewAI for collaborative agents
- **Monitoring:** LangFuse for observability and evaluation
- **Backend:** Python (FastAPI)
- **Frontend:** React/Next.js
- **Database:** PostgreSQL + Vector DB (Chroma)
- **Infrastructure:** Docker, Kubernetes

## Project Structure

```
AAP/
├── backend/           # Python FastAPI backend
├── frontend/          # React/Next.js frontend
├── agents/            # Agent implementations
├── tools/             # Custom tools and integrations
├── workflows/         # Workflow templates and definitions
├── docs/              # Documentation
├── tests/             # Test suites
├── docker/            # Docker configurations
└── scripts/           # Utility scripts
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL

### Installation

1. Clone the repository
2. Set up Python virtual environment
3. Install dependencies
4. Configure environment variables
5. Run with Docker Compose

## Development

See [Development Guide](docs/development.md) for detailed setup instructions.

## License

Internal use only.