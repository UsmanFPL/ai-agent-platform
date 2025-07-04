from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class AgentBase(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    config: Optional[Dict[Any, Any]] = None

class AgentCreate(AgentBase):
    pass

class AgentResponse(AgentBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ExecutionBase(BaseModel):
    agent_id: int
    input_data: Optional[Dict[Any, Any]] = None

class ExecutionCreate(ExecutionBase):
    pass

class ExecutionResponse(ExecutionBase):
    id: int
    status: str
    output_data: Optional[Dict[Any, Any]] = None
    error_message: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True