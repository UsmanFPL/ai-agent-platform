#!/usr/bin/env python3
"""
Quick Start - AI Agent Platform Frontend
Minimal setup to get the platform running
"""

import subprocess
import sys
import os
import time
import webbrowser
import threading

def start_backend():
    """Start FastAPI backend"""
    print("🚀 Starting backend...")
    
    # Set OneGPT environment
    os.environ["CUSTOM_LLM_URL"] = "https://onegpt.fplinternal.in/api/chat/completions"
    os.environ["CUSTOM_LLM_MODEL"] = "gpt-4o"
    os.environ["CUSTOM_LLM_API_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjAyZDY2MTQ2LTVjYmYtNDEwZC1hNTlkLWJkMGQ4NjY3MzYxNCJ9.-rBBUXk5DqNk2eIN_5_SPfzuPX-brATzN_N6hi0QY5w"
    
    try:
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "src.api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
        print("✅ Backend started on http://localhost:8000")
        return backend_process
    except Exception as e:
        print(f"❌ Backend failed: {e}")
        return None

def create_simple_frontend():
    """Create a simple HTML frontend"""
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agent Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen">
    <div class="max-w-6xl mx-auto p-8">
        <header class="text-center mb-8">
            <h1 class="text-4xl font-bold text-gray-900 mb-2">🎯 AI Agent Platform</h1>
            <p class="text-gray-600">Enterprise Automation & Intelligence</p>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="bg-white rounded-lg shadow p-6 text-center">
                <div class="text-3xl font-bold text-blue-600">3</div>
                <div class="text-gray-600">Total Agents</div>
            </div>
            <div class="bg-white rounded-lg shadow p-6 text-center">
                <div class="text-3xl font-bold text-green-600">2</div>
                <div class="text-gray-600">Active Agents</div>
            </div>
            <div class="bg-white rounded-lg shadow p-6 text-center">
                <div class="text-3xl font-bold text-purple-600">1.8s</div>
                <div class="text-gray-600">Avg Response</div>
            </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6 mb-8">
            <h2 class="text-2xl font-bold mb-4">🔍 TAMS Analysis</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                    <label class="block text-sm font-medium mb-2">Merchant</label>
                    <input type="text" id="merchant" value="Unknown Online Store" 
                           class="w-full px-3 py-2 border rounded-md">
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">Amount ($)</label>
                    <input type="number" id="amount" value="299.99" 
                           class="w-full px-3 py-2 border rounded-md">
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">Transaction Type</label>
                    <select id="type" class="w-full px-3 py-2 border rounded-md">
                        <option value="Card-Not-Present">Card-Not-Present</option>
                        <option value="Card-Present">Card-Present</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">User ID</label>
                    <input type="text" id="userId" value="user_12345" 
                           class="w-full px-3 py-2 border rounded-md">
                </div>
            </div>
            <button onclick="analyzeTAMS()" id="analyzeBtn" 
                    class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700">
                🚀 Run TAMS Analysis
            </button>
            <div id="results" class="mt-6 hidden">
                <h3 class="text-lg font-semibold mb-2">Analysis Results:</h3>
                <div id="resultContent" class="bg-gray-50 p-4 rounded-md"></div>
            </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-2xl font-bold mb-4">🤖 Active Agents</h2>
            <div class="space-y-3">
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                    <div>
                        <div class="font-medium">TAMS AI-Assist</div>
                        <div class="text-sm text-gray-600">Fraud Detection Agent</div>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span class="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs">Active</span>
                        <button onclick="testTAMS()" class="px-3 py-1 bg-blue-100 text-blue-800 rounded text-xs">Test</button>
                    </div>
                </div>
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                    <div>
                        <div class="font-medium">Email Automation Agent</div>
                        <div class="text-sm text-gray-600">Communication Automation</div>
                    </div>
                    <span class="px-2 py-1 bg-gray-100 text-gray-800 rounded-full text-xs">Idle</span>
                </div>
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                    <div>
                        <div class="font-medium">Document Processing Agent</div>
                        <div class="text-sm text-gray-600">Document Analysis</div>
                    </div>
                    <span class="px-2 py-1 bg-gray-100 text-gray-800 rounded-full text-xs">Idle</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        async function analyzeTAMS() {
            const btn = document.getElementById('analyzeBtn');
            const results = document.getElementById('results');
            const content = document.getElementById('resultContent');
            
            btn.textContent = '⏳ Analyzing...';
            btn.disabled = true;
            
            const data = {
                timestamp: new Date().toISOString(),
                merchant: document.getElementById('merchant').value,
                amount: parseFloat(document.getElementById('amount').value),
                transaction_type: document.getElementById('type').value,
                user_id: document.getElementById('userId').value
            };
            
            try {
                const response = await fetch('http://localhost:8000/api/v1/tams/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    const rec = result.final_recommendation;
                    content.innerHTML = `
                        <div class="space-y-4">
                            <div class="grid grid-cols-3 gap-4 text-center">
                                <div>
                                    <div class="text-2xl font-bold text-red-600">${rec.overall_risk_score}/10</div>
                                    <div class="text-sm text-gray-600">Risk Score</div>
                                </div>
                                <div>
                                    <div class="text-lg font-semibold">${rec.final_classification}</div>
                                    <div class="text-sm text-gray-600">Classification</div>
                                </div>
                                <div>
                                    <div class="text-lg font-semibold">${rec.confidence_level}</div>
                                    <div class="text-sm text-gray-600">Confidence</div>
                                </div>
                            </div>
                            <div>
                                <h4 class="font-semibold mb-2">Recommended Actions:</h4>
                                <ul class="list-disc list-inside space-y-1">
                                    ${rec.next_actions.map(action => `<li class="text-sm">${action}</li>`).join('')}
                                </ul>
                            </div>
                        </div>
                    `;
                    results.classList.remove('hidden');
                } else {
                    content.innerHTML = `<div class="text-red-600">Analysis failed: ${result.error || 'Unknown error'}</div>`;
                    results.classList.remove('hidden');
                }
            } catch (error) {
                content.innerHTML = `<div class="text-red-600">Connection error: ${error.message}</div>`;
                results.classList.remove('hidden');
            } finally {
                btn.textContent = '🚀 Run TAMS Analysis';
                btn.disabled = false;
            }
        }
        
        async function testTAMS() {
            try {
                const response = await fetch('http://localhost:8000/api/v1/tams/test', { method: 'POST' });
                const result = await response.json();
                alert(`TAMS Test: ${response.ok ? 'Success' : 'Failed'}\\nRisk Score: ${result.result?.final_recommendation?.overall_risk_score || 'N/A'}/10`);
            } catch (error) {
                alert(`TAMS Test Error: ${error.message}`);
            }
        }
    </script>
</body>
</html>'''
    
    with open('frontend_simple.html', 'w') as f:
        f.write(html_content)
    
    print("✅ Simple frontend created: frontend_simple.html")

def main():
    print("🎯 AI Agent Platform - Quick Start")
    print("=" * 40)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        return
    
    # Create simple frontend
    create_simple_frontend()
    
    # Wait for backend to start
    time.sleep(3)
    
    # Open browser
    print("🌐 Opening frontend...")
    webbrowser.open('file://' + os.path.abspath('frontend_simple.html'))
    
    print("\n✅ Platform is running!")
    print("📱 Frontend: file://frontend_simple.html")
    print("🔧 Backend: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\n🛑 Press Ctrl+C to stop")
    
    try:
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
        backend_process.terminate()

if __name__ == "__main__":
    main()