#!/bin/bash

echo "🚀 Starting AI Agent Platform with TAMS..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Create network
echo "📡 Creating Docker network..."
docker network create ai-agent-network 2>/dev/null || true

# Start services
echo "🐳 Starting services..."
docker-compose up -d --build

# Wait for services
echo "⏳ Waiting for services to start..."
sleep 30

# Check health
echo "🔍 Checking service health..."

# Check API
if curl -f http://localhost:8000/health/ > /dev/null 2>&1; then
    echo "✅ API service is healthy"
else
    echo "❌ API service is not responding"
fi

# Check FlowiseAI
if curl -f http://localhost:3001 > /dev/null 2>&1; then
    echo "✅ FlowiseAI is healthy"
else
    echo "❌ FlowiseAI is not responding"
fi

# Import TAMS workflow
echo "📊 Importing TAMS workflow to FlowiseAI..."
sleep 10
curl -X POST "http://localhost:8000/api/v1/flowise/workflows/tams/import" 2>/dev/null || echo "⚠️  TAMS workflow import will be available once API is ready"

echo ""
echo "🎉 Platform is ready!"
echo ""
echo "📋 Access URLs:"
echo "   • API Documentation: http://localhost:8000/docs"
echo "   • TAMS Analysis: http://localhost:8000/api/v1/tams/test"
echo "   • FlowiseAI (No-Code): http://localhost:3001"
echo "   • LangFuse (Monitoring): http://localhost:3000"
echo ""
echo "🧪 Test TAMS Analysis:"
echo "curl -X POST http://localhost:8000/api/v1/tams/test"
echo ""
echo "🛑 To stop: docker-compose down"