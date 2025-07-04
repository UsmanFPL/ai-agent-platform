# TAMS Workflow in FlowiseAI No-Code Builder

## Overview

The TAMS AI-Assist workflow has been designed as a visual, no-code workflow in FlowiseAI that exactly mirrors the 3-stage fraud analysis process described in your prompt specifications.

## Accessing the No-Code Builder

### 1. Start the Platform
```bash
cd ai-agent-platform
./deploy.sh
```

### 2. Access FlowiseAI
- **URL**: http://localhost:3001
- **Username**: admin (default)
- **Password**: admin (default)

### 3. Import TAMS Workflow
```bash
# Import the pre-built TAMS workflow
curl -X POST "http://localhost:8000/api/v1/flowise/workflows/tams/import"
```

## Visual Workflow Structure

The TAMS workflow in FlowiseAI consists of 7 connected nodes:

### 📥 **1. Transaction Alert Input**
- **Type**: Input Node
- **Purpose**: Receives transaction alert data
- **Fields**:
  - Timestamp
  - Merchant
  - Amount
  - Transaction Type
  - User ID

### 🔍 **2. Fetch User Data**
- **Type**: Tool Node
- **Purpose**: Retrieves historical data from database
- **Outputs**:
  - Recent genuine alerts (24h+ filtered)
  - 3-month transaction history
  - User profile data
  - Risk intelligence data

### 🎯 **3. Stage 1: Genuine Alert Correlation**
- **Type**: LLM Chain Node
- **Purpose**: Compares against recent genuine transactions
- **Process**:
  - Filters genuine alerts (24+ hours old)
  - Similarity analysis (merchant, type, amount, location)
  - Classification: "Likely Genuine" or "Requires Further Analysis"
  - Confidence scoring (High/Medium/Low)
  - HTML output generation

### 📊 **4. Stage 2: Behavioral Anomaly Detection**
- **Type**: LLM Chain Node
- **Purpose**: Analyzes behavioral patterns
- **Analysis Areas**:
  - Merchant Analysis (new/unusual merchants)
  - Transaction Amount Analysis (vs. averages)
  - Time & Frequency Analysis (patterns)
  - Transaction Type Analysis (deviations)
- **Outputs**:
  - Anomaly Rating (Low/Medium/High)
  - Key Anomalous Observations
  - Behavioral Summary
  - HTML visualization

### ⚖️ **5. Stage 3: Comprehensive Risk Assessment**
- **Type**: LLM Chain Node
- **Purpose**: Final risk assessment with SOP integration
- **Inputs**:
  - Previous stage results
  - User profile data
  - Risk intelligence data
  - SOP checklist
- **Outputs**:
  - Risk Rating (1-10 scale)
  - Key Findings
  - Risk Factors
  - Recommendations
  - HTML dashboard

### 🧠 **6. Final Recommendation Engine**
- **Type**: Function Node
- **Purpose**: Combines all stages for final decision
- **Logic**:
  - Evaluates all stage classifications
  - Calculates overall confidence
  - Determines priority level
  - Generates next actions

### 📤 **7. TAMS Analysis Output**
- **Type**: Output Node
- **Purpose**: Returns complete analysis result
- **Format**: JSON with HTML visualizations

## Using the No-Code Builder

### Step 1: Open FlowiseAI
1. Navigate to http://localhost:3001
2. Login with default credentials
3. Click "Create New Chatflow"

### Step 2: Import TAMS Workflow
**Option A: API Import**
```bash
curl -X POST "http://localhost:8000/api/v1/flowise/workflows/tams/import"
```

**Option B: Manual Import**
1. Click "Import" in FlowiseAI
2. Upload `/workflows/tams_flowise_workflow.json`
3. The workflow will appear with all nodes connected

### Step 3: Configure Nodes
Each node can be configured by clicking on it:

**LLM Nodes Configuration:**
- Select your preferred LLM (OpenAI GPT-4, Claude, etc.)
- Adjust temperature settings (recommended: 0.1 for consistency)
- Configure API keys in environment variables

**Data Fetch Node:**
- Configure database connection string
- Set up authentication credentials
- Test connection

### Step 4: Test the Workflow
1. Click "Test Chatflow" 
2. Input sample transaction data:
```json
{
  "timestamp": "2024-12-16T14:30:00Z",
  "merchant": "Unknown Online Store",
  "amount": 299.99,
  "transaction_type": "Card-Not-Present",
  "user_id": "user_12345"
}
```
3. View the complete analysis output

### Step 5: Deploy for Production
1. Click "Deploy" to make the workflow live
2. Get the webhook URL for integration
3. Configure in your existing systems

## Visual Flow Diagram

```
[Transaction Input] 
       ↓
[Fetch User Data] ──→ [Stage 1: Genuine Correlation]
       ↓                        ↓
       ├──→ [Stage 2: Behavioral Analysis]
       ↓                        ↓
       └──→ [Stage 3: Risk Assessment] ←──┘
                     ↓
            [Final Recommendation]
                     ↓
              [Analysis Output]
```

## Customization Options

### Modify Prompts
- Click on any LLM node
- Edit the prompt template
- Add custom instructions
- Save changes

### Add New Analysis Stages
- Drag new LLM Chain node
- Connect to existing flow
- Configure custom prompts
- Update final decision logic

### Change LLM Models
- Select different models per stage
- Compare performance
- A/B test different approaches

### Add Custom Tools
- Create new tool nodes
- Integrate with external APIs
- Add database connectors
- Build custom functions

## Integration with Existing Systems

### Frappe Integration
```javascript
// Call FlowiseAI workflow from Frappe
const response = await fetch('http://localhost:3001/api/v1/prediction/CHATFLOW_ID', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: JSON.stringify(transactionData)
  })
});
```

### REST API Integration
```python
import requests

def analyze_with_flowise(transaction_data):
    response = requests.post(
        'http://localhost:3001/api/v1/prediction/CHATFLOW_ID',
        json={'question': json.dumps(transaction_data)}
    )
    return response.json()
```

## Monitoring & Analytics

### Built-in Analytics
- FlowiseAI provides execution logs
- Performance metrics per node
- Error tracking and debugging
- Usage statistics

### Custom Monitoring
- Add logging nodes
- Connect to external monitoring
- Set up alerts for failures
- Track accuracy metrics

## Version Control

### Workflow Versioning
- Export workflow definitions
- Store in version control
- Track changes over time
- Rollback capabilities

### Environment Management
- Development workflows
- Staging environment testing
- Production deployment
- A/B testing different versions

## Troubleshooting

### Common Issues
1. **Node Connection Errors**
   - Check data types match
   - Verify all required inputs connected
   - Test individual nodes

2. **LLM Response Issues**
   - Verify API keys configured
   - Check prompt formatting
   - Monitor token usage

3. **Performance Issues**
   - Optimize prompt lengths
   - Cache frequently used data
   - Use appropriate model sizes

### Debug Mode
- Enable debug logging
- View intermediate outputs
- Step through execution
- Monitor resource usage

## Next Steps

1. **Customize for Your Data**: Modify prompts and logic for your specific transaction patterns
2. **Add More Stages**: Extend with additional analysis stages
3. **Integrate ML Models**: Add custom ML model nodes
4. **Build Dashboards**: Create visualization dashboards
5. **Scale Deployment**: Set up production infrastructure

The TAMS workflow is now fully available in the no-code builder, allowing business analysts to modify and enhance the fraud detection logic without coding!