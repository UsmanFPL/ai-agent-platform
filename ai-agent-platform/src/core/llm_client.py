"""
Custom LLM Client - Supports any API endpoint
"""

import asyncio
import aiohttp
import json
import os
from typing import Dict, Any, Optional

class CustomLLMClient:
    """Generic LLM client that can work with any API endpoint"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        
        # Default configurations for different providers
        self.providers = {
            "openai": {
                "url": "https://api.openai.com/v1/chat/completions",
                "headers": {"Authorization": "Bearer {api_key}", "Content-Type": "application/json"},
                "payload_format": "openai",
                "model": "gpt-4"
            },
            "anthropic": {
                "url": "https://api.anthropic.com/v1/messages",
                "headers": {"x-api-key": "{api_key}", "Content-Type": "application/json", "anthropic-version": "2023-06-01"},
                "payload_format": "anthropic",
                "model": "claude-3-sonnet-20240229"
            },
            "onegpt": {
                "url": "https://onegpt.fplinternal.in/api/chat/completions",
                "headers": {"Authorization": "Bearer {api_key}", "Content-Type": "application/json", "Accept": "application/json"},
                "payload_format": "openai",
                "model": "gpt-4o"
            },
            "custom": {
                "url": os.getenv("CUSTOM_LLM_URL", "http://localhost:11434/api/generate"),
                "headers": {"Content-Type": "application/json"},
                "payload_format": "ollama",
                "model": os.getenv("CUSTOM_LLM_MODEL", "llama2")
            }
        }
    
    async def call_llm(self, prompt: str, provider: str = None) -> str:
        """Call LLM with specified provider or auto-detect"""
        
        # Auto-detect provider based on available API keys
        if not provider:
            provider = self._detect_provider()
        
        if provider not in self.providers:
            raise ValueError(f"Unsupported provider: {provider}")
        
        config = self.providers[provider]
        
        try:
            payload = self._build_payload(prompt, config)
            headers = self._build_headers(config)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    config["url"],
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        return self._extract_response(result, config["payload_format"])
                    else:
                        error_text = await response.text()
                        raise Exception(f"LLM API error {response.status}: {error_text}")
                        
        except Exception as e:
            print(f"LLM call failed for {provider}: {e}")
            raise
    
    def _detect_provider(self) -> str:
        """Auto-detect which LLM provider to use based on available credentials"""
        
        # Check for OpenAI
        if os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_API_KEY") != "your_openai_key_here":
            return "openai"
        
        # Check for Anthropic
        if os.getenv("ANTHROPIC_API_KEY") and os.getenv("ANTHROPIC_API_KEY") != "your_anthropic_key_here":
            return "anthropic"
        
        # Check for OneGPT (FPL Internal)
        if os.getenv("ONEGPT_JWT_TOKEN"):
            return "onegpt"
        
        # Check for custom LLM URL
        if os.getenv("CUSTOM_LLM_URL"):
            # Special case for OneGPT URL
            if "onegpt.fplinternal.in" in os.getenv("CUSTOM_LLM_URL", ""):
                return "onegpt"
            return "custom"
        
        # Default to custom (local)
        return "custom"
    
    def _build_headers(self, config: Dict[str, Any]) -> Dict[str, str]:
        """Build headers for the request"""
        headers = config["headers"].copy()
        
        # Replace API key placeholders
        for key, value in headers.items():
            if "{api_key}" in value:
                api_key = self._get_api_key(config)
                headers[key] = value.format(api_key=api_key)
        
        return headers
    
    def _get_api_key(self, config: Dict[str, Any]) -> str:
        """Get API key based on provider"""
        if "openai.com" in config["url"]:
            return os.getenv("OPENAI_API_KEY", "")
        elif "anthropic" in config["url"]:
            return os.getenv("ANTHROPIC_API_KEY", "")
        elif "onegpt.fplinternal.in" in config["url"]:
            return os.getenv("ONEGPT_JWT_TOKEN") or os.getenv("CUSTOM_LLM_API_KEY", "")
        else:
            return os.getenv("CUSTOM_LLM_API_KEY", "")
    
    def _build_payload(self, prompt: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Build request payload based on provider format"""
        
        format_type = config["payload_format"]
        model = config["model"]
        
        if format_type == "openai":
            return {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a financial fraud analysis AI assistant. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 2000
            }
        
        elif format_type == "anthropic":
            return {
                "model": model,
                "max_tokens": 2000,
                "temperature": 0.1,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        
        elif format_type == "ollama":
            return {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 2000
                }
            }
        
        else:  # Generic format
            return {
                "prompt": prompt,
                "model": model,
                "temperature": 0.1,
                "max_tokens": 2000
            }
    
    def _extract_response(self, result: Dict[str, Any], format_type: str) -> str:
        """Extract response text based on provider format"""
        
        if format_type == "openai":
            return result["choices"][0]["message"]["content"]
        
        elif format_type == "anthropic":
            return result["content"][0]["text"]
        
        elif format_type == "ollama":
            return result["response"]
        
        else:  # Generic format
            # Try common response fields
            for field in ["response", "text", "content", "output"]:
                if field in result:
                    return result[field]
            
            # If no standard field found, return the whole result as string
            return str(result)

class LLMProvider:
    """Main LLM provider class for TAMS"""
    
    def __init__(self):
        self.client = CustomLLMClient()
        self.fallback_responses = {
            "stage1": {
                "classification": "Requires Further Analysis",
                "confidenceScore": "Medium",
                "rationale": "No similar genuine transactions found in recent 24+ hour history",
                "htmlContent": "<h4 style='color: red; text-align: left;'>⚠️ Requires Further Analysis</h4><table style='width: 100%; background: white; border: 1px solid black;'><tr><th>Attribute</th><th>Current Transaction</th><th>Recent Genuine Transaction</th><th>Comparison Status</th></tr><tr><td>Merchant</td><td>Unknown Online Store</td><td>N/A</td><td style='color: red;'>❌ No Match</td></tr></table>"
            },
            "stage2": {
                "classification": "Requires Further Analysis",
                "anomalyRating": "High",
                "keyAnomalousObservations": ["New merchant not seen in 3-month history", "Transaction amount 3x higher than user average", "Unusual time of day for this user"],
                "behavioralSummary": "Transaction shows significant deviation from established user patterns",
                "htmlContent": "<h4 style='color: black; font-weight: bold;'>Anomaly Rating: <span style='color: red;'>High</span></h4><ul style='font-size: small;'><li>New merchant not seen in 3-month history</li><li>Transaction amount 3x higher than user average</li></ul>"
            },
            "stage3": {
                "keyFindings": ["High-value transaction to unknown merchant", "Multiple behavioral anomalies detected"],
                "riskFactors": ["New merchant", "Above-average transaction amount"],
                "recommendations": ["Immediate manual review required", "Contact customer for verification"],
                "riskRating": 8,
                "htmlContent": "<div style='text-align: center;'><div style='width: 60px; height: 60px; border-radius: 50%; background-color: red; color: white; display: inline-flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold;'>8</div></div>"
            }
        }
    
    async def call_with_fallback(self, prompt: str, stage: str = "stage1") -> str:
        """Call LLM with fallback to mock response"""
        
        try:
            # Try to call real LLM
            response = await self.client.call_llm(prompt)
            return response
            
        except Exception as e:
            print(f"⚠️ LLM call failed, using fallback: {e}")
            # Return fallback response
            return json.dumps(self.fallback_responses.get(stage, {}))

# Global LLM provider instance
llm_provider = LLMProvider()