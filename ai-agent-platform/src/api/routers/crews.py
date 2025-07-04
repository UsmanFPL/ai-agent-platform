from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from ...integrations.crewai import crewai_integration

router = APIRouter()

@router.get("/")
async def list_crews():
    """List all available crews"""
    crews = crewai_integration.list_crews()
    return {
        "crews": crews,
        "total": len(crews)
    }

@router.get("/{crew_name}")
async def get_crew_status(crew_name: str):
    """Get status of a specific crew"""
    status = crewai_integration.get_crew_status(crew_name)
    if "error" in status:
        raise HTTPException(status_code=404, detail=status["error"])
    return status

@router.post("/{crew_name}/execute")
async def execute_crew(crew_name: str, inputs: Dict[str, Any] = None):
    """Execute a crew workflow"""
    try:
        result = await crewai_integration.execute_crew(crew_name, inputs)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crew execution failed: {str(e)}")

@router.get("/health")
async def crews_health():
    """Check crews system health"""
    return {
        "status": "healthy",
        "crews_available": len(crewai_integration.crews),
        "agents_available": len(crewai_integration.agents)
    }