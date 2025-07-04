from .base import BaseTool, ToolInput, ToolOutput
from typing import Dict, Any
from pydantic import BaseModel
import asyncpg
import os

class DatabaseQueryInput(ToolInput):
    query: str
    parameters: Dict[str, Any] = {}

class DatabaseTool(BaseTool):
    """Tool for executing database queries"""
    
    def __init__(self):
        super().__init__(
            name="database_query",
            description="Execute SQL queries against the database"
        )
        self.connection_string = os.getenv("DATABASE_URL")
    
    async def execute(self, input_data: DatabaseQueryInput) -> ToolOutput:
        """Execute database query"""
        try:
            conn = await asyncpg.connect(self.connection_string)
            
            # Security: Only allow SELECT queries for now
            if not input_data.query.strip().upper().startswith('SELECT'):
                return ToolOutput(
                    success=False,
                    error="Only SELECT queries are allowed"
                )
            
            result = await conn.fetch(input_data.query, *input_data.parameters.values())
            await conn.close()
            
            # Convert result to list of dicts
            data = [dict(row) for row in result]
            
            return ToolOutput(success=True, data=data)
            
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
    
    def get_schema(self) -> Dict[str, Any]:
        """Get tool schema"""
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "SQL SELECT query to execute"
                },
                "parameters": {
                    "type": "object",
                    "description": "Query parameters"
                }
            },
            "required": ["query"]
        }