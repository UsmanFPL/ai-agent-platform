from .base import BaseTool, ToolInput, ToolOutput
from typing import Dict, Any, Optional
from pydantic import BaseModel
import aiohttp
import json

class APICallInput(ToolInput):
    url: str
    method: str = "GET"
    headers: Optional[Dict[str, str]] = None
    data: Optional[Dict[str, Any]] = None

class APITool(BaseTool):
    """Tool for making HTTP API calls"""
    
    def __init__(self):
        super().__init__(
            name="api_call",
            description="Make HTTP API calls to external services"
        )
    
    async def execute(self, input_data: APICallInput) -> ToolOutput:
        """Execute API call"""
        try:
            async with aiohttp.ClientSession() as session:
                kwargs = {
                    'method': input_data.method,
                    'url': input_data.url,
                    'headers': input_data.headers or {}
                }
                
                if input_data.data:
                    if input_data.method.upper() in ['POST', 'PUT', 'PATCH']:
                        kwargs['json'] = input_data.data
                
                async with session.request(**kwargs) as response:
                    if response.content_type == 'application/json':
                        data = await response.json()
                    else:
                        data = await response.text()
                    
                    return ToolOutput(
                        success=response.status < 400,
                        data={
                            'status_code': response.status,
                            'data': data,
                            'headers': dict(response.headers)
                        }
                    )
                    
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
    
    def get_schema(self) -> Dict[str, Any]:
        """Get tool schema"""
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to make the request to"
                },
                "method": {
                    "type": "string",
                    "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"],
                    "description": "HTTP method"
                },
                "headers": {
                    "type": "object",
                    "description": "HTTP headers"
                },
                "data": {
                    "type": "object",
                    "description": "Request body data"
                }
            },
            "required": ["url"]
        }