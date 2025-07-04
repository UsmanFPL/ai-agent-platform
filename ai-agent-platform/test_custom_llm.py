#!/usr/bin/env python3
"""
Test Custom LLM Implementation
Shows how to use different LLM providers including custom URLs
"""

import os
import asyncio
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.tams_agent import create_tams_agent

async def test_custom_llm():
    """Test TAMS with different LLM configurations"""
    
    print("🧪 Testing Custom LLM Implementation")
    print("=" * 50)
    
    # Test configurations
    test_configs = [
        {
            "name": "OpenAI GPT-4",
            "env_vars": {"OPENAI_API_KEY": "sk-test-key-here"},
            "description": "Uses OpenAI API"
        },
        {
            "name": "Anthropic Claude",
            "env_vars": {"ANTHROPIC_API_KEY": "sk-ant-test-key-here"},
            "description": "Uses Anthropic API"
        },
        {
            "name": "Local Ollama",
            "env_vars": {
                "CUSTOM_LLM_URL": "http://localhost:11434/api/generate",
                "CUSTOM_LLM_MODEL": "llama2"
            },
            "description": "Uses local Ollama server"
        },
        {
            "name": "Custom API",
            "env_vars": {
                "CUSTOM_LLM_URL": "https://your-custom-api.com/v1/chat",
                "CUSTOM_LLM_MODEL": "your-model",
                "CUSTOM_LLM_API_KEY": "your-api-key"
            },
            "description": "Uses custom LLM API endpoint"
        }
    ]
    
    sample_alert = {
        "timestamp": "2024-12-16T14:30:00Z",
        "merchant": "Unknown Online Store",
        "amount": 299.99,
        "transaction_type": "Card-Not-Present",
        "user_id": "user_12345"
    }
    
    for config in test_configs:
        print(f"\n🔧 Testing: {config['name']}")
        print(f"   Description: {config['description']}")
        
        # Set environment variables for this test
        original_env = {}
        for key, value in config['env_vars'].items():
            original_env[key] = os.getenv(key)
            os.environ[key] = value
        
        try:
            # Create agent and test
            agent = create_tams_agent()
            print(f"   Status: Agent created successfully")
            
            # Test a quick analysis (will use fallback if API not available)
            result = await agent.execute(sample_alert)
            
            if result.get("status") == "completed":
                risk_score = result["final_recommendation"]["overall_risk_score"]
                classification = result["final_recommendation"]["final_classification"]
                print(f"   Result: {classification} (Risk: {risk_score}/10)")
                print(f"   ✅ Test passed")
            else:
                print(f"   ⚠️  Analysis failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"   ❌ Test failed: {str(e)}")
        
        # Restore original environment
        for key in config['env_vars'].keys():
            if original_env[key] is not None:
                os.environ[key] = original_env[key]
            elif key in os.environ:
                del os.environ[key]
    
    print("\n" + "=" * 50)
    print("🎯 Custom LLM Configuration Guide:")
    print()
    print("1. **OpenAI Integration:**")
    print("   export OPENAI_API_KEY='sk-your-openai-key'")
    print()
    print("2. **Anthropic Integration:**")
    print("   export ANTHROPIC_API_KEY='sk-ant-your-anthropic-key'")
    print()
    print("3. **Local Ollama:**")
    print("   export CUSTOM_LLM_URL='http://localhost:11434/api/generate'")
    print("   export CUSTOM_LLM_MODEL='llama2'")
    print()
    print("4. **Custom API Endpoint:**")
    print("   export CUSTOM_LLM_URL='https://your-api.com/v1/chat'")
    print("   export CUSTOM_LLM_MODEL='your-model'")
    print("   export CUSTOM_LLM_API_KEY='your-api-key'")
    print()
    print("5. **Azure OpenAI:**")
    print("   export CUSTOM_LLM_URL='https://your-resource.openai.azure.com/openai/deployments/your-deployment/chat/completions?api-version=2023-12-01-preview'")
    print("   export CUSTOM_LLM_API_KEY='your-azure-key'")
    print()
    print("🔧 The system will auto-detect and use the first available provider.")
    print("📊 Fallback responses are used when no LLM is available.")

if __name__ == "__main__":
    asyncio.run(test_custom_llm())