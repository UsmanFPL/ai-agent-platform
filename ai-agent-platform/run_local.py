#!/usr/bin/env python3
"""
Local development server for AI Agent Platform
Runs without Docker for development/testing
"""

import subprocess
import sys
import os
import time
import requests
from pathlib import Path

def install_dependencies():
    """Install required Python packages"""
    packages = [
        "fastapi==0.104.1",
        "uvicorn==0.24.0", 
        "langchain==0.1.0",
        "pydantic==2.5.0",
        "python-multipart==0.0.6",
        "aiofiles==23.2.1",
        "aiohttp==3.9.1"
    ]
    
    print("📦 Installing dependencies...")
    for package in packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"⚠️  Failed to install {package}")

def setup_environment():
    """Set up environment variables"""
    os.environ.update({
        "DATABASE_URL": "sqlite:///./ai_agent_platform.db",
        "REDIS_URL": "redis://localhost:6379",
        "ENVIRONMENT": "development",
        "DEBUG": "true"
    })
    print("🔧 Environment configured for local development")

def start_api_server():
    """Start the FastAPI server"""
    print("🚀 Starting AI Agent Platform API...")
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    # Start uvicorn server
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")

def test_tams_endpoint():
    """Test TAMS analysis endpoint"""
    print("🧪 Testing TAMS analysis...")
    try:
        response = requests.post("http://localhost:8000/api/v1/tams/test", timeout=10)
        if response.status_code == 200:
            print("✅ TAMS analysis working!")
            result = response.json()
            print(f"📊 Risk Score: {result.get('result', {}).get('final_recommendation', {}).get('overall_risk_score', 'N/A')}")
        else:
            print(f"⚠️  TAMS test returned status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ TAMS test failed: {e}")

def main():
    """Main execution function"""
    print("🎯 AI Agent Platform - Local Development Mode")
    print("=" * 50)
    
    # Install dependencies
    install_dependencies()
    
    # Setup environment
    setup_environment()
    
    # Start server
    start_api_server()

if __name__ == "__main__":
    main()