from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from typing import Dict, Any, List, TypedDict
import json

class AgentState(TypedDict):
    """State structure for LangGraph agents"""
    messages: List[Dict[str, Any]]
    current_step: str
    tools_used: List[str]
    output: Dict[str, Any]
    error: str

class GraphManager:
    """Manager for LangGraph workflows"""
    
    def __init__(self):
        self.graphs = {}
        self.executors = {}
    
    def create_automation_graph(self, name: str, workflow_steps: List[Dict[str, Any]], tools: List[Any]):
        """Create a state machine graph for automation agents"""
        
        # Create tool executor
        tool_executor = ToolExecutor(tools)
        self.executors[name] = tool_executor
        
        # Define the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes for each workflow step
        for i, step in enumerate(workflow_steps):
            step_name = f"step_{i}"
            workflow.add_node(step_name, self._create_step_node(step, tool_executor))
        
        # Add edges between steps
        for i in range(len(workflow_steps) - 1):
            workflow.add_edge(f"step_{i}", f"step_{i+1}")
        
        # Set entry point and end
        workflow.set_entry_point("step_0")
        workflow.add_edge(f"step_{len(workflow_steps)-1}", END)
        
        # Compile the graph
        graph = workflow.compile()
        self.graphs[name] = graph
        
        return graph
    
    def create_assistive_graph(self, name: str, tools: List[Any]):
        """Create a ReAct-style graph for assistive agents"""
        
        # Create tool executor
        tool_executor = ToolExecutor(tools)
        self.executors[name] = tool_executor
        
        # Define the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", self._agent_node)
        workflow.add_node("action", self._action_node(tool_executor))
        
        # Set entry point
        workflow.set_entry_point("agent")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "action",
                "end": END
            }
        )
        workflow.add_edge("action", "agent")
        
        # Compile the graph
        graph = workflow.compile()
        self.graphs[name] = graph
        
        return graph
    
    def _create_step_node(self, step: Dict[str, Any], tool_executor):
        """Create a node for a workflow step"""
        def step_node(state: AgentState):
            # Execute the step
            try:
                if step.get("tool"):
                    # Use tool
                    result = tool_executor.invoke({
                        "tool": step["tool"],
                        "tool_input": step.get("input", {})
                    })
                    state["output"] = result
                else:
                    # Direct action
                    state["output"] = step.get("output", {})
                
                state["current_step"] = step["name"]
                state["tools_used"].append(step.get("tool", "none"))
                
            except Exception as e:
                state["error"] = str(e)
            
            return state
        
        return step_node
    
    def _agent_node(self, state: AgentState):
        """Agent reasoning node for assistive agents"""
        # This would integrate with LLM for reasoning
        # Simplified for now
        messages = state.get("messages", [])
        
        # Determine if we need to use tools or can respond
        last_message = messages[-1] if messages else {}
        
        if "tool_needed" in last_message.get("content", ""):
            state["messages"].append({
                "role": "assistant",
                "content": "I need to use a tool to help with this request."
            })
        else:
            state["messages"].append({
                "role": "assistant", 
                "content": "I can help you with that directly."
            })
        
        return state
    
    def _action_node(self, tool_executor):
        """Tool execution node"""
        def action_node(state: AgentState):
            # Execute tool based on agent's decision
            # Simplified implementation
            try:
                result = tool_executor.invoke({
                    "tool": "example_tool",
                    "tool_input": {}
                })
                state["output"] = result
            except Exception as e:
                state["error"] = str(e)
            
            return state
        
        return action_node
    
    def _should_continue(self, state: AgentState):
        """Decide whether to continue or end"""
        messages = state.get("messages", [])
        if len(messages) > 10:  # Prevent infinite loops
            return "end"
        
        last_message = messages[-1] if messages else {}
        if "final_answer" in last_message.get("content", ""):
            return "end"
        
        return "continue"
    
    def get_graph(self, name: str):
        """Get a compiled graph by name"""
        return self.graphs.get(name)
    
    def list_graphs(self) -> List[str]:
        """List all available graphs"""
        return list(self.graphs.keys())

# Global graph manager
graph_manager = GraphManager()