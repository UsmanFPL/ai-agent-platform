import aiohttp
import json
from typing import Dict, Any, List, Optional
import os

class FlowiseIntegration:
    """Integration with FlowiseAI for visual workflow building"""
    
    def __init__(self, flowise_url: str = None):
        self.flowise_url = flowise_url or os.getenv("FLOWISE_URL", "http://localhost:3001")
        self.api_key = os.getenv("FLOWISE_API_KEY")
    
    async def create_chatflow(self, name: str, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a new chatflow in Flowise"""
        chatflow_data = {
            "name": name,
            "flowData": json.dumps({
                "nodes": nodes,
                "edges": edges,
                "viewport": {"x": 0, "y": 0, "zoom": 1}
            }),
            "deployed": False,
            "isPublic": False,
            "apikeyid": "",
            "chatbotConfig": ""
        }
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.flowise_url}/api/v1/chatflows",
                json=chatflow_data,
                headers=headers
            ) as response:
                if response.status == 201:
                    return await response.json()
                else:
                    raise Exception(f"Failed to create chatflow: {response.status}")
    
    async def deploy_chatflow(self, chatflow_id: str) -> Dict[str, Any]:
        """Deploy a chatflow"""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                f"{self.flowise_url}/api/v1/chatflows/{chatflow_id}",
                json={"deployed": True},
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed to deploy chatflow: {response.status}")
    
    async def execute_chatflow(self, chatflow_id: str, message: str, session_id: str = None) -> Dict[str, Any]:
        """Execute a deployed chatflow"""
        data = {"question": message}
        if session_id:
            data["sessionId"] = session_id
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.flowise_url}/api/v1/prediction/{chatflow_id}",
                json=data,
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed to execute chatflow: {response.status}")
    
    def create_custom_tool_node(self, tool_name: str, tool_description: str, tool_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Create a custom tool node for Flowise"""
        return {
            "id": f"customTool_{tool_name}",
            "position": {"x": 0, "y": 0},
            "type": "customNode",
            "data": {
                "id": f"customTool_{tool_name}",
                "label": tool_name,
                "version": 1,
                "name": "customTool",
                "type": "Tool",
                "baseClasses": ["Tool", "StructuredTool"],
                "category": "Custom Tools",
                "description": tool_description,
                "inputParams": [
                    {
                        "label": "Tool Name",
                        "name": "name",
                        "type": "string",
                        "default": tool_name
                    },
                    {
                        "label": "Tool Description", 
                        "name": "description",
                        "type": "string",
                        "default": tool_description
                    },
                    {
                        "label": "Schema",
                        "name": "schema",
                        "type": "json",
                        "default": json.dumps(tool_schema)
                    }
                ],
                "inputs": {
                    "name": tool_name,
                    "description": tool_description,
                    "schema": json.dumps(tool_schema)
                }
            },
            "width": 300,
            "height": 400,
            "selected": False,
            "dragging": False
        }
    
    async def sync_tools_to_flowise(self, tools: Dict[str, Any]) -> List[str]:
        """Sync platform tools to Flowise as custom nodes"""
        synced_tools = []
        
        for tool_name, tool_info in tools.items():
            try:
                # Create custom tool node
                node = self.create_custom_tool_node(
                    tool_name=tool_name,
                    tool_description=tool_info.get("description", ""),
                    tool_schema=tool_info.get("schema", {})
                )
                
                # Register with Flowise (this would require custom Flowise API)
                # For now, we'll just track the created nodes
                synced_tools.append(tool_name)
                
            except Exception as e:
                print(f"Failed to sync tool {tool_name}: {e}")
        
        return synced_tools

# Global Flowise integration instance
flowise_integration = FlowiseIntegration()