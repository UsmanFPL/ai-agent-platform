from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
from ...core.evaluation import evaluation_framework
from ...agents.base import agent_registry

router = APIRouter()

@router.post("/test-suites")
async def create_test_suite(
    name: str,
    test_cases: List[Dict[str, Any]]
):
    """Create a new test suite"""
    try:
        evaluation_framework.create_test_suite(name, test_cases)
        return {
            "status": "success",
            "test_suite": name,
            "test_cases_count": len(test_cases)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create test suite: {str(e)}")

@router.get("/test-suites")
async def list_test_suites():
    """List all available test suites"""
    return {
        "test_suites": list(evaluation_framework.test_suites.keys()),
        "total": len(evaluation_framework.test_suites)
    }

@router.get("/test-suites/{suite_name}")
async def get_test_suite(suite_name: str):
    """Get details of a specific test suite"""
    if suite_name not in evaluation_framework.test_suites:
        raise HTTPException(status_code=404, detail="Test suite not found")
    
    return evaluation_framework.test_suites[suite_name]

@router.post("/evaluate/{agent_id}")
async def evaluate_agent(
    agent_id: str,
    test_suite_name: str,
    metrics: Optional[List[str]] = None
):
    """Evaluate an agent against a test suite"""
    try:
        # Get agent from registry
        agent = agent_registry.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Run evaluation
        results = await evaluation_framework.evaluate_agent(agent, test_suite_name, metrics)
        return results
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

@router.get("/metrics")
async def list_metrics():
    """List all available evaluation metrics"""
    metrics_info = {}
    for name, metric in evaluation_framework.metrics.items():
        metrics_info[name] = {
            "name": metric.name,
            "description": metric.description
        }
    
    return {
        "metrics": metrics_info,
        "total": len(metrics_info)
    }

@router.post("/continuous-evaluation/{agent_id}")
async def start_continuous_evaluation(
    agent_id: str,
    test_suite_name: str,
    interval_minutes: int = 60
):
    """Start continuous evaluation for an agent"""
    try:
        agent = agent_registry.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Start continuous evaluation in background
        import asyncio
        asyncio.create_task(
            evaluation_framework.continuous_evaluation(agent, test_suite_name, interval_minutes)
        )
        
        return {
            "status": "started",
            "agent_id": agent_id,
            "test_suite": test_suite_name,
            "interval_minutes": interval_minutes
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start continuous evaluation: {str(e)}")

@router.get("/health")
async def evaluation_health():
    """Check evaluation system health"""
    return {
        "status": "healthy",
        "metrics_available": len(evaluation_framework.metrics),
        "test_suites_available": len(evaluation_framework.test_suites)
    }