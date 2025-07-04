# AI Agent Platform - Deployment Guide

## Quick Start

1. **Prerequisites**
   - Docker and Docker Compose installed
   - Python 3.11+ (for development)
   - Git

2. **Environment Setup**
   ```bash
   # Clone and navigate to project
   cd ai-agent-platform
   
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your API keys
   nano .env
   ```

3. **Deploy Platform**
   ```bash
   # Run deployment script
   ./deploy.sh
   ```

## Service URLs

- **API Documentation**: http://localhost:8000/docs
- **FlowiseAI**: http://localhost:3001
- **LangFuse**: http://localhost:3000
- **Health Check**: http://localhost:8000/health/

## Configuration

### Required Environment Variables

```env
# LLM Providers
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Database
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/ai_agent_platform
REDIS_URL=redis://redis:6379

# LangFuse
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_HOST=http://localhost:3000

# Security
SECRET_KEY=your_secret_key_here
```

## Development Setup

1. **Install Dependencies**
   ```bash
   poetry install
   ```

2. **Run Tests**
   ```bash
   poetry run pytest
   ```

3. **Start Development Server**
   ```bash
   poetry run uvicorn src.api.main:app --reload
   ```

## Production Deployment

### Docker Swarm
```bash
docker swarm init
docker stack deploy -c docker-compose.yml ai-agent-platform
```

### Kubernetes
```bash
# Generate Kubernetes manifests
docker-compose config > k8s-manifests.yaml
kubectl apply -f k8s-manifests.yaml
```

## Monitoring

- **Health Checks**: All services expose `/health` endpoints
- **Metrics**: LangFuse provides comprehensive observability
- **Logs**: Use `docker-compose logs -f` to view logs

## Scaling

### Horizontal Scaling
```bash
# Scale API service
docker-compose up -d --scale api=3

# Scale with load balancer
docker-compose -f docker-compose.yml -f docker-compose.scale.yml up -d
```

### Database Scaling
- Use PostgreSQL read replicas
- Implement connection pooling
- Consider database sharding for high volume

## Security

1. **API Security**
   - JWT authentication enabled
   - CORS configured
   - Input validation on all endpoints

2. **Database Security**
   - SQL injection prevention
   - Encrypted connections
   - Regular backups

3. **Network Security**
   - Internal Docker network
   - Firewall rules
   - SSL/TLS termination

## Troubleshooting

### Common Issues

1. **Services not starting**
   ```bash
   docker-compose logs [service_name]
   ```

2. **Database connection issues**
   ```bash
   docker-compose exec postgres psql -U postgres -d ai_agent_platform
   ```

3. **Memory issues**
   ```bash
   docker system prune
   docker-compose restart
   ```

### Performance Tuning

1. **Database Optimization**
   - Add indexes for frequent queries
   - Tune PostgreSQL configuration
   - Monitor query performance

2. **API Optimization**
   - Enable response caching
   - Implement connection pooling
   - Use async operations

3. **Memory Management**
   - Monitor container memory usage
   - Implement garbage collection
   - Optimize vector database size