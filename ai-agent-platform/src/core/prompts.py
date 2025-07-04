from langchain.prompts import PromptTemplate, ChatPromptTemplate
from typing import Dict, Any

class PromptManager:
    """Centralized prompt management system"""
    
    def __init__(self):
        self.templates = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load default prompt templates"""
        
        # Automation Agent Template
        self.templates["automation_agent"] = ChatPromptTemplate.from_messages([
            ("system", """You are an automation agent designed to execute specific workflows reliably.
            Follow the given workflow steps exactly. If you encounter an error, stop and report it.
            
            Workflow: {workflow}
            Available Tools: {tools}"""),
            ("human", "{input}")
        ])
        
        # Assistive Agent Template
        self.templates["assistive_agent"] = ChatPromptTemplate.from_messages([
            ("system", """You are an assistive agent helping users accomplish their tasks.
            Use the available tools to gather information and provide helpful responses.
            Ask clarifying questions when needed.
            
            Available Tools: {tools}
            Context: {context}"""),
            ("human", "{input}")
        ])
        
        # Tool Execution Template
        self.templates["tool_execution"] = PromptTemplate(
            input_variables=["tool_name", "tool_description", "parameters"],
            template="""Execute the following tool:
            Tool: {tool_name}
            Description: {tool_description}
            Parameters: {parameters}
            
            Provide the result in JSON format."""
        )
    
    def get_template(self, name: str) -> ChatPromptTemplate:
        """Get a prompt template by name"""
        if name not in self.templates:
            raise ValueError(f"Template '{name}' not found")
        return self.templates[name]
    
    def add_template(self, name: str, template: ChatPromptTemplate):
        """Add a new prompt template"""
        self.templates[name] = template
    
    def list_templates(self) -> list:
        """List all available templates"""
        return list(self.templates.keys())

# Global prompt manager instance
prompt_manager = PromptManager()