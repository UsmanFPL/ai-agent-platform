from .assistive_agent import AssistiveAgent
from ..core.rag import rag_manager
from ..core.llm import llm_provider
from typing import Dict, Any, List
import asyncio

class EnhancedAssistiveAgent(AssistiveAgent):
    """Enhanced assistive agent with proactive suggestions and learning"""
    
    def __init__(self, name: str, tools: List[str], config: Dict[str, Any] = None):
        super().__init__(name, tools, config)
        self.learning_enabled = config.get("learning_enabled", True) if config else True
        self.proactive_mode = config.get("proactive_mode", False) if config else False
        self.suggestion_threshold = config.get("suggestion_threshold", 0.7) if config else 0.7
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute with enhanced capabilities"""
        try:
            session_id = input_data.get("session_id", "default")
            user_message = input_data.get("message", "")
            
            # Get relevant context from knowledge base
            context = await rag_manager.get_context(user_message, max_tokens=1500)
            
            # Generate proactive suggestions if enabled
            suggestions = []
            if self.proactive_mode:
                suggestions = await self._generate_suggestions(user_message, context)
            
            # Enhanced system prompt with context
            enhanced_prompt = self._get_enhanced_system_prompt(context, suggestions)
            
            # Execute base agent logic with enhancements
            result = await super().execute(input_data)
            
            # Add enhancements to result
            if result.get("status") == "completed":
                result["context_used"] = bool(context)
                result["suggestions"] = suggestions
                result["enhanced_features"] = {
                    "learning_enabled": self.learning_enabled,
                    "proactive_mode": self.proactive_mode
                }
                
                # Learn from interaction if enabled
                if self.learning_enabled:
                    await self._learn_from_interaction(user_message, result["response"], session_id)
            
            return result
            
        except Exception as e:
            return {
                "status": "failed",
                "error": f"Enhanced execution failed: {str(e)}"
            }
    
    async def _generate_suggestions(self, user_message: str, context: str) -> List[Dict[str, Any]]:
        """Generate proactive suggestions based on user message and context"""
        try:
            # Search for similar past interactions
            similar_queries = await rag_manager.search(user_message, k=3, collection_filter="interactions")
            
            suggestions = []
            for result in similar_queries:
                if result["similarity_score"] > self.suggestion_threshold:
                    suggestions.append({
                        "type": "similar_query",
                        "suggestion": result["content"],
                        "confidence": result["similarity_score"]
                    })
            
            # Generate contextual suggestions
            if context:
                contextual_suggestions = await self._generate_contextual_suggestions(user_message, context)
                suggestions.extend(contextual_suggestions)
            
            return suggestions[:3]  # Limit to top 3 suggestions
            
        except Exception as e:
            print(f"Failed to generate suggestions: {e}")
            return []
    
    async def _generate_contextual_suggestions(self, user_message: str, context: str) -> List[Dict[str, Any]]:
        """Generate suggestions based on available context"""
        suggestions = []
        
        # Analyze context for actionable items
        if "alert" in user_message.lower() and "database" in context.lower():
            suggestions.append({
                "type": "action",
                "suggestion": "Would you like me to query the alerts database for recent entries?",
                "confidence": 0.8
            })
        
        if "report" in user_message.lower() and "data" in context.lower():
            suggestions.append({
                "type": "action", 
                "suggestion": "I can help generate a report based on the available data sources.",
                "confidence": 0.75
            })
        
        return suggestions
    
    async def _learn_from_interaction(self, user_message: str, response: str, session_id: str):
        """Learn from user interactions for future improvements"""
        try:
            # Store interaction in knowledge base for future reference
            interaction_doc = f"User: {user_message}\nAssistant: {response}"
            
            await rag_manager.add_text(
                interaction_doc,
                metadata={
                    "type": "interaction",
                    "session_id": session_id,
                    "timestamp": asyncio.get_event_loop().time()
                }
            )
            
        except Exception as e:
            print(f"Failed to learn from interaction: {e}")
    
    def _get_enhanced_system_prompt(self, context: str = "", suggestions: List[Dict[str, Any]] = None) -> str:
        """Get enhanced system prompt with context and suggestions"""
        base_prompt = super()._get_system_prompt()
        
        enhancements = []
        
        if context:
            enhancements.append(f"Relevant Context:\n{context}")
        
        if suggestions:
            suggestion_text = "\n".join([f"- {s['suggestion']}" for s in suggestions])
            enhancements.append(f"Proactive Suggestions:\n{suggestion_text}")
        
        if enhancements:
            enhanced_prompt = f"{base_prompt}\n\n" + "\n\n".join(enhancements)
            enhanced_prompt += "\n\nUse the context and suggestions to provide more helpful and informed responses."
            return enhanced_prompt
        
        return base_prompt
    
    async def get_interaction_analytics(self, session_id: str = None) -> Dict[str, Any]:
        """Get analytics about user interactions"""
        try:
            # Search for interactions
            filter_criteria = "interactions"
            if session_id:
                # This would need enhanced filtering in the RAG system
                interactions = await rag_manager.search("", k=100, collection_filter=filter_criteria)
                interactions = [i for i in interactions if i.get("metadata", {}).get("session_id") == session_id]
            else:
                interactions = await rag_manager.search("", k=100, collection_filter=filter_criteria)
            
            # Analyze interactions
            total_interactions = len(interactions)
            unique_sessions = len(set(i.get("metadata", {}).get("session_id", "unknown") for i in interactions))
            
            # Common topics (simplified analysis)
            topics = {}
            for interaction in interactions:
                content = interaction.get("content", "").lower()
                for word in ["alert", "report", "data", "query", "help"]:
                    if word in content:
                        topics[word] = topics.get(word, 0) + 1
            
            return {
                "total_interactions": total_interactions,
                "unique_sessions": unique_sessions,
                "common_topics": topics,
                "learning_enabled": self.learning_enabled
            }
            
        except Exception as e:
            return {"error": str(e)}

def create_enhanced_tams_assistive_agent() -> EnhancedAssistiveAgent:
    """Create an enhanced TAMS assistive agent"""
    tools = ["database_query", "api_call", "file_operations", "email_operations"]
    config = {
        "max_conversation_length": 50,
        "response_timeout": 30,
        "learning_enabled": True,
        "proactive_mode": True,
        "suggestion_threshold": 0.7
    }
    
    return EnhancedAssistiveAgent(
        name="Enhanced_TAMS_Assistive_Agent",
        tools=tools,
        config=config
    )