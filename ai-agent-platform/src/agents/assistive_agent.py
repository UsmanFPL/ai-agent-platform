from .base import BaseAgent, AgentType
from ..core.graph import graph_manager, AgentState
from ..core.llm import llm_provider
from ..core.memory import memory_manager
from ..tools.base import tool_registry
from typing import Dict, Any, List
import asyncio

class AssistiveAgent(BaseAgent):
    """Assistive agent for flexible, conversational interactions"""
    
    def __init__(self, name: str, tools: List[str], config: Dict[str, Any] = None):
        super().__init__(name, AgentType.ASSISTIVE, config)
        self.tools = tools
        self.graph = None
        self.llm = llm_provider.get_default_llm()
        self._setup_graph()
    
    def _setup_graph(self):
        """Setup the ReAct-style LangGraph workflow"""
        # Get required tools
        tool_objects = []
        for tool_name in self.tools:
            tool = tool_registry.get_tool(tool_name)
            if tool:
                tool_objects.append(tool)
        
        # Create the assistive graph
        self.graph = graph_manager.create_assistive_graph(
            name=self.name,
            tools=tool_objects
        )
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the assistive agent conversation"""
        self.start_execution(input_data)
        
        try:
            session_id = input_data.get("session_id", "default")
            user_message = input_data.get("message", "")
            
            # Load conversation memory
            memory = memory_manager.get_buffer_memory(session_id)
            
            # Initialize state
            initial_state = AgentState(
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": user_message}
                ],
                current_step="reasoning",
                tools_used=[],
                output={},
                error=""
            )
            
            # Execute the graph
            result = await asyncio.to_thread(self.graph.invoke, initial_state)
            
            # Extract response
            messages = result.get("messages", [])
            assistant_response = ""
            for msg in reversed(messages):
                if msg.get("role") == "assistant":
                    assistant_response = msg.get("content", "")
                    break
            
            # Save to memory
            memory.chat_memory.add_user_message(user_message)
            memory.chat_memory.add_ai_message(assistant_response)
            memory_manager.save_memory(session_id, memory)
            
            output_data = {
                "status": "completed",
                "response": assistant_response,
                "tools_used": result.get("tools_used", []),
                "session_id": session_id
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
        """Validate input data"""
        # Must have a message
        if "message" not in input_data:
            return False
        
        # Message must be a string
        if not isinstance(input_data["message"], str):
            return False
        
        # Message must not be empty
        if not input_data["message"].strip():
            return False
        
        return True
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the assistive agent"""
        tools_description = "\n".join([
            f"- {tool_name}: {tool_registry.get_tool(tool_name).description}"
            for tool_name in self.tools
            if tool_registry.get_tool(tool_name)
        ])
        
        return f"""You are an AI assistant helping users with their tasks.
        
Available tools:
{tools_description}

Instructions:
1. Listen carefully to the user's request
2. Use available tools when needed to gather information or perform actions
3. Provide helpful, accurate responses
4. Ask clarifying questions if the request is unclear
5. Be concise but thorough in your responses

Always think step by step and explain your reasoning when using tools."""
    
    def add_tool(self, tool_name: str):
        """Add a tool to the agent"""
        if tool_name not in self.tools:
            self.tools.append(tool_name)
            self._setup_graph()  # Recreate graph with new tool
    
    def remove_tool(self, tool_name: str):
        """Remove a tool from the agent"""
        if tool_name in self.tools:
            self.tools.remove(tool_name)
            self._setup_graph()  # Recreate graph
    
    def get_conversation_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a session"""
        memory = memory_manager.get_buffer_memory(session_id)
        return [msg.dict() for msg in memory.chat_memory.messages]
    
    def clear_conversation(self, session_id: str):
        """Clear conversation history for a session"""
        memory_manager.redis_memory.clear_conversation(session_id)

def create_tams_assistive_agent() -> AssistiveAgent:
    """Create a TAMS assistive agent"""
    tools = ["database_query", "api_call"]
    config = {
        "max_conversation_length": 50,
        "response_timeout": 30
    }
    
    return AssistiveAgent(
        name="TAMS_Assistive_Agent",
        tools=tools,
        config=config
    )