from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import os

from ..core.database import engine, Base
from ..tools import registry  # Initialize tools
from .routers import agents, executions, tools, workflows, health, flowise, rag, evaluation, crews, tams

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Agent Platform API",
    description="Internal AI Agent Platform for automation and assistance",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(executions.router, prefix="/api/v1/executions", tags=["executions"])
app.include_router(tools.router, prefix="/api/v1/tools", tags=["tools"])
app.include_router(workflows.router, prefix="/api/v1/workflows", tags=["workflows"])
app.include_router(flowise.router, prefix="/api/v1/flowise", tags=["flowise"])
app.include_router(rag.router, prefix="/api/v1/rag", tags=["rag"])
app.include_router(evaluation.router, prefix="/api/v1/evaluation", tags=["evaluation"])
app.include_router(crews.router, prefix="/api/v1/crews", tags=["crews"])
app.include_router(tams.router, prefix="/api/v1/tams", tags=["tams"])

@app.get("/")
async def root():
    return {"message": "AI Agent Platform API", "version": "0.1.0"}