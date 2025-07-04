from .automation_agent import AutomationAgent
from ..core.rag import rag_manager
from ..tools.base import tool_registry
from typing import Dict, Any, List
import asyncio
import json

class EnhancedAutomationAgent(AutomationAgent):
    """Enhanced automation agent with RAG and advanced error handling"""
    
    def __init__(self, name: str, workflow_definition: List[Dict[str, Any]], config: Dict[str, Any] = None):
        super().__init__(name, workflow_definition, config)
        self.knowledge_base = config.get("knowledge_base") if config else None
        self.retry_config = config.get("retry_config", {"max_retries": 3, "backoff_factor": 2}) if config else {"max_retries": 3, "backoff_factor": 2}
        self.context_window = config.get("context_window", 2000) if config else 2000
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute with enhanced features"""
        self.start_execution(input_data)
        
        try:
            # Get relevant context if knowledge base is configured
            context = ""
            if self.knowledge_base and input_data.get("query"):
                context = await rag_manager.get_context(
                    input_data["query"], 
                    max_tokens=self.context_window
                )
            
            # Enhanced execution with retry logic
            result = await self._execute_with_retry(input_data, context)
            
            output_data = {
                "status": "completed",
                "result": result.get("output", {}),
                "steps_executed": len(result.get("tools_used", [])),
                "tools_used": result.get("tools_used", []),
                "context_used": bool(context),
                "retries_used": result.get("retries_used", 0)
            }
            
            if result.get("error"):
                output_data["status"] = "failed"
                output_data["error"] = result["error"]
                self.fail_execution(result["error"])
            else:
                self.complete_execution(output_data)
            
            return output_data
            
        except Exception as e:
            error_msg = f"Enhanced execution failed: {str(e)}"
            self.fail_execution(error_msg)
            return {
                "status": "failed",
                "error": error_msg
            }
    
    async def _execute_with_retry(self, input_data: Dict[str, Any], context: str = "") -> Dict[str, Any]:
        """Execute workflow with retry logic"""
        max_retries = self.retry_config["max_retries"]
        backoff_factor = self.retry_config["backoff_factor"]
        
        for attempt in range(max_retries + 1):
            try:
                # Prepare enhanced input with context
                enhanced_input = input_data.copy()
                if context:
                    enhanced_input["context"] = context
                
                # Execute the workflow
                result = await self._execute_workflow(enhanced_input)
                result["retries_used"] = attempt
                return result
                
            except Exception as e:
                if attempt == max_retries:
                    return {"error": f"Failed after {max_retries} retries: {str(e)}", "retries_used": attempt}
                
                # Wait before retry with exponential backoff
                wait_time = backoff_factor ** attempt
                await asyncio.sleep(wait_time)
    
    async def _execute_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the actual workflow steps"""
        results = []
        tools_used = []
        
        for i, step in enumerate(self.workflow_definition):
            try:
                step_result = await self._execute_step(step, input_data, results)
                results.append(step_result)
                tools_used.append(step.get("tool", "none"))
                
                if not step_result.get("success", True):
                    raise Exception(f"Step {i} failed: {step_result.get('error', 'Unknown error')}")
                
            except Exception as e:
                raise Exception(f"Workflow failed at step {i}: {str(e)}")
        
        return {
            "output": {"steps": results, "final_result": results[-1] if results else {}},
            "tools_used": tools_used
        }
    
    async def _execute_step(self, step: Dict[str, Any], input_data: Dict[str, Any], previous_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        tool_name = step.get("tool")
        
        if not tool_name:
            return {
                "success": True,
                "step_name": step.get("name", "unnamed"),
                "output": step.get("output", {})
            }
        
        tool = tool_registry.get_tool(tool_name)
        if not tool:
            raise Exception(f"Tool '{tool_name}' not found")
        
        tool_input = step.get("input", {}).copy()
        result = await tool.execute(tool_input)
        
        return {
            "success": result.success,
            "step_name": step.get("name", "unnamed"),
            "tool_used": tool_name,
            "output": result.data,
            "error": result.error if not result.success else None
        }