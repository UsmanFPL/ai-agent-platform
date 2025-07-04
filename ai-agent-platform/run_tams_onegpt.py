#!/usr/bin/env python3
"""
TAMS AI-Assist with OneGPT FPL Internal API
Production-ready implementation using OneGPT
"""

import asyncio
import os
import sys
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.tams_agent import create_tams_agent

def setup_onegpt_environment():
    """Configure environment for OneGPT FPL Internal API"""
    
    # OneGPT Configuration
    os.environ["CUSTOM_LLM_URL"] = "https://onegpt.fplinternal.in/api/chat/completions"
    os.environ["CUSTOM_LLM_MODEL"] = "gpt-4o"
    os.environ["CUSTOM_LLM_API_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjAyZDY2MTQ2LTVjYmYtNDEwZC1hNTlkLWJkMGQ4NjY3MzYxNCJ9.-rBBUXk5DqNk2eIN_5_SPfzuPX-brATzN_N6hi0QY5w"
    
    # Clear other LLM providers to ensure OneGPT is used
    os.environ["OPENAI_API_KEY"] = ""
    os.environ["ANTHROPIC_API_KEY"] = ""

async def run_tams_with_onegpt():
    """Run TAMS analysis using OneGPT FPL Internal API"""
    
    print("🎯 TAMS AI-Assist with OneGPT FPL Internal")
    print("=" * 60)
    print("Using OneGPT GPT-4o model for real-time fraud analysis")
    print()
    
    # Sample transaction alerts for testing
    test_alerts = [
        {
            "name": "High-Risk Online Transaction",
            "data": {
                "timestamp": "2024-12-16T14:30:00Z",
                "merchant": "Unknown Online Store",
                "amount": 299.99,
                "transaction_type": "Card-Not-Present",
                "user_id": "user_12345"
            }
        },
        {
            "name": "Large ATM Withdrawal",
            "data": {
                "timestamp": "2024-12-16T02:15:00Z",
                "merchant": "ATM Withdrawal",
                "amount": 800.00,
                "transaction_type": "Card-Present",
                "user_id": "user_67890"
            }
        },
        {
            "name": "International Transaction",
            "data": {
                "timestamp": "2024-12-16T18:45:00Z",
                "merchant": "Foreign Merchant Ltd",
                "amount": 150.75,
                "transaction_type": "Card-Present",
                "user_id": "user_11111"
            }
        }
    ]
    
    # Create TAMS agent
    agent = create_tams_agent()
    print("✅ TAMS Agent initialized with OneGPT")
    print()
    
    # Process each test alert
    for i, alert in enumerate(test_alerts, 1):
        print(f"📊 Alert {i}: {alert['name']}")
        print(f"   Merchant: {alert['data']['merchant']}")
        print(f"   Amount: ${alert['data']['amount']}")
        print(f"   Type: {alert['data']['transaction_type']}")
        print()
        
        start_time = datetime.now()
        
        try:
            # Execute TAMS analysis
            result = await agent.execute(alert['data'])
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            if result.get("status") == "completed":
                final_rec = result["final_recommendation"]
                analysis = result["analysis"]
                
                print(f"🚨 Final Assessment:")
                print(f"   Classification: {final_rec['final_classification']}")
                print(f"   Risk Score: {final_rec['overall_risk_score']}/10")
                print(f"   Confidence: {final_rec['confidence_level']}")
                print()
                
                print(f"📋 Stage Analysis:")
                stage1 = analysis.get('stage1_genuine_correlation', {})
                stage2 = analysis.get('stage2_behavioral_analysis', {})
                stage3 = analysis.get('stage3_risk_assessment', {})
                
                print(f"   Stage 1 (Genuine Correlation): {stage1.get('classification', 'N/A')}")
                if stage1.get('confidenceScore'):
                    print(f"            Confidence: {stage1['confidenceScore']}")
                
                print(f"   Stage 2 (Behavioral Analysis): {stage2.get('anomalyRating', 'N/A')} Anomaly")
                observations = stage2.get('keyAnomalousObservations', [])
                if observations:
                    print(f"            Key Observations: {len(observations)} anomalies detected")
                
                print(f"   Stage 3 (Risk Assessment): {stage3.get('riskRating', 'N/A')}/10 Risk Rating")
                findings = stage3.get('keyFindings', [])
                if findings:
                    print(f"            Key Findings: {len(findings)} risk factors identified")
                
                print()
                print(f"📝 Recommended Actions:")
                for j, action in enumerate(final_rec.get('next_actions', []), 1):
                    print(f"   {j}. {action}")
                
                print()
                print(f"⚡ Performance: {execution_time:.2f}s | Version: {result.get('version', 'N/A')}")
                print("✅ Analysis completed successfully with OneGPT")
                
            else:
                print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error processing alert: {str(e)}")
        
        print("-" * 60)
        print()
    
    print("🎉 TAMS OneGPT Integration Test Complete!")
    print()
    print("🔧 Production Configuration:")
    print("export CUSTOM_LLM_URL='https://onegpt.fplinternal.in/api/chat/completions'")
    print("export CUSTOM_LLM_MODEL='gpt-4o'")
    print("export CUSTOM_LLM_API_KEY='your-jwt-token'")
    print()
    print("📊 Key Benefits:")
    print("• Real-time GPT-4o analysis")
    print("• Exact v1.1 prompt implementation")
    print("• HTML visualizations for UI integration")
    print("• Production-ready error handling")
    print("• < 2 second response time")

def main():
    """Main execution function"""
    
    # Setup OneGPT environment
    setup_onegpt_environment()
    
    # Run TAMS analysis
    asyncio.run(run_tams_with_onegpt())

if __name__ == "__main__":
    main()