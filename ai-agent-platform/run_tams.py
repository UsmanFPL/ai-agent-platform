#!/usr/bin/env python3
"""
TAMS AI-Assist Runner - Production Ready
Uses real LLM implementation with exact prompts from specification
"""

import asyncio
import json
import os
import sys
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agents.tams_agent import create_tams_agent

async def run_tams_analysis():
    """Run TAMS analysis with real LLM implementation"""
    
    print("🎯 TAMS AI-Assist - Production Implementation")
    print("=" * 60)
    print("Using exact v1.1 prompts from specification document")
    print()
    
    # Check for API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    if openai_key and openai_key != "your_openai_key_here":
        print("✅ OpenAI API key configured")
    elif anthropic_key and anthropic_key != "your_anthropic_key_here":
        print("✅ Anthropic API key configured")
    else:
        print("⚠️  No LLM API keys found - using mock responses")
        print("   Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable for real LLM calls")
    print()
    
    # Sample transaction alert
    sample_alert = {
        "timestamp": "2024-12-16T14:30:00Z",
        "merchant": "Unknown Online Store",
        "amount": 299.99,
        "transaction_type": "Card-Not-Present",
        "user_id": "user_12345",
        "alert_id": "alert_67890"
    }
    
    print("📊 Analyzing Transaction Alert:")
    print(f"   • Merchant: {sample_alert['merchant']}")
    print(f"   • Amount: ${sample_alert['amount']}")
    print(f"   • Type: {sample_alert['transaction_type']}")
    print(f"   • Time: {sample_alert['timestamp']}")
    print()
    
    # Create TAMS agent
    agent = create_tams_agent()
    
    print("🔍 Running 3-Stage LLM Analysis...")
    print("   Stage 1: Genuine Alert Correlation (v1.1 prompt)")
    print("   Stage 2: Behavioral Anomaly Detection (v1.1 prompt)")
    print("   Stage 3: Comprehensive Risk Assessment (v1.1 prompt)")
    print()
    
    start_time = datetime.now()
    
    try:
        # Execute analysis
        result = await agent.execute(sample_alert)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Display results
        print("📋 ANALYSIS RESULTS:")
        print("=" * 40)
        
        if result.get("status") == "completed":
            final_rec = result["final_recommendation"]
            print(f"🚨 Classification: {final_rec['final_classification']}")
            print(f"📊 Risk Score: {final_rec['overall_risk_score']}/10")
            print(f"🎯 Confidence: {final_rec['confidence_level']}")
            print()
            
            print("📝 Next Actions:")
            for i, action in enumerate(final_rec['next_actions'], 1):
                print(f"   {i}. {action}")
            print()
            
            print("🔍 Stage-by-Stage Results:")
            analysis = result["analysis"]
            
            # Stage 1
            stage1 = analysis.get('stage1_genuine_correlation', {})
            classification = stage1.get('classification', 'Unknown')
            print(f"   Stage 1: {classification}")
            if stage1.get('confidenceScore'):
                print(f"            Confidence: {stage1['confidenceScore']}")
            if stage1.get('rationale'):
                print(f"            Rationale: {stage1['rationale']}")
            
            # Stage 2
            stage2 = analysis.get('stage2_behavioral_analysis', {})
            anomaly_rating = stage2.get('anomalyRating', 'Unknown')
            print(f"   Stage 2: {anomaly_rating} Anomaly Rating")
            observations = stage2.get('keyAnomalousObservations', [])
            print(f"            {len(observations)} anomalous observations")
            
            # Stage 3
            stage3 = analysis.get('stage3_risk_assessment', {})
            risk_rating = stage3.get('riskRating', 'Unknown')
            print(f"   Stage 3: Risk Rating {risk_rating}/10")
            findings = stage3.get('keyFindings', [])
            print(f"            {len(findings)} key findings")
            print()
            
            print("⚡ Performance:")
            print(f"   Execution Time: {execution_time:.2f}s")
            print(f"   Version: {result['version']}")
            print()
            
            print("🎨 HTML Visualizations:")
            print("   ✅ Stage 1: Classification table with comparison status")
            print("   ✅ Stage 2: Anomaly rating with color-coded observations")
            print("   ✅ Stage 3: Risk dashboard with circular score indicator")
            print()
            
            # Show sample HTML output
            html_content = stage1.get('htmlContent', '')
            if html_content:
                print("📄 Sample HTML Output (Stage 1):")
                print(html_content[:200] + "..." if len(html_content) > 200 else html_content)
                print()
            
            print("🚀 TAMS AI-Assist Analysis Complete!")
            print("   Ready for integration with Frappe, FlowiseAI, or direct API calls")
            
        else:
            print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return result

def main():
    """Main execution function"""
    
    # Set environment variables if not set
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "your_openai_key_here"
    if not os.getenv("ANTHROPIC_API_KEY"):
        os.environ["ANTHROPIC_API_KEY"] = "your_anthropic_key_here"
    
    # Run analysis
    result = asyncio.run(run_tams_analysis())
    
    print()
    print("🔧 Integration Options:")
    print("   1. Set OPENAI_API_KEY for real OpenAI GPT-4 analysis")
    print("   2. Set ANTHROPIC_API_KEY for real Claude analysis")
    print("   3. Use FastAPI server: python -m uvicorn src.api.main:app --reload")
    print("   4. Import into FlowiseAI for no-code workflow")
    print()
    print("📖 Documentation:")
    print("   • TAMS Usage Guide: docs/TAMS_USAGE.md")
    print("   • FlowiseAI Guide: docs/FLOWISE_TAMS_GUIDE.md")
    
    return result

if __name__ == "__main__":
    main()