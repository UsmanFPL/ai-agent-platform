from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel
import json

class ToolInput(BaseModel):
    """Base class for tool inputs"""
    pass

class ToolOutput(BaseModel):
    """Base class for tool outputs"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

class BaseTool(ABC):
    """Base class for all tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def execute(self, input_data: ToolInput) -> ToolOutput:
        """Execute the tool with given input"""
        pass
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """Get the tool's input schema"""
        pass
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input against schema"""
        try:
            schema = self.get_schema()
            # Basic validation - can be enhanced with jsonschema
            required_fields = schema.get("required", [])
            for field in required_fields:
                if field not in input_data:
                    return False
            return True
        except Exception:
            return False

class ToolRegistry:
    """Registry for managing available tools"""
    
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
    
    def register(self, tool: BaseTool):
        """Register a new tool"""
        self.tools[tool.name] = tool
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> Dict[str, str]:
        """List all available tools"""
        return {name: tool.description for name, tool in self.tools.items()}
    
    def get_tools_schema(self) -> Dict[str, Dict[str, Any]]:
        """Get schemas for all tools"""
        return {name: tool.get_schema() for name, tool in self.tools.items()}

# Global tool registry
tool_registry = ToolRegistry()