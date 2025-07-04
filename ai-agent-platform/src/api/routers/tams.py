from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ...agents.tams_agent import create_tams_agent
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class TAMSAnalysisRequest(BaseModel):
    timestamp: str
    merchant: str
    amount: float
    transaction_type: str
    user_id: str
    alert_id: str = None

class TAMSAnalysisResponse(BaseModel):
    status: str
    analysis: Dict[str, Any]
    final_recommendation: Dict[str, Any]
    version: str
    execution_time_ms: float = None

# Global TAMS agent instance
tams_agent = create_tams_agent()

@router.post("/analyze", response_model=TAMSAnalysisResponse)
async def analyze_transaction_alert(request: TAMSAnalysisRequest):
    """Analyze a transaction alert using TAMS AI-Assist"""
    try:
        start_time = datetime.now()
        
        # Convert request to dict
        input_data = request.dict()
        
        # Execute TAMS analysis
        result = await tams_agent.execute(input_data)
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        result["execution_time_ms"] = execution_time
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TAMS analysis failed: {str(e)}")

@router.get("/agent/status")
async def get_tams_agent_status():
    """Get TAMS agent status and information"""
    return {
        "agent_name": tams_agent.name,
        "agent_type": tams_agent.type.value,
        "status": tams_agent.status.value,
        "version": tams_agent.version,
        "created_at": tams_agent.created_at.isoformat(),
        "execution_count": len(tams_agent.execution_history)
    }

@router.get("/agent/history")
async def get_tams_execution_history():
    """Get TAMS agent execution history"""
    return {
        "agent_name": tams_agent.name,
        "execution_history": tams_agent.execution_history[-10:],  # Last 10 executions
        "total_executions": len(tams_agent.execution_history)
    }

@router.post("/test")
async def test_tams_analysis():
    """Test TAMS analysis with sample data"""
    sample_data = {
        "timestamp": "2024-12-16T14:30:00Z",
        "merchant": "Unknown Online Store",
        "amount": 299.99,
        "transaction_type": "Card-Not-Present",
        "user_id": "user_12345",
        "alert_id": "alert_67890"
    }
    
    try:
        result = await tams_agent.execute(sample_data)
        return {
            "message": "TAMS test analysis completed",
            "sample_input": sample_data,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TAMS test failed: {str(e)}")

@router.get("/health")
async def tams_health():
    """Check TAMS system health"""
    return {
        "status": "healthy",
        "agent_operational": tams_agent.status.value != "failed",
        "version": tams_agent.version,
        "last_execution": tams_agent.last_execution
    }