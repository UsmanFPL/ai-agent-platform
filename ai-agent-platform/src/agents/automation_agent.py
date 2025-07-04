from .base import BaseAgent, AgentType, AgentStatus
from ..core.graph import graph_manager, AgentState
from ..tools.base import tool_registry
from typing import Dict, Any, List
import asyncio

class AutomationAgent(BaseAgent):
    """Automation agent for deterministic workflow execution"""
    
    def __init__(self, name: str, workflow_definition: List[Dict[str, Any]], config: Dict[str, Any] = None):
        super().__init__(name, AgentType.AUTOMATION, config)
        self.workflow_definition = workflow_definition
        self.graph = None
        self._setup_graph()
    
    def _setup_graph(self):
        """Setup the LangGraph workflow"""
        # Get required tools
        tools = []
        for step in self.workflow_definition:
            if step.get("tool"):
                tool = tool_registry.get_tool(step["tool"])
                if tool:
                    tools.append(tool)
        
        # Create the automation graph
        self.graph = graph_manager.create_automation_graph(
            name=self.name,
            workflow_steps=self.workflow_definition,
            tools=tools
        )
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the automation workflow"""
        self.start_execution(input_data)
        
        try:
            # Initialize state
            initial_state = AgentState(
                messages=[{"role": "user", "content": str(input_data)}],
                current_step="",
                tools_used=[],
                output={},
                error=""
            )
            
            # Execute the graph
            result = await asyncio.to_thread(self.graph.invoke, initial_state)
            
            # Process result
            output_data = {
                "status": "completed",
                "result": result.get("output", {}),
                "steps_executed": len(result.get("tools_used", [])),
                "tools_used": result.get("tools_used", [])
            }
            
            if result.get("error"):
                output_data["status"] = "failed"
                output_data["error"] = result["error"]
                self.fail_execution(result["error"])
            else:
                self.complete_execution(output_data)
            
            return output_data
            
        except Exception as e:
            error_msg = f"Execution failed: {str(e)}"
            self.fail_execution(error_msg)
            return {
                "status": "failed",
                "error": error_msg
            }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data against workflow requirements"""
        # Check if all required inputs are provided
        required_inputs = self.config.get("required_inputs", [])
        for field in required_inputs:
            if field not in input_data:
                return False
        
        # Validate data types if specified
        input_schema = self.config.get("input_schema", {})
        for field, expected_type in input_schema.items():
            if field in input_data:
                if not isinstance(input_data[field], expected_type):
                    return False
        
        return True

# Example workflow for TAMS automation
TAMS_WORKFLOW = [
    {
        "name": "fetch_alert_data",
        "tool": "database_query",
        "input": {"query": "SELECT * FROM alerts WHERE status = 'new'"},
        "description": "Fetch new alerts from database"
    },
    {
        "name": "analyze_alert",
        "tool": "api_call",
        "input": {"url": "/api/analyze", "method": "POST"},
        "description": "Analyze alert using ML service"
    },
    {
        "name": "update_alert_status",
        "tool": "database_query", 
        "input": {"query": "UPDATE alerts SET status = 'processed' WHERE id = ?"},
        "description": "Update alert status in database"
    }
]

def create_tams_agent() -> AutomationAgent:
    """Create a TAMS automation agent"""
    config = {
        "required_inputs": ["alert_id"],
        "input_schema": {"alert_id": int},
        "max_execution_time": 300  # 5 minutes
    }
    
    return AutomationAgent(
        name="TAMS_Automation_Agent",
        workflow_definition=TAMS_WORKFLOW,
        config=config
    )