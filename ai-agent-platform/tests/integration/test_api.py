import pytest
from fastapi.testclient import TestClient

class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "AI Agent Platform API"
        assert data["version"] == "0.1.0"
    
    def test_health_check(self, client):
        """Test basic health check"""
        response = client.get("/health/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "ai-agent-platform"

class TestAgentEndpoints:
    """Test agent management endpoints"""
    
    def test_list_agents_empty(self, client):
        """Test listing agents when none exist"""
        response = client.get("/api/v1/agents/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_create_agent(self, client):
        """Test creating a new agent"""
        agent_data = {
            "name": "test_agent",
            "type": "automation",
            "description": "A test agent",
            "config": {"test": True}
        }
        
        response = client.post("/api/v1/agents/", json=agent_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "test_agent"
        assert data["type"] == "automation"
        assert data["is_active"] == True
    
    def test_get_agent(self, client):
        """Test retrieving a specific agent"""
        # First create an agent
        agent_data = {
            "name": "test_agent_2",
            "type": "assistive",
            "description": "Another test agent"
        }
        
        create_response = client.post("/api/v1/agents/", json=agent_data)
        agent_id = create_response.json()["id"]
        
        # Then retrieve it
        response = client.get(f"/api/v1/agents/{agent_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "test_agent_2"
        assert data["type"] == "assistive"
    
    def test_get_nonexistent_agent(self, client):
        """Test retrieving a non-existent agent"""
        response = client.get("/api/v1/agents/99999")
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()

class TestToolEndpoints:
    """Test tool management endpoints"""
    
    def test_list_tools(self, client):
        """Test listing available tools"""
        response = client.get("/api/v1/tools/")
        assert response.status_code == 200
        # Should return placeholder message for now
        data = response.json()
        assert "tools" in data["message"].lower()

class TestWorkflowEndpoints:
    """Test workflow management endpoints"""
    
    def test_list_workflows(self, client):
        """Test listing available workflows"""
        response = client.get("/api/v1/workflows/")
        assert response.status_code == 200
        # Should return placeholder message for now
        data = response.json()
        assert "workflows" in data["message"].lower()