import pytest
from src.agents.base import BaseAgent, AgentType, AgentStatus, agent_registry
from src.agents.automation_agent import AutomationAgent, TAMS_WORKFLOW
from src.agents.assistive_agent import AssistiveAgent

class TestBaseAgent:
    """Test base agent functionality"""
    
    def test_agent_creation(self):
        """Test agent creation and initialization"""
        # Create a mock agent class
        class MockAgent(BaseAgent):
            async def execute(self, input_data):
                return {"result": "mock"}
            
            def validate_input(self, input_data):
                return True
        
        agent = MockAgent("test_agent", AgentType.AUTOMATION)
        
        assert agent.name == "test_agent"
        assert agent.type == AgentType.AUTOMATION
        assert agent.status == AgentStatus.IDLE
        assert agent.id is not None
        assert agent.created_at is not None
    
    def test_agent_registry(self):
        """Test agent registry functionality"""
        class MockAgent(BaseAgent):
            async def execute(self, input_data):
                return {"result": "mock"}
            
            def validate_input(self, input_data):
                return True
        
        agent = MockAgent("test_agent", AgentType.AUTOMATION)
        
        # Register agent
        agent_registry.register(agent)
        
        # Retrieve agent
        retrieved = agent_registry.get_agent(agent.id)
        assert retrieved == agent
        
        # List agents
        agents = agent_registry.list_agents()
        assert len(agents) >= 1
        
        # Remove agent
        agent_registry.remove_agent(agent.id)
        assert agent_registry.get_agent(agent.id) is None

class TestAutomationAgent:
    """Test automation agent functionality"""
    
    def test_automation_agent_creation(self):
        """Test automation agent creation"""
        agent = AutomationAgent("test_automation", TAMS_WORKFLOW)
        
        assert agent.name == "test_automation"
        assert agent.type == AgentType.AUTOMATION
        assert len(agent.workflow_definition) == len(TAMS_WORKFLOW)
    
    def test_workflow_validation(self):
        """Test workflow input validation"""
        config = {
            "required_inputs": ["alert_id"],
            "input_schema": {"alert_id": int}
        }
        agent = AutomationAgent("test_automation", TAMS_WORKFLOW, config)
        
        # Valid input
        assert agent.validate_input({"alert_id": 123}) == True
        
        # Missing required field
        assert agent.validate_input({}) == False
        
        # Wrong type
        assert agent.validate_input({"alert_id": "not_int"}) == False

class TestAssistiveAgent:
    """Test assistive agent functionality"""
    
    def test_assistive_agent_creation(self):
        """Test assistive agent creation"""
        tools = ["database_query", "api_call"]
        agent = AssistiveAgent("test_assistive", tools)
        
        assert agent.name == "test_assistive"
        assert agent.type == AgentType.ASSISTIVE
        assert agent.tools == tools
    
    def test_input_validation(self):
        """Test assistive agent input validation"""
        agent = AssistiveAgent("test_assistive", [])
        
        # Valid input
        assert agent.validate_input({"message": "Hello"}) == True
        
        # Missing message
        assert agent.validate_input({}) == False
        
        # Empty message
        assert agent.validate_input({"message": ""}) == False
        
        # Wrong type
        assert agent.validate_input({"message": 123}) == False