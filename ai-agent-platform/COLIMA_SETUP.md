# Colima Setup for AI Agent Platform

Colima is a lightweight Docker alternative for macOS that works well in corporate environments with Docker restrictions.

## Installation

```bash
# Install Colima
brew install colima

# Install Docker CLI
brew install docker

# Install docker-compose
brew install docker-compose
```

## Starting Colima

```bash
# Start Colima with recommended resources
colima start --cpu 4 --memory 8 --disk 50

# Verify installation
docker --version
docker-compose --version
```

## Running the Platform

```bash
# Clone repository
git clone https://github.com/UsmanFPL/ai-agent-platform.git
cd ai-agent-platform

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Start with Colima
./run_colima.sh
```

## Stopping Services

```bash
# Stop platform
docker-compose down

# Stop Colima (optional)
colima stop
```

## Troubleshooting

### Port Conflicts
If ports are in use, modify `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # API
  - "3002:3001"  # FlowiseAI
  - "3001:3000"  # LangFuse
```

### Memory Issues
Increase Colima memory:
```bash
colima stop
colima start --cpu 4 --memory 12
```

### Docker Socket Issues
```bash
# Reset Docker context
docker context use default
```