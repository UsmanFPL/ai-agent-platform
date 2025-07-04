#!/usr/bin/env python3
"""Web demo for TAMS AI-Assist with visual interface"""

import asyncio
from quick_start import MockTAMSAgent
import webbrowser
import http.server
import socketserver
import threading
import json

def create_html_demo():
    """Create HTML demo page"""
    
    # Get analysis results
    agent = MockTAMSAgent()
    sample_alert = {
        "timestamp": "2024-12-16T14:30:00Z",
        "merchant": "Unknown Online Store", 
        "amount": 299.99,
        "transaction_type": "Card-Not-Present",
        "user_id": "user_12345"
    }
    
    result = asyncio.run(agent.execute(sample_alert))
    analysis = result["analysis"]
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TAMS AI-Assist Demo</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
        .alert-card {{ background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .stage-card {{ background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .stage-title {{ color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; margin-bottom: 15px; }}
        .risk-score {{ text-align: center; margin: 20px 0; }}
        .risk-circle {{ width: 80px; height: 80px; border-radius: 50%; background-color: #dc3545; color: white; display: inline-flex; align-items: center; justify-content: center; font-size: 32px; font-weight: bold; }}
        .final-recommendation {{ background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; padding: 20px; border-radius: 10px; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }}
        @media (max-width: 768px) {{ .grid {{ grid-template-columns: 1fr; }} }}
        .metric {{ text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 5px; }}
        .status-badge {{ padding: 5px 15px; border-radius: 20px; font-weight: bold; display: inline-block; }}
        .high-risk {{ background-color: #dc3545; color: white; }}
        .medium-risk {{ background-color: #ffc107; color: black; }}
        .low-risk {{ background-color: #28a745; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 TAMS AI-Assist - Transaction Analysis Demo</h1>
            <p>3-Stage Fraud Detection System v1.1</p>
        </div>
        
        <div class="alert-card">
            <h2>📊 Transaction Alert Details</h2>
            <div class="grid">
                <div class="metric">
                    <h3>Merchant</h3>
                    <p><strong>{sample_alert['merchant']}</strong></p>
                </div>
                <div class="metric">
                    <h3>Amount</h3>
                    <p><strong>${sample_alert['amount']}</strong></p>
                </div>
                <div class="metric">
                    <h3>Type</h3>
                    <p><strong>{sample_alert['transaction_type']}</strong></p>
                </div>
            </div>
        </div>
        
        <div class="grid">
            <div class="stage-card">
                <h2 class="stage-title">🎯 Stage 1: Genuine Alert Correlation</h2>
                {analysis['stage1_genuine_correlation']['htmlContent']}
                <p><strong>Confidence:</strong> {analysis['stage1_genuine_correlation']['confidenceScore']}</p>
                <p><strong>Rationale:</strong> {analysis['stage1_genuine_correlation']['rationale']}</p>
            </div>
            
            <div class="stage-card">
                <h2 class="stage-title">📊 Stage 2: Behavioral Anomaly Detection</h2>
                {analysis['stage2_behavioral_analysis']['htmlContent']}
            </div>
            
            <div class="stage-card">
                <h2 class="stage-title">⚖️ Stage 3: Comprehensive Risk Assessment</h2>
                {analysis['stage3_risk_assessment']['htmlContent']}
            </div>
        </div>
        
        <div class="final-recommendation">
            <h2>🚨 Final Recommendation</h2>
            <div class="grid">
                <div class="metric">
                    <h3>Classification</h3>
                    <span class="status-badge high-risk">{result['final_recommendation']['final_classification']}</span>
                </div>
                <div class="metric">
                    <h3>Risk Score</h3>
                    <div class="risk-score">
                        <div class="risk-circle">{result['final_recommendation']['overall_risk_score']}</div>
                    </div>
                </div>
                <div class="metric">
                    <h3>Confidence</h3>
                    <span class="status-badge high-risk">{result['final_recommendation']['confidence_level']}</span>
                </div>
            </div>
            
            <h3>📝 Recommended Actions:</h3>
            <ul>
                {"".join([f"<li>{action}</li>" for action in result['final_recommendation']['next_actions']])}
            </ul>
        </div>
        
        <div class="alert-card">
            <h2>⚡ Performance Metrics</h2>
            <div class="grid">
                <div class="metric">
                    <h3>Execution Time</h3>
                    <p><strong>{result['execution_time_ms']}ms</strong></p>
                </div>
                <div class="metric">
                    <h3>Version</h3>
                    <p><strong>{result['version']}</strong></p>
                </div>
                <div class="metric">
                    <h3>Status</h3>
                    <span class="status-badge low-risk">{result['status'].upper()}</span>
                </div>
            </div>
        </div>
        
        <div class="alert-card">
            <h2>🔧 Integration Ready</h2>
            <p>This TAMS AI-Assist system is ready for integration with:</p>
            <ul>
                <li><strong>Frappe ERP:</strong> Direct API integration available</li>
                <li><strong>FlowiseAI:</strong> Visual no-code workflow builder</li>
                <li><strong>REST APIs:</strong> Standard HTTP endpoints</li>
                <li><strong>Webhooks:</strong> Real-time alert processing</li>
            </ul>
            
            <h3>🚀 Next Steps:</h3>
            <ol>
                <li>Configure LLM API keys (OpenAI, Anthropic, etc.)</li>
                <li>Connect to your transaction database</li>
                <li>Customize prompts for your specific use case</li>
                <li>Deploy to production environment</li>
            </ol>
        </div>
    </div>
</body>
</html>
"""
    
    return html_content

def start_web_server():
    """Start simple web server"""
    
    # Create HTML file
    html_content = create_html_demo()
    with open('tams_demo.html', 'w') as f:
        f.write(html_content)
    
    # Start server
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🌐 TAMS Demo Server running at http://localhost:{PORT}")
        print("📱 Opening browser...")
        
        # Open browser
        threading.Timer(1.0, lambda: webbrowser.open(f'http://localhost:{PORT}/tams_demo.html')).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    start_web_server()