import pytest
from src.tools.base import BaseTool, ToolInput, ToolOutput, tool_registry
from src.tools.database_tool import DatabaseTool, DatabaseQueryInput
from src.tools.api_tool import APITool, APICallInput

class TestBaseTool:
    """Test base tool functionality"""
    
    def test_tool_registry(self):
        """Test tool registry functionality"""
        # Create a mock tool
        class MockTool(BaseTool):
            def __init__(self):
                super().__init__("mock_tool", "A mock tool for testing")
            
            async def execute(self, input_data):
                return ToolOutput(success=True, data="mock_result")
            
            def get_schema(self):
                return {"type": "object", "properties": {}}
        
        tool = MockTool()
        
        # Register tool
        tool_registry.register(tool)
        
        # Retrieve tool
        retrieved = tool_registry.get_tool("mock_tool")
        assert retrieved == tool
        
        # List tools
        tools = tool_registry.list_tools()
        assert "mock_tool" in tools
        assert tools["mock_tool"] == "A mock tool for testing"

class TestDatabaseTool:
    """Test database tool functionality"""
    
    def test_database_tool_creation(self):
        """Test database tool creation"""
        tool = DatabaseTool()
        assert tool.name == "database_query"
        assert "SQL queries" in tool.description
    
    def test_input_validation(self):
        """Test database tool input validation"""
        tool = DatabaseTool()
        
        # Valid input
        valid_input = {"query": "SELECT * FROM users"}
        assert tool.validate_input(valid_input) == True
        
        # Missing query
        invalid_input = {}
        assert tool.validate_input(invalid_input) == False
    
    @pytest.mark.asyncio
    async def test_query_validation(self):
        """Test SQL query validation"""
        tool = DatabaseTool()
        
        # Valid SELECT query
        select_input = DatabaseQueryInput(query="SELECT * FROM users")
        result = await tool.execute(select_input)
        # Should fail due to no actual database, but should not reject SELECT
        assert "Only SELECT queries are allowed" not in str(result.error) if result.error else True
        
        # Invalid non-SELECT query
        insert_input = DatabaseQueryInput(query="INSERT INTO users VALUES (1, 'test')")
        result = await tool.execute(insert_input)
        assert result.success == False
        assert "Only SELECT queries are allowed" in result.error

class TestAPITool:
    """Test API tool functionality"""
    
    def test_api_tool_creation(self):
        """Test API tool creation"""
        tool = APITool()
        assert tool.name == "api_call"
        assert "HTTP API calls" in tool.description
    
    def test_input_validation(self):
        """Test API tool input validation"""
        tool = APITool()
        
        # Valid input
        valid_input = {"url": "https://api.example.com/data"}
        assert tool.validate_input(valid_input) == True
        
        # Missing URL
        invalid_input = {"method": "GET"}
        assert tool.validate_input(invalid_input) == False
    
    def test_schema(self):
        """Test API tool schema"""
        tool = APITool()
        schema = tool.get_schema()
        
        assert "url" in schema["properties"]
        assert "method" in schema["properties"]
        assert "url" in schema["required"]