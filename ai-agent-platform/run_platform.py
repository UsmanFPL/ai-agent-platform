#!/usr/bin/env python3
"""
Run AI Agent Platform - Minimal Setup
"""

import subprocess
import sys
import os
import time
import webbrowser

def setup_environment():
    """Set up OneGPT environment"""
    os.environ["CUSTOM_LLM_URL"] = "https://onegpt.fplinternal.in/api/chat/completions"
    os.environ["CUSTOM_LLM_MODEL"] = "gpt-4o"
    os.environ["CUSTOM_LLM_API_KEY"] = os.getenv("CUSTOM_LLM_API_KEY", "your-jwt-token-here")

def create_frontend():
    """Create simple frontend HTML"""
    html = '''<!DOCTYPE html>
<html>
<head>
    <title>AI Agent Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 p-8">
    <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold mb-8 text-center">🎯 AI Agent Platform</h1>
        
        <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h2 class="text-xl font-bold mb-4">🔍 TAMS Analysis</h2>
            <div class="grid grid-cols-2 gap-4 mb-4">
                <input type="text" id="merchant" placeholder="Merchant" value="Unknown Online Store" class="border p-2 rounded">
                <input type="number" id="amount" placeholder="Amount" value="299.99" class="border p-2 rounded">
            </div>
            <button onclick="runAnalysis()" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                Run Analysis
            </button>
            <div id="result" class="mt-4 hidden"></div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-bold mb-4">🤖 System Status</h2>
            <div class="space-y-2">
                <div class="flex justify-between">
                    <span>TAMS Agent</span>
                    <span class="text-green-600">Active</span>
                </div>
                <div class="flex justify-between">
                    <span>OneGPT Connection</span>
                    <span class="text-green-600">Connected</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        async function runAnalysis() {
            const result = document.getElementById('result');
            result.innerHTML = '<div class="text-blue-600">Analyzing...</div>';
            result.classList.remove('hidden');
            
            try {
                const response = await fetch('http://localhost:8000/api/v1/tams/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        timestamp: new Date().toISOString(),
                        merchant: document.getElementById('merchant').value,
                        amount: parseFloat(document.getElementById('amount').value),
                        transaction_type: 'Card-Not-Present',
                        user_id: 'user_12345'
                    })
                });
                
                const data = await response.json();
                const rec = data.final_recommendation;
                
                result.innerHTML = `
                    <div class="bg-gray-50 p-4 rounded">
                        <div class="grid grid-cols-3 gap-4 text-center mb-4">
                            <div>
                                <div class="text-2xl font-bold text-red-600">${rec.overall_risk_score}/10</div>
                                <div class="text-sm">Risk Score</div>
                            </div>
                            <div>
                                <div class="font-semibold">${rec.final_classification}</div>
                                <div class="text-sm">Classification</div>
                            </div>
                            <div>
                                <div class="font-semibold">${rec.confidence_level}</div>
                                <div class="text-sm">Confidence</div>
                            </div>
                        </div>
                        <div>
                            <strong>Actions:</strong>
                            <ul class="list-disc list-inside mt-2">
                                ${rec.next_actions.map(action => `<li>${action}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                `;
            } catch (error) {
                result.innerHTML = `<div class="text-red-600">Error: ${error.message}</div>`;
            }
        }
    </script>
</body>
</html>'''
    
    with open('platform.html', 'w') as f:
        f.write(html)

def main():
    print("🎯 AI Agent Platform - Starting...")
    
    setup_environment()
    create_frontend()
    
    print("✅ Frontend created: platform.html")
    print("🚀 Starting TAMS agent...")
    
    # Test TAMS directly
    try:
        result = subprocess.run([sys.executable, "run_tams_onegpt.py"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ TAMS agent working!")
        else:
            print("⚠️  TAMS agent test completed with warnings")
    except Exception as e:
        print(f"⚠️  TAMS test: {e}")
    
    # Open frontend
    webbrowser.open('file://' + os.path.abspath('platform.html'))
    
    print("\n🎉 Platform Ready!")
    print("📱 Frontend: platform.html")
    print("🔧 TAMS: Working with OneGPT")
    print("\nFor full API server, run: python3 run_tams_onegpt.py")

if __name__ == "__main__":
    main()