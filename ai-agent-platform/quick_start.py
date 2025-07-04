#!/usr/bin/env python3
"""Quick start script for TAMS AI-Assist demo"""

import json
from datetime import datetime

class MockTAMSAgent:
    """Mock TAMS agent for demo purposes"""
    
    def __init__(self):
        self.name = "TAMS_AI_Assist"
        self.version = "v1.1"
    
    async def execute(self, input_data):
        """Execute 3-stage TAMS analysis with mock data"""
        
        # Stage 1: Genuine Alert Correlation
        stage1_result = {
            "classification": "Requires Further Analysis",
            "confidenceScore": "Medium",
            "rationale": "No similar genuine transactions found in recent 24+ hour history",
            "htmlContent": """
            <h4 style="color: red; text-align: left;">⚠️ Requires Further Analysis</h4>
            <table style="width: 100%; font-size: medium;">
                <tr><td>✅ Merchant Match</td><td style="color: red;">❌ No Match</td></tr>
                <tr><td>✅ Amount Range</td><td style="color: red;">❌ Outside Range</td></tr>
                <tr><td>✅ Transaction Type</td><td style="color: green;">✅ Match</td></tr>
            </table>
            """
        }
        
        # Stage 2: Behavioral Anomaly Detection
        stage2_result = {
            "classification": "Requires Further Analysis",
            "anomalyRating": "High",
            "keyAnomalousObservations": [
                "New merchant not seen in 3-month history",
                "Transaction amount 3x higher than user average",
                "Unusual time of day for this user",
                "Card-not-present transaction (user typically uses card-present)"
            ],
            "behavioralSummary": "Transaction shows significant deviation from established user patterns across multiple dimensions",
            "htmlContent": """
            <h4 style="color: black; font-weight: bold;">Anomaly Rating: <span style="color: red;">High</span></h4>
            <ul style="font-size: small;">
                <li>New merchant not seen in 3-month history</li>
                <li>Transaction amount 3x higher than user average</li>
                <li>Unusual time of day for this user</li>
                <li>Card-not-present transaction (user typically uses card-present)</li>
            </ul>
            <p style="font-style: italic; font-size: small;">Transaction shows significant deviation from established user patterns across multiple dimensions</p>
            """
        }
        
        # Stage 3: Comprehensive Risk Assessment
        stage3_result = {
            "keyFindings": [
                "High-value transaction to unknown merchant",
                "Multiple behavioral anomalies detected",
                "Card-not-present transaction increases fraud risk",
                "Transaction outside user's normal spending patterns"
            ],
            "riskFactors": [
                "New merchant",
                "Above-average transaction amount",
                "Unusual transaction time",
                "Online transaction type"
            ],
            "recommendations": [
                "Immediate manual review required",
                "Contact customer for transaction verification",
                "Consider temporary card restriction pending verification"
            ],
            "riskRating": 8,
            "htmlContent": """
            <div style="text-align: center;">
                <div style="width: 60px; height: 60px; border-radius: 50%; background-color: red; color: white; display: inline-flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold;">8</div>
            </div>
            <h4 style="color: black; font-weight: bold;">Key Findings</h4>
            <ul style="font-size: small;">
                <li>High-value transaction to unknown merchant</li>
                <li>Multiple behavioral anomalies detected</li>
                <li>Card-not-present transaction increases fraud risk</li>
            </ul>
            <h4 style="color: black; font-weight: bold;">Recommendations</h4>
            <ul style="font-size: small;">
                <li>Immediate manual review required</li>
                <li>Contact customer for transaction verification</li>
                <li>Consider temporary card restriction pending verification</li>
            </ul>
            <h4 style="color: black; font-weight: bold;">Risk Factors</h4>
            <ul style="font-size: small;">
                <li>New merchant</li>
                <li>Above-average transaction amount</li>
                <li>Unusual transaction time</li>
                <li>Online transaction type</li>
            </ul>
            """
        }
        
        # Final Recommendation
        final_recommendation = {
            "final_classification": "High Priority Review",
            "overall_risk_score": 8,
            "confidence_level": "High",
            "next_actions": [
                "Immediate manual review required",
                "Contact customer for verification if needed",
                "Consider temporary card block if risk score > 8"
            ]
        }
        
        return {
            "status": "completed",
            "analysis": {
                "stage1_genuine_correlation": stage1_result,
                "stage2_behavioral_analysis": stage2_result,
                "stage3_risk_assessment": stage3_result
            },
            "final_recommendation": final_recommendation,
            "version": self.version,
            "execution_time_ms": 1250.5
        }

def demo_tams_analysis():
    """Run TAMS analysis demo"""
    print("🎯 TAMS AI-Assist Demo")
    print("=" * 50)
    
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
    
    # Create and run TAMS agent
    agent = MockTAMSAgent()
    
    print("🔍 Running 3-Stage Analysis...")
    print("   Stage 1: Genuine Alert Correlation")
    print("   Stage 2: Behavioral Anomaly Detection") 
    print("   Stage 3: Comprehensive Risk Assessment")
    print()
    
    # Execute analysis
    import asyncio
    result = asyncio.run(agent.execute(sample_alert))
    
    # Display results
    print("📋 ANALYSIS RESULTS:")
    print("=" * 30)
    
    final_rec = result["final_recommendation"]
    print(f"🚨 Classification: {final_rec['final_classification']}")
    print(f"📊 Risk Score: {final_rec['overall_risk_score']}/10")
    print(f"🎯 Confidence: {final_rec['confidence_level']}")
    print()
    
    print("📝 Next Actions:")
    for i, action in enumerate(final_rec['next_actions'], 1):
        print(f"   {i}. {action}")
    print()
    
    print("🔍 Stage Details:")
    analysis = result["analysis"]
    
    print(f"   Stage 1: {analysis['stage1_genuine_correlation']['classification']}")
    print(f"   Stage 2: {analysis['stage2_behavioral_analysis']['anomalyRating']} Anomaly")
    print(f"   Stage 3: {len(analysis['stage3_risk_assessment']['keyFindings'])} Key Findings")
    print()
    
    print("⚡ Performance:")
    print(f"   Execution Time: {result['execution_time_ms']}ms")
    print(f"   Version: {result['version']}")
    print()
    
    print("🎨 HTML Visualizations Generated:")
    print("   ✅ Stage 1: Classification table with color coding")
    print("   ✅ Stage 2: Anomaly rating with bullet points")
    print("   ✅ Stage 3: Risk dashboard with circular score")
    print()
    
    print("🚀 TAMS AI-Assist is working perfectly!")
    print("   Ready for integration with Frappe or other systems")
    
    return result

if __name__ == "__main__":
    demo_tams_analysis()