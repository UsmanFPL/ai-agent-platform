# TAMS AI-Assist Usage Guide

## Overview

The TAMS (Transaction Alert Monitoring System) AI-Assist agent implements a sophisticated 3-stage fraud analysis workflow to help analysts quickly assess transaction alerts for potential fraud.

## Features

### 3-Stage Analysis Process

1. **Stage 1: Genuine Alert Correlation**
   - Compares current alert against recent confirmed genuine transactions
   - Filters out alerts from last 24 hours to avoid bias
   - Provides similarity scoring based on merchant, amount, type, and location

2. **Stage 2: Behavioral Anomaly Detection**
   - Analyzes transaction against user's 3-month history
   - Checks for merchant, amount, timing, and type anomalies
   - Provides anomaly rating (Low/Medium/High)

3. **Stage 3: Comprehensive Risk Assessment**
   - Incorporates SOP checklist and risk intelligence data
   - Considers user profile and account information
   - Generates final risk score (1-10) and recommendations

## API Endpoints

### Analyze Transaction Alert
```http
POST /api/v1/tams/analyze
```

**Request Body:**
```json
{
  "timestamp": "2024-12-16T14:30:00Z",
  "merchant": "Unknown Online Store",
  "amount": 299.99,
  "transaction_type": "Card-Not-Present",
  "user_id": "user_12345",
  "alert_id": "alert_67890"
}
```

**Response:**
```json
{
  "status": "completed",
  "analysis": {
    "stage1_genuine_correlation": {
      "classification": "Requires Further Analysis",
      "confidenceScore": "Medium",
      "rationale": "No similar genuine transactions found in recent history",
      "htmlContent": "<div>...</div>"
    },
    "stage2_behavioral_analysis": {
      "classification": "Requires Further Analysis",
      "anomalyRating": "High",
      "keyAnomalousObservations": [
        "New merchant not seen in 3-month history",
        "Transaction amount 3x higher than average"
      ],
      "behavioralSummary": "Transaction shows significant deviation from user patterns",
      "htmlContent": "<div>...</div>"
    },
    "stage3_risk_assessment": {
      "keyFindings": [
        "High-value transaction to unknown merchant",
        "Card-not-present transaction type increases risk"
      ],
      "riskFactors": [
        "New merchant",
        "Above-average amount",
        "Online transaction"
      ],
      "recommendations": [
        "Immediate manual review required",
        "Contact customer for verification"
      ],
      "riskRating": 8,
      "htmlContent": "<div>...</div>"
    }
  },
  "final_recommendation": {
    "final_classification": "High Priority Review",
    "overall_risk_score": 8,
    "confidence_level": "Medium",
    "next_actions": [
      "Immediate manual review required",
      "Contact customer for verification if needed",
      "Consider temporary card block if risk score > 8"
    ]
  },
  "version": "v1.1",
  "execution_time_ms": 1250.5
}
```

### Other Endpoints

- `GET /api/v1/tams/agent/status` - Get agent status
- `GET /api/v1/tams/agent/history` - Get execution history
- `POST /api/v1/tams/test` - Run test analysis
- `GET /api/v1/tams/health` - Health check

## Integration Examples

### Python Client
```python
import requests

# Analyze a transaction alert
alert_data = {
    "timestamp": "2024-12-16T14:30:00Z",
    "merchant": "Suspicious Store",
    "amount": 500.00,
    "transaction_type": "Card-Not-Present",
    "user_id": "user_12345"
}

response = requests.post(
    "http://localhost:8000/api/v1/tams/analyze",
    json=alert_data
)

result = response.json()
print(f"Risk Score: {result['final_recommendation']['overall_risk_score']}")
print(f"Classification: {result['final_recommendation']['final_classification']}")
```

### JavaScript/Node.js Client
```javascript
const axios = require('axios');

async function analyzeTAMSAlert(alertData) {
  try {
    const response = await axios.post(
      'http://localhost:8000/api/v1/tams/analyze',
      alertData
    );
    
    const result = response.data;
    console.log('Risk Score:', result.final_recommendation.overall_risk_score);
    console.log('Classification:', result.final_recommendation.final_classification);
    
    return result;
  } catch (error) {
    console.error('TAMS analysis failed:', error.message);
  }
}

// Usage
const alertData = {
  timestamp: "2024-12-16T14:30:00Z",
  merchant: "Unknown Merchant",
  amount: 299.99,
  transaction_type: "Card-Not-Present",
  user_id: "user_12345"
};

analyzeTAMSAlert(alertData);
```

## Frappe Integration

For integration with Frappe ERP systems:

```python
# frappe_integration.py
import frappe
import requests
from frappe import _

@frappe.whitelist()
def analyze_transaction_alert(alert_doc):
    """Analyze transaction alert using TAMS AI-Assist"""
    
    # Prepare data for TAMS analysis
    tams_data = {
        "timestamp": alert_doc.timestamp,
        "merchant": alert_doc.merchant_name,
        "amount": float(alert_doc.transaction_amount),
        "transaction_type": alert_doc.transaction_type,
        "user_id": alert_doc.user_id,
        "alert_id": alert_doc.name
    }
    
    try:
        # Call TAMS API
        response = requests.post(
            f"{frappe.conf.tams_api_url}/api/v1/tams/analyze",
            json=tams_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Update alert document with analysis
            alert_doc.ai_analysis = frappe.as_json(result)
            alert_doc.risk_score = result['final_recommendation']['overall_risk_score']
            alert_doc.ai_classification = result['final_recommendation']['final_classification']
            alert_doc.save()
            
            return result
        else:
            frappe.log_error(f"TAMS API error: {response.text}")
            return {"error": "TAMS analysis failed"}
            
    except Exception as e:
        frappe.log_error(f"TAMS integration error: {str(e)}")
        return {"error": str(e)}
```

## Performance Considerations

- **Response Time**: Typical analysis completes in 1-3 seconds
- **Rate Limiting**: No built-in rate limiting (implement at API gateway level)
- **Caching**: Consider caching user profiles and risk intelligence data
- **Scaling**: Agent is stateless and can be horizontally scaled

## Monitoring and Alerts

Monitor these key metrics:
- Average response time
- Analysis accuracy rate
- Error rate
- Risk score distribution
- False positive/negative rates

## Troubleshooting

### Common Issues

1. **Slow Response Times**
   - Check LLM API latency
   - Verify database query performance
   - Monitor system resources

2. **Analysis Errors**
   - Validate input data format
   - Check LLM API connectivity
   - Review error logs

3. **Inconsistent Results**
   - Verify prompt templates
   - Check data quality
   - Review model temperature settings

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export TAMS_DEBUG=true
```

This will provide detailed logs of each analysis stage.

## Version History

- **v1.1**: Added 24-hour filtering for genuine alerts
- **v1.0**: Initial 3-stage analysis implementation

## Support

For technical support or feature requests, contact the AI Platform team or create an issue in the project repository.