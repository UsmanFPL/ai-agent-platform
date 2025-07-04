#!/usr/bin/env python3
"""
Start API Server Only - Minimal FastAPI server for TAMS
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.tams_agent import create_tams_agent

# Setup OneGPT environment
os.environ["CUSTOM_LLM_URL"] = "https://onegpt.fplinternal.in/api/chat/completions"
os.environ["CUSTOM_LLM_MODEL"] = "gpt-4o"
os.environ["CUSTOM_LLM_API_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjAyZDY2MTQ2LTVjYmYtNDEwZC1hNTlkLWJkMGQ4NjY3MzYxNCJ9.-rBBUXk5DqNk2eIN_5_SPfzuPX-brATzN_N6hi0QY5w"

app = FastAPI(title="AI Agent Platform API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TAMSRequest(BaseModel):
    timestamp: str
    merchant: str
    amount: float
    transaction_type: str
    user_id: str

@app.get("/")
async def root():
    return {"message": "AI Agent Platform API", "status": "online"}

@app.get("/api/v1/health/")
async def health():
    return {"status": "healthy", "agents": ["TAMS_AI_Assist"]}

@app.post("/api/v1/tams/analyze")
async def analyze_tams(request: TAMSRequest):
    try:
        agent = create_tams_agent()
        result = await agent.execute(request.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/tams/test")
async def test_tams():
    try:
        agent = create_tams_agent()
        sample_data = {
            "timestamp": "2024-12-16T14:30:00Z",
            "merchant": "Test Merchant",
            "amount": 199.99,
            "transaction_type": "Card-Not-Present",
            "user_id": "test_user"
        }
        result = await agent.execute(sample_data)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AI Agent Platform API...")
    print("📡 API will be available at: http://localhost:8000")
    print("📚 Documentation at: http://localhost:8000/docs")
    print("🔧 TAMS Analysis: http://localhost:8000/api/v1/tams/analyze")
    uvicorn.run(app, host="0.0.0.0", port=8000)