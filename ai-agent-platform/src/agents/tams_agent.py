from .base import BaseAgent, AgentType
from ..core.llm_client import llm_provider
from typing import Dict, Any, List
import json
import asyncio
from datetime import datetime, timedelta
import os

class TAMSAgent(BaseAgent):
    """TAMS AI-Assist agent implementing 3-stage fraud analysis"""
    
    def __init__(self, name: str = "TAMS_AI_Assist", config: Dict[str, Any] = None):
        super().__init__(name, AgentType.AUTOMATION, config)
        self.version = config.get("version", "v1.1") if config else "v1.1"
        self.llm_provider = llm_provider
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute 3-stage TAMS analysis"""
        self.start_execution(input_data)
        
        try:
            # Stage 1: Genuine Alert Correlation
            stage1_result = await self._stage1_genuine_correlation(input_data)
            
            # Stage 2: Behavioral Anomaly Detection
            stage2_result = await self._stage2_behavioral_analysis(input_data)
            
            # Stage 3: Comprehensive Risk Assessment
            stage3_result = await self._stage3_risk_assessment(input_data, stage1_result, stage2_result)
            
            # Combine results
            final_result = {
                "status": "completed",
                "analysis": {
                    "stage1_genuine_correlation": stage1_result,
                    "stage2_behavioral_analysis": stage2_result,
                    "stage3_risk_assessment": stage3_result
                },
                "final_recommendation": self._generate_final_recommendation(stage1_result, stage2_result, stage3_result),
                "version": self.version
            }
            
            self.complete_execution(final_result)
            return final_result
            
        except Exception as e:
            error_msg = f"TAMS analysis failed: {str(e)}"
            self.fail_execution(error_msg)
            return {"status": "failed", "error": error_msg}
    
    async def _stage1_genuine_correlation(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 1: Genuine Alert Correlation Analysis using exact v1.1 prompt"""
        
        # Get recent genuine alerts (filtered for 24+ hours old)
        genuine_alerts = await self._get_genuine_alerts(input_data.get("user_id"))
        days_back = 30
        
        # Use exact prompt from v1.1
        prompt = f"""You are a financial fraud analysis AI assistant specializing in identifying genuine transaction patterns.
Analyze the CURRENT TRANSACTION ALERT:
- Timestamp: {input_data.get('timestamp')}
- Merchant: {input_data.get('merchant')}
- Amount: {input_data.get('amount')}
- Transaction Type: {input_data.get('transaction_type')}

Compare it against the following RECENTLY CONFIRMED GENUINE ALERTS (last {days_back} days) for this user/segment:
{json.dumps(genuine_alerts, indent=2)}

TASK:
1.Perform Similarity Analysis (Two-Step Process):
Step 1: Create a Filtered Working Dataset from Genuine Alerts.
Action: From the provided list named "RECENTLY CONFIRMED GENUINE ALERTS", you must create a new, temporary dataset.
Inclusion Criteria: This new dataset should only contain transactions from the original list whose Timestamp is older than 24 hours from the current Timestamp.
Step 2: Compare Against the Filtered Dataset.
Source: Use the filtered working dataset you created in Step 1.
Action: Compare the "CURRENT TRANSACTION ALERT" against each transaction in your working dataset.
Comparison Attributes & Rule: A high degree of similarity is determined by matching the following attributes. If at least three of these four attributes match a single genuine transaction, classify the alert as 'Likely Genuine' with 'High' confidence:
-Merchant
-Transaction Type
-Amount (must be within a +/-10% range)
-Timestamp
2. Classify the CURRENT TRANSACTION ALERT as either 'Likely Genuine' or 'Requires Further Analysis'.
3. If 'Likely Genuine', provide a confidence score (High, Medium, Low) and a brief rationale (e.g., 'Matches 3 out of 4 key attributes with genuine transaction X from {days_back} days ago').
4. Provide a HTML preview code with
    - Classification heading in it with h4 size and start from left alignment and with respective red and green color
    - Tabular format with check marks of acceptance and rejection with full width used in medium font size and keep background of table as white and border as black and add a comparison column with tick mark icon in it for matched status and use Attribute, Current Transaction, Recent Genuine Transaction, Comparison Status columns
    - Add respective danger and acceptance color and styling in it with either red color or green color
    - Don't provide any note in HTML Preview
Respond with a JSON object:
{{
  "classification": "Likely Genuine" | "Requires Further Analysis",
  "confidenceScore": "High" | "Medium" | "Low" | null,
  "rationale": "brief explanation" | null,
  "htmlContent": "HTML Preview of final result"
}}"""

        response = await self.llm_provider.call_with_fallback(prompt, "stage1")
        return self._parse_json_response(response)
    
    async def _stage2_behavioral_analysis(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 2: Behavioral Anomaly Detection using exact v1.1 prompt"""
        
        # Get user transaction history (3 months)
        transaction_history = await self._get_transaction_history(input_data.get("user_id"))
        
        # Use exact prompt from v1.1
        prompt = f"""You are an AI assistant specializing in detecting behavioral anomalies in financial transactions.
Analyze the CURRENT TRANSACTION ALERT by comparing it against the USER'S TRANSACTION HISTORY from the past 3 months.

CURRENT TRANSACTION ALERT:
- Timestamp: {input_data.get('timestamp')}
- Merchant: {input_data.get('merchant')}
- Transaction Amount: {input_data.get('amount')}
- Transaction Type: {input_data.get('transaction_type')}

USER'S TRANSACTION HISTORY (Past 3 Months):
{json.dumps(transaction_history, indent=2)}

TASK:
Based on the provided data, perform the following behavioral checks and provide your assessment:
1.  **Merchant Analysis:**
    * Is the current merchant new for the user compared to the 3-month history?
    * Is the current MCC unusual or a first-time MCC for the user in the last 3 months?
    * If the merchant is not new, is the transaction frequency or amount for this merchant significantly different from past patterns with this merchant?
2.  **Transaction Amount Analysis:**
    * Is the current transaction amount significantly higher or lower than the user's average transaction amount in the last 3 months?
    * Is the amount unusual for this specific MCC based on the user's history with this MCC?
3.  **Time & Frequency Analysis:**
    * Does the time of day/day of week of the current transaction deviate significantly from the user's established patterns in the last 3 months?
    * Is the overall transaction frequency (e.g., multiple transactions today if unusual) notably different from the user's norm?
4.  **Transaction Type Analysis:**
    * Is the current transaction type (e.g., Card-Not-Present vs. Card-Present) a deviation from the user's typical transaction types in the last 3 months?

Based on your analysis of the above points, provide:
- An overall 'anomalyRating' (Low, Medium, High).
- A list of 'keyAnomalousObservations' (bullet points of specific deviations found).
- A 'behavioralSummary' (a brief narrative summarizing how the current transaction compares to the user's 3-month historical behavior).
- Classify the CURRENT TRANSACTION ALERT as either 'Likely Genuine' or 'Requires Further Analysis'.
- Provide a HTML preview code with 
    - Heading of Anomaly Rating with h4 size and black color with bold style and provide text color to rating word with green or yellow or red based on 
      the rating
    - Provide all key observations in bullet points one by one in small text size
    - Provide the behavioral summary at the end with italic style and small text size
    
Respond with a JSON object:
{{
  "classification": "Likely Genuine" | "Requires Further Analysis",
  "anomalyRating": "Low" | "Medium" | "High",
  "keyAnomalousObservations": ["string observation 1", "string observation 2", ...],
  "behavioralSummary": "A brief summary.",
  "htmlContent": "HTML Preview of final result"
}}"""

        response = await self.llm_provider.call_with_fallback(prompt, "stage2")
        return self._parse_json_response(response)
    
    async def _stage3_risk_assessment(self, input_data: Dict[str, Any], stage1_result: Dict[str, Any], stage2_result: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 3: Comprehensive Risk Assessment using exact v1.1 prompt"""
        
        # Get user profile and risk intelligence data
        user_profile = await self._get_user_profile(input_data.get("user_id"))
        risk_intelligence = await self._get_risk_intelligence_data()
        sop_checklist = await self._get_sop_checklist()
        
        # Use exact prompt from v1.1
        prompt = f"""You are a financial fraud analysis AI assistant. Analyze the following alert details and associated data to provide a structured risk assessment.
Consider the preceding Behavioral Anomaly Assessment.

ALERT DETAILS:
- Merchant: {input_data.get('merchant')}
- Transaction Amount: {input_data.get('amount')}
- Transaction Type: {input_data.get('transaction_type')}
- Timestamp: {input_data.get('timestamp')}

BEHAVIORAL ANOMALY ASSESSMENT (from previous analysis step - Rule 2):
- Anomaly Rating: {stage2_result.get('anomalyRating')}
- Key Anomalous Observations: {stage2_result.get('keyAnomalousObservations')}
- Behavioral Summary: {stage2_result.get('behavioralSummary')}

USER PROFILE & HISTORY:
- Credit Limit: {user_profile.get('credit_limit')}
- Outstanding Balance: {user_profile.get('outstanding_balance')}
- User Status: {user_profile.get('user_status')}

RISK INTELLIGENCE DATA:
- High-Risk Merchants: {risk_intelligence.get('high_risk_merchants')}
- High-Risk Countries: {risk_intelligence.get('high_risk_countries')}
- Risky Currencies For User: {risk_intelligence.get('risky_currencies')}
- MCC Risk Data: {risk_intelligence.get('mcc_risk_data')}

STANDARD OPERATING PROCEDURE (SOP) - CHECKLIST FOR ANALYSIS (Rules 3, 4, 5):
Please perform the following checks and use your findings, along with the behavioral anomaly assessment, to inform your overall assessment:
{json.dumps(sop_checklist, indent=2)}

TASK:
1. Analyze this alert and associated data based *strictly* on the SOP checklist provided above, considering the prior behavioral anomaly assessment.
2. Determine the risk level on a scale of 1-10 (1=Very Low, 10=Very High).
3. Provide your analysis in a structured format.

Format your response as a JSON object with these fields:
- 'keyFindings' (array of strings, 3-4 main issues or concerns based on SOP checks and behavioral context)
- 'riskFactors' (array of strings, specific risk factors identified from SOP checks and behavioral context)
- 'recommendations' (array of strings, 2-3 recommended actions for the analyst)
- 'riskRating' (number from 1-10)
- 'htmlContent' (HTML Preview of final result in below structured format)
    - display numeric circular icon with rating number in it with background as per the rating number and align it horizontally centered
    - list all key findings with bullet points - keep heading with h4 size black and bold and bullet points in small text size
    - list all recommendations with bullet points - keep heading with h4 size black and bold and bullet points in small text size
    - list all riskFactors with bullet points - keep heading with h4 size black and bold and bullet points in small text size
    - don't add any extra heading and all except above mentioned points

{{
  "keyFindings": ["finding1", "finding2", ...],
  "riskFactors": ["factor1", "factor2", ...],
  "recommendations": ["rec1", "rec2", ...],
  "riskRating": 1-10,
  "htmlContent": "HTML Preview of final result"
}}"""

        response = await self.llm_provider.call_with_fallback(prompt, "stage3")
        return self._parse_json_response(response)
    
    def _generate_final_recommendation(self, stage1: Dict[str, Any], stage2: Dict[str, Any], stage3: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final recommendation based on all three stages"""
        
        # Determine overall classification
        classifications = [
            stage1.get('classification'),
            stage2.get('classification')
        ]
        
        requires_analysis = any(c == 'Requires Further Analysis' for c in classifications)
        risk_rating = stage3.get('riskRating', 5)
        
        if requires_analysis or risk_rating >= 7:
            final_classification = "High Priority Review"
        elif risk_rating >= 4:
            final_classification = "Medium Priority Review"
        else:
            final_classification = "Low Priority - Likely Genuine"
        
        return {
            "final_classification": final_classification,
            "overall_risk_score": risk_rating,
            "confidence_level": self._calculate_confidence(stage1, stage2, stage3),
            "next_actions": self._determine_next_actions(final_classification, risk_rating)
        }
    
    def _calculate_confidence(self, stage1: Dict[str, Any], stage2: Dict[str, Any], stage3: Dict[str, Any]) -> str:
        """Calculate overall confidence level"""
        confidence_score = stage1.get('confidenceScore', 'Medium')
        anomaly_rating = stage2.get('anomalyRating', 'Medium')
        
        if confidence_score == 'High' and anomaly_rating == 'Low':
            return 'High'
        elif confidence_score == 'Low' or anomaly_rating == 'High':
            return 'Low'
        else:
            return 'Medium'
    
    def _determine_next_actions(self, classification: str, risk_rating: int) -> List[str]:
        """Determine recommended next actions"""
        if classification == "High Priority Review":
            return [
                "Immediate manual review required",
                "Contact customer for verification if needed",
                "Consider temporary card block if risk score > 8"
            ]
        elif classification == "Medium Priority Review":
            return [
                "Schedule for analyst review within 4 hours",
                "Monitor for additional suspicious activity",
                "Review customer contact preferences"
            ]
        else:
            return [
                "Mark as reviewed - likely genuine",
                "Continue standard monitoring",
                "Update customer behavior patterns"
            ]
    
    async def _get_genuine_alerts(self, user_id: str) -> List[Dict[str, Any]]:
        """Get recent genuine alerts for the user (filtered for 24+ hours old)"""
        # Mock data - in production, this would query the database
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        return [
            {
                "timestamp": "2024-12-14T10:30:00Z",
                "merchant": "Amazon",
                "amount": 45.99,
                "transaction_type": "Card-Not-Present",
                "status": "genuine"
            },
            {
                "timestamp": "2024-12-13T15:45:00Z", 
                "merchant": "Starbucks",
                "amount": 12.50,
                "transaction_type": "Card-Present",
                "status": "genuine"
            }
        ]
    
    async def _get_transaction_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's 3-month transaction history"""
        # Mock data - in production, this would query the database
        return [
            {
                "timestamp": "2024-12-10T09:15:00Z",
                "merchant": "Amazon",
                "amount": 67.89,
                "transaction_type": "Card-Not-Present",
                "mcc": "5399"
            },
            {
                "timestamp": "2024-12-09T12:30:00Z",
                "merchant": "Starbucks", 
                "amount": 8.75,
                "transaction_type": "Card-Present",
                "mcc": "5814"
            }
        ]
    
    async def _get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile and account information"""
        # Mock data - in production, this would query the database
        return {
            "credit_limit": 5000.00,
            "outstanding_balance": 1250.00,
            "user_status": "Active",
            "account_age_months": 24,
            "average_monthly_spend": 800.00
        }
    
    async def _get_risk_intelligence_data(self) -> Dict[str, Any]:
        """Get risk intelligence data"""
        # Mock data - in production, this would query risk databases
        return {
            "high_risk_merchants": ["SuspiciousMerchant1", "FraudulentStore2"],
            "high_risk_countries": ["Country1", "Country2"],
            "risky_currencies": ["Currency1"],
            "mcc_risk_data": {
                "5399": "Medium Risk",
                "5814": "Low Risk"
            }
        }
    
    async def _get_sop_checklist(self) -> List[str]:
        """Get Standard Operating Procedure checklist from v1.1 spec"""
        return [
            "Calculate Transaction-Level Credit Utilization: (Current Transaction Amount / Total Credit Limit) * 100. Is this > 70.0%? If so, note as 'High Transaction Credit Utilization'.",
            "Analyze 30 days Total Cumulative Utilization: 30.0%",
            "Analyze Repayment History: Are there frequent late payments, payments of only minimum amount due, or history of defaults/collections? Note any negative patterns.",
            "Consider User Status Classification (Transactor): How does this transaction align with the typical behavior of a Transactor (e.g., a large purchase by an 'Infrequent User' might be more notable)?",
            "Is the transaction merchant present in the provided High-Risk Merchant List?",
            "Analyze Merchant Attributes for Risk:",
            "  - Merchant Location/Country: Is the merchant in a known high-risk country?",
            "  - Transaction Currency: Is the transaction currency unusual for the user or commonly associated with fraud?",
            "  - MCC Risk: Is the MCC inherently high-risk (e.g., money transfers, gambling) or recently associated with fraud trends?"
        ]
    

    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON response from LLM"""
        try:
            # Clean up response text
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            return {
                "error": f"Failed to parse JSON response: {str(e)}",
                "raw_response": response_text
            }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for TAMS analysis"""
        required_fields = ['timestamp', 'merchant', 'amount', 'transaction_type', 'user_id']
        return all(field in input_data for field in required_fields)

def create_tams_agent() -> TAMSAgent:
    """Create a TAMS AI-Assist agent"""
    config = {
        "version": "v1.1",
        "required_inputs": ["timestamp", "merchant", "amount", "transaction_type", "user_id"],
        "max_execution_time": 60
    }
    
    return TAMSAgent("TAMS_AI_Assist", config)