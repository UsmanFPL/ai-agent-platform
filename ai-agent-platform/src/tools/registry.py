from .base import tool_registry
from .database_tool import DatabaseTool
from .api_tool import APITool
from .file_tool import FileTool
from .email_tool import EmailTool

def initialize_default_tools():
    """Initialize and register default tools"""
    
    # Register database tool
    db_tool = DatabaseTool()
    tool_registry.register(db_tool)
    
    # Register API tool
    api_tool = APITool()
    tool_registry.register(api_tool)
    
    # Register file tool
    file_tool = FileTool()
    tool_registry.register(file_tool)
    
    # Register email tool
    email_tool = EmailTool()
    tool_registry.register(email_tool)
    
    return tool_registry

# Initialize tools when module is imported
initialize_default_tools()