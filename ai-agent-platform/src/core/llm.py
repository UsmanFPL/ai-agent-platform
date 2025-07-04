from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.schema import BaseLanguageModel
from typing import Optional
import os

class LLMProvider:
    """LLM provider abstraction for easy switching between models"""
    
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    def get_openai_chat(self, model: str = "gpt-3.5-turbo", temperature: float = 0.7) -> BaseLanguageModel:
        """Get OpenAI chat model"""
        if not self.openai_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        return ChatOpenAI(
            openai_api_key=self.openai_key,
            model_name=model,
            temperature=temperature
        )
    
    def get_anthropic_chat(self, model: str = "claude-3-sonnet-20240229", temperature: float = 0.7) -> BaseLanguageModel:
        """Get Anthropic chat model"""
        if not self.anthropic_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        return ChatAnthropic(
            anthropic_api_key=self.anthropic_key,
            model=model,
            temperature=temperature
        )
    
    def get_default_llm(self) -> BaseLanguageModel:
        """Get default LLM (OpenAI GPT-3.5-turbo)"""
        try:
            return self.get_openai_chat()
        except ValueError:
            try:
                return self.get_anthropic_chat()
            except ValueError:
                raise ValueError("No LLM API keys found. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY")

# Global LLM provider instance
llm_provider = LLMProvider()