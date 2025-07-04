#!/usr/bin/env python3
"""
Start AI Agent Platform Frontend
Installs dependencies and starts Next.js development server
"""

import subprocess
import sys
import os
import time
import webbrowser
import threading

def install_dependencies():
    """Install Node.js dependencies"""
    print("📦 Installing frontend dependencies...")
    
    try:
        # Check if Node.js is installed
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js and npm are required but not installed.")
        print("Please install Node.js from https://nodejs.org/")
        return False
    
    # Change to frontend directory
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    os.chdir(frontend_dir)
    
    try:
        # Install dependencies
        subprocess.run(["npm", "install"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting backend server...")
    
    backend_dir = os.path.dirname(__file__)
    
    try:
        # Start the backend server in a separate process
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "src.api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], cwd=backend_dir)
        
        print("✅ Backend server starting on http://localhost:8000")
        return backend_process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the Next.js frontend server"""
    print("🎨 Starting frontend server...")
    
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    
    try:
        # Start the frontend server
        subprocess.run(["npm", "run", "dev"], cwd=frontend_dir)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")

def open_browser():
    """Open browser after a delay"""
    time.sleep(3)
    webbrowser.open('http://localhost:3000')

def main():
    """Main execution function"""
    print("🎯 AI Agent Platform - Frontend Startup")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Start backend server
    backend_process = start_backend()
    if not backend_process:
        return
    
    # Wait a moment for backend to start
    time.sleep(2)
    
    # Open browser in background
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    print("\n🌐 Starting frontend development server...")
    print("📱 Frontend will open at: http://localhost:3000")
    print("🔧 Backend API available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("\n🛑 Press Ctrl+C to stop both servers")
    print("=" * 50)
    
    try:
        # Start frontend (this will block)
        start_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
    finally:
        # Clean up backend process
        if backend_process:
            backend_process.terminate()
            backend_process.wait()
        print("✅ All servers stopped")

if __name__ == "__main__":
    main()