import pytest
from src.agents.tams_agent import TAMSAgent, create_tams_agent
from src.agents.base import AgentType, AgentStatus

class TestTAMSAgent:
    """Test TAMS AI-Assist agent functionality"""
    
    def test_tams_agent_creation(self):
        """Test TAMS agent creation and initialization"""
        agent = create_tams_agent()
        
        assert agent.name == "TAMS_AI_Assist"
        assert agent.type == AgentType.AUTOMATION
        assert agent.status == AgentStatus.IDLE
        assert agent.version == "v1.1"
    
    def test_input_validation(self):
        """Test TAMS agent input validation"""
        agent = create_tams_agent()
        
        # Valid input
        valid_input = {
            "timestamp": "2024-12-16T14:30:00Z",
            "merchant": "Test Merchant",
            "amount": 100.00,
            "transaction_type": "Card-Present",
            "user_id": "user123"
        }
        assert agent.validate_input(valid_input) == True
        
        # Missing required field
        invalid_input = {
            "timestamp": "2024-12-16T14:30:00Z",
            "merchant": "Test Merchant",
            "amount": 100.00
            # Missing transaction_type and user_id
        }
        assert agent.validate_input(invalid_input) == False
    
    @pytest.mark.asyncio
    async def test_tams_execution_structure(self):
        """Test TAMS agent execution returns proper structure"""
        agent = create_tams_agent()
        
        input_data = {
            "timestamp": "2024-12-16T14:30:00Z",
            "merchant": "Test Merchant",
            "amount": 100.00,
            "transaction_type": "Card-Present",
            "user_id": "user123"
        }
        
        # Mock the LLM responses to avoid actual API calls in tests
        agent._parse_json_response = lambda x: {
            "classification": "Likely Genuine",
            "confidenceScore": "High",
            "rationale": "Test rationale",
            "htmlContent": "<div>Test HTML</div>"
        }
        
        result = await agent.execute(input_data)
        
        # Check result structure
        assert "status" in result
        assert "analysis" in result
        assert "final_recommendation" in result
        assert "version" in result
        
        # Check analysis stages
        analysis = result["analysis"]
        assert "stage1_genuine_correlation" in analysis
        assert "stage2_behavioral_analysis" in analysis
        assert "stage3_risk_assessment" in analysis
    
    def test_json_response_parsing(self):
        """Test JSON response parsing functionality"""
        agent = create_tams_agent()
        
        # Test valid JSON
        valid_json = '{"classification": "Likely Genuine", "confidenceScore": "High"}'
        result = agent._parse_json_response(valid_json)
        assert result["classification"] == "Likely Genuine"
        assert result["confidenceScore"] == "High"
        
        # Test JSON with markdown formatting
        markdown_json = '```json\n{"classification": "Requires Further Analysis"}\n```'
        result = agent._parse_json_response(markdown_json)
        assert result["classification"] == "Requires Further Analysis"
        
        # Test invalid JSON
        invalid_json = '{"invalid": json}'
        result = agent._parse_json_response(invalid_json)
        assert "error" in result
        assert "raw_response" in result
    
    def test_final_recommendation_logic(self):
        """Test final recommendation generation logic"""
        agent = create_tams_agent()
        
        # Test high risk scenario
        stage1 = {"classification": "Requires Further Analysis"}
        stage2 = {"classification": "Requires Further Analysis", "anomalyRating": "High"}
        stage3 = {"riskRating": 8}
        
        recommendation = agent._generate_final_recommendation(stage1, stage2, stage3)
        assert recommendation["final_classification"] == "High Priority Review"
        assert recommendation["overall_risk_score"] == 8
        
        # Test low risk scenario
        stage1 = {"classification": "Likely Genuine", "confidenceScore": "High"}
        stage2 = {"classification": "Likely Genuine", "anomalyRating": "Low"}
        stage3 = {"riskRating": 2}
        
        recommendation = agent._generate_final_recommendation(stage1, stage2, stage3)
        assert recommendation["final_classification"] == "Low Priority - Likely Genuine"
        assert recommendation["overall_risk_score"] == 2
    
    def test_confidence_calculation(self):
        """Test confidence level calculation"""
        agent = create_tams_agent()
        
        # High confidence scenario
        stage1 = {"confidenceScore": "High"}
        stage2 = {"anomalyRating": "Low"}
        stage3 = {}
        
        confidence = agent._calculate_confidence(stage1, stage2, stage3)
        assert confidence == "High"
        
        # Low confidence scenario
        stage1 = {"confidenceScore": "Low"}
        stage2 = {"anomalyRating": "High"}
        stage3 = {}
        
        confidence = agent._calculate_confidence(stage1, stage2, stage3)
        assert confidence == "Low"
    
    def test_next_actions_determination(self):
        """Test next actions determination"""
        agent = create_tams_agent()
        
        # High priority actions
        actions = agent._determine_next_actions("High Priority Review", 9)
        assert "Immediate manual review required" in actions[0]
        assert len(actions) == 3
        
        # Low priority actions
        actions = agent._determine_next_actions("Low Priority - Likely Genuine", 2)
        assert "Mark as reviewed - likely genuine" in actions[0]
        assert len(actions) == 3