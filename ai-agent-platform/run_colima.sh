#!/bin/bash

# AI Agent Platform - Colima Startup Script
echo "🚀 Starting AI Agent Platform with Colima..."

# Check if Colima is installed
if ! command -v colima &> /dev/null; then
    echo "❌ Colima not found. Please install:"
    echo "   brew install colima"
    exit 1
fi

# Check if Docker CLI is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker CLI not found. Please install:"
    echo "   brew install docker"
    exit 1
fi

# Check if Colima is running
if ! colima status &> /dev/null; then
    echo "🔄 Starting Colima..."
    colima start --cpu 4 --memory 8 --disk 50
    echo "✅ Colima started"
else
    echo "✅ Colima already running"
fi

# Verify Docker connection
if ! docker info &> /dev/null; then
    echo "❌ Cannot connect to Docker. Try:"
    echo "   colima restart"
    exit 1
fi

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env with your API keys before continuing"
    echo "   Required: CUSTOM_LLM_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY"
    read -p "Press Enter after editing .env file..."
fi

# Start services
echo "🔄 Starting AI Agent Platform services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check service health
echo "🔍 Checking service health..."

# Check API
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ API Server: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
else
    echo "⚠️  API Server not ready yet"
fi

# Check FlowiseAI
if curl -s http://localhost:3001 > /dev/null; then
    echo "✅ FlowiseAI: http://localhost:3001"
else
    echo "⚠️  FlowiseAI not ready yet"
fi

# Check LangFuse
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ LangFuse: http://localhost:3000"
else
    echo "⚠️  LangFuse not ready yet"
fi

echo ""
echo "🎉 AI Agent Platform is starting up!"
echo ""
echo "📋 Available Services:"
echo "   • API Server: http://localhost:8000"
echo "   • API Documentation: http://localhost:8000/docs"
echo "   • FlowiseAI Builder: http://localhost:3001"
echo "   • LangFuse Monitoring: http://localhost:3000"
echo "   • TAMS Test: http://localhost:8000/api/v1/tams/test"
echo ""
echo "🛠️  Management Commands:"
echo "   • View logs: docker-compose logs -f"
echo "   • Stop services: docker-compose down"
echo "   • Restart: docker-compose restart"
echo "   • Stop Colima: colima stop"
echo ""
echo "📖 For troubleshooting, see COLIMA_SETUP.md"