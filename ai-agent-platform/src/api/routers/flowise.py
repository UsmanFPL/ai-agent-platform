from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from ...integrations.flowise import flowise_integration
from ...tools.base import tool_registry
import json
import os

router = APIRouter()

@router.post("/sync-tools")
async def sync_tools_to_flowise():
    """Sync platform tools to FlowiseAI"""
    try:
        tools_schema = tool_registry.get_tools_schema()
        tools_info = {}
        
        for tool_name, schema in tools_schema.items():
            tool = tool_registry.get_tool(tool_name)
            if tool:
                tools_info[tool_name] = {
                    "description": tool.description,
                    "schema": schema
                }
        
        synced_tools = await flowise_integration.sync_tools_to_flowise(tools_info)
        
        return {
            "status": "success",
            "synced_tools": synced_tools,
            "total_tools": len(tools_info)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to sync tools: {str(e)}")

@router.post("/chatflows")
async def create_chatflow(
    name: str,
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]]
):
    """Create a new chatflow in FlowiseAI"""
    try:
        result = await flowise_integration.create_chatflow(name, nodes, edges)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create chatflow: {str(e)}")

@router.post("/chatflows/{chatflow_id}/deploy")
async def deploy_chatflow(chatflow_id: str):
    """Deploy a chatflow"""
    try:
        result = await flowise_integration.deploy_chatflow(chatflow_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to deploy chatflow: {str(e)}")

@router.post("/chatflows/{chatflow_id}/execute")
async def execute_chatflow(
    chatflow_id: str,
    message: str,
    session_id: str = None
):
    """Execute a deployed chatflow"""
    try:
        result = await flowise_integration.execute_chatflow(chatflow_id, message, session_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute chatflow: {str(e)}")

@router.post("/workflows/tams/import")
async def import_tams_workflow():
    """Import TAMS workflow into FlowiseAI"""
    try:
        # Load TAMS workflow definition
        workflow_path = os.path.join(os.path.dirname(__file__), "../../../workflows/tams_flowise_workflow.json")
        
        with open(workflow_path, 'r') as f:
            workflow_data = json.load(f)
        
        # Create chatflow in Flowise
        result = await flowise_integration.create_chatflow(
            name="TAMS_AI_Assist_Workflow",
            nodes=workflow_data["nodes"],
            edges=workflow_data["edges"]
        )
        
        return {
            "status": "success",
            "message": "TAMS workflow imported successfully",
            "chatflow_id": result.get("id"),
            "workflow_name": "TAMS_AI_Assist_Workflow"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to import TAMS workflow: {str(e)}")

@router.get("/workflows/tams/definition")
async def get_tams_workflow_definition():
    """Get TAMS workflow definition for FlowiseAI"""
    try:
        workflow_path = os.path.join(os.path.dirname(__file__), "../../../workflows/tams_flowise_workflow.json")
        
        with open(workflow_path, 'r') as f:
            workflow_data = json.load(f)
        
        return {
            "workflow_name": "TAMS_AI_Assist_Workflow",
            "description": "3-stage fraud analysis workflow for transaction alerts",
            "stages": [
                "Stage 1: Genuine Alert Correlation",
                "Stage 2: Behavioral Anomaly Detection", 
                "Stage 3: Comprehensive Risk Assessment"
            ],
            "workflow_definition": workflow_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get workflow definition: {str(e)}")

@router.get("/health")
async def flowise_health():
    """Check FlowiseAI integration health"""
    try:
        # Simple health check by trying to connect
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{flowise_integration.flowise_url}/api/v1/chatflows") as response:
                if response.status == 200:
                    return {"status": "healthy", "flowise_url": flowise_integration.flowise_url}
                else:
                    return {"status": "unhealthy", "error": f"HTTP {response.status}"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}