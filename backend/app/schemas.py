"""
Pydantic schemas for request/response models
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, EmailStr
from uuid import UUID


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Agent schemas
class AgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    agent_type: str
    configuration: Optional[Dict[str, Any]] = None


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None


class Agent(AgentBase):
    id: UUID
    status: str
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Workflow schemas
class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None
    definition: Dict[str, Any]


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    definition: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class Workflow(WorkflowBase):
    id: UUID
    version: int
    is_active: bool
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Execution schemas
class ExecutionBase(BaseModel):
    input_data: Optional[Dict[str, Any]] = None


class ExecutionCreate(ExecutionBase):
    agent_id: UUID
    workflow_id: Optional[UUID] = None


class Execution(ExecutionBase):
    id: UUID
    agent_id: UUID
    workflow_id: Optional[UUID] = None
    status: str
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    trace_id: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Tool schemas
class ToolBase(BaseModel):
    name: str
    description: Optional[str] = None
    tool_type: str
    configuration: Optional[Dict[str, Any]] = None


class ToolCreate(ToolBase):
    pass


class ToolUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class Tool(ToolBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# API Response schemas
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int