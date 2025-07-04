#!/bin/bash

# AI Agent Platform Deployment Script

echo "🚀 Starting AI Agent Platform Deployment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Create network if it doesn't exist
docker network create ai-agent-network 2>/dev/null || true

# Build and start services
echo "📦 Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🔍 Checking service health..."

# Check API health
if curl -f http://localhost:8000/health/ > /dev/null 2>&1; then
    echo "✅ API service is healthy"
else
    echo "❌ API service is not responding"
fi

# Check FlowiseAI health
if curl -f http://localhost:3001 > /dev/null 2>&1; then
    echo "✅ FlowiseAI service is healthy"
else
    echo "❌ FlowiseAI service is not responding"
fi

# Check LangFuse health
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ LangFuse service is healthy"
else
    echo "❌ LangFuse service is not responding"
fi

echo ""
echo "🎉 Deployment completed!"
echo ""
echo "📋 Service URLs:"
echo "   • API Documentation: http://localhost:8000/docs"
echo "   • FlowiseAI: http://localhost:3001"
echo "   • LangFuse: http://localhost:3000"
echo ""
echo "🔧 To stop services: docker-compose down"
echo "📊 To view logs: docker-compose logs -f"