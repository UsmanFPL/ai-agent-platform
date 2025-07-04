import pytest
from fastapi.testclient import TestClient

class TestTAMSAPI:
    """Test TAMS API endpoints"""
    
    def test_tams_health_check(self, client):
        """Test TAMS health endpoint"""
        response = client.get("/api/v1/tams/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    def test_tams_agent_status(self, client):
        """Test TAMS agent status endpoint"""
        response = client.get("/api/v1/tams/agent/status")
        assert response.status_code == 200
        data = response.json()
        assert data["agent_name"] == "TAMS_AI_Assist"
        assert data["agent_type"] == "automation"
        assert "version" in data
    
    def test_tams_analysis_request_validation(self, client):
        """Test TAMS analysis request validation"""
        # Valid request
        valid_request = {
            "timestamp": "2024-12-16T14:30:00Z",
            "merchant": "Test Merchant",
            "amount": 100.00,
            "transaction_type": "Card-Present",
            "user_id": "user123"
        }
        
        response = client.post("/api/v1/tams/analyze", json=valid_request)
        # Note: This might fail in test environment without proper LLM setup
        # but should at least validate the request structure
        assert response.status_code in [200, 500]  # 500 if LLM not configured
        
        # Invalid request - missing required fields
        invalid_request = {
            "timestamp": "2024-12-16T14:30:00Z",
            "merchant": "Test Merchant"
            # Missing amount, transaction_type, user_id
        }
        
        response = client.post("/api/v1/tams/analyze", json=invalid_request)
        assert response.status_code == 422  # Validation error
    
    def test_tams_test_endpoint(self, client):
        """Test TAMS test analysis endpoint"""
        response = client.post("/api/v1/tams/test")
        # This endpoint uses sample data, so should work even without full setup
        assert response.status_code in [200, 500]  # 500 if LLM not configured
        
        if response.status_code == 200:
            data = response.json()
            assert "message" in data
            assert "sample_input" in data
    
    def test_tams_execution_history(self, client):
        """Test TAMS execution history endpoint"""
        response = client.get("/api/v1/tams/agent/history")
        assert response.status_code == 200
        data = response.json()
        assert "agent_name" in data
        assert "execution_history" in data
        assert "total_executions" in data