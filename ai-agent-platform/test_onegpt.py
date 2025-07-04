#!/usr/bin/env python3
"""
Test connection to OneGPT FPL Internal API
"""

import asyncio
import aiohttp
import json
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.tams_agent import create_tams_agent

async def test_onegpt_direct():
    """Test direct connection to OneGPT API"""
    
    url = "https://onegpt.fplinternal.in/api/chat/completions"
    token = os.getenv("CUSTOM_LLM_API_KEY", "your-jwt-token-here")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a financial fraud analysis AI assistant. Always respond with valid JSON."},
            {"role": "user", "content": "Test message: Can you respond with a simple JSON object containing status: success?"}
        ],
        "temperature": 0.1,
        "max_tokens": 2000
    }
    
    print("🧪 Testing OneGPT FPL Internal API")
    print("=" * 50)
    print(f"URL: {url}")
    print(f"Model: {payload['model']}")
    print()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
                
                print(f"Status Code: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    print("✅ Connection successful!")
                    print(f"Model: {result.get('model', 'N/A')}")
                    print(f"Response: {result['choices'][0]['message']['content']}")
                    if 'usage' in result:
                        print(f"Tokens: {result['usage'].get('total_tokens', 'N/A')}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Connection failed: HTTP {response.status}")
                    print(f"Error: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        return False

async def test_onegpt_with_tams():
    """Test OneGPT with TAMS agent"""
    
    print("\n🎯 Testing OneGPT with TAMS Agent")
    print("=" * 50)
    
    # Set environment variables for OneGPT
    os.environ["CUSTOM_LLM_URL"] = "https://onegpt.fplinternal.in/api/chat/completions"
    os.environ["CUSTOM_LLM_MODEL"] = "gpt-4o"
    os.environ["CUSTOM_LLM_API_KEY"] = os.getenv("CUSTOM_LLM_API_KEY", "your-jwt-token-here")
    
    # Clear other LLM keys to force custom LLM usage
    os.environ["OPENAI_API_KEY"] = ""
    os.environ["ANTHROPIC_API_KEY"] = ""
    
    sample_alert = {
        "timestamp": "2024-12-16T14:30:00Z",
        "merchant": "Unknown Online Store",
        "amount": 299.99,
        "transaction_type": "Card-Not-Present",
        "user_id": "user_12345"
    }
    
    try:
        agent = create_tams_agent()
        print("Agent created successfully")
        
        print("Running TAMS 3-stage analysis with OneGPT...")
        result = await agent.execute(sample_alert)
        
        if result.get("status") == "completed":
            final_rec = result["final_recommendation"]
            print("✅ TAMS analysis completed successfully!")
            print(f"Classification: {final_rec['final_classification']}")
            print(f"Risk Score: {final_rec['overall_risk_score']}/10")
            print(f"Confidence: {final_rec['confidence_level']}")
            
            # Show stage results
            analysis = result["analysis"]
            stage1 = analysis.get('stage1_genuine_correlation', {})
            stage2 = analysis.get('stage2_behavioral_analysis', {})
            stage3 = analysis.get('stage3_risk_assessment', {})
            
            print(f"\nStage Results:")
            print(f"  Stage 1: {stage1.get('classification', 'N/A')}")
            print(f"  Stage 2: {stage2.get('anomalyRating', 'N/A')} Anomaly")
            print(f"  Stage 3: Risk {stage3.get('riskRating', 'N/A')}/10")
            
            return True
        else:
            print(f"❌ TAMS analysis failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ TAMS test failed: {str(e)}")
        return False

async def main():
    """Main test function"""
    
    print("🔗 OneGPT FPL Internal API Connection Test")
    print("=" * 60)
    
    # Test 1: Direct API connection
    direct_success = await test_onegpt_direct()
    
    # Test 2: TAMS integration
    if direct_success:
        tams_success = await test_onegpt_with_tams()
        
        if tams_success:
            print("\n🎉 All tests passed!")
            print("OneGPT is ready for TAMS production use")
            print("\nTo use OneGPT in production:")
            print("export CUSTOM_LLM_URL='https://onegpt.fplinternal.in/api/chat/completions'")
            print("export CUSTOM_LLM_MODEL='gpt-4o'")
            print("export CUSTOM_LLM_API_KEY='your-jwt-token'")
        else:
            print("\n⚠️ Direct connection works but TAMS integration failed")
    else:
        print("\n❌ Direct connection failed - check token and network access")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(main())