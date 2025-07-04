from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from enum import Enum
import uuid
from datetime import datetime

class AgentStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"

class AgentType(Enum):
    AUTOMATION = "automation"
    ASSISTIVE = "assistive"

class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, name: str, agent_type: AgentType, config: Dict[str, Any] = None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.type = agent_type
        self.config = config or {}
        self.status = AgentStatus.IDLE
        self.created_at = datetime.utcnow()
        self.last_execution = None
        self.execution_history = []
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent with given input"""
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data"""
        pass
    
    def start_execution(self, input_data: Dict[str, Any]):
        """Start agent execution"""
        self.status = AgentStatus.RUNNING
        self.last_execution = {
            'id': str(uuid.uuid4()),
            'started_at': datetime.utcnow(),
            'input_data': input_data,
            'status': 'running'
        }
    
    def complete_execution(self, output_data: Dict[str, Any]):
        """Complete agent execution"""
        self.status = AgentStatus.COMPLETED
        if self.last_execution:
            self.last_execution.update({
                'completed_at': datetime.utcnow(),
                'output_data': output_data,
                'status': 'completed'
            })
            self.execution_history.append(self.last_execution)
    
    def fail_execution(self, error: str):
        """Fail agent execution"""
        self.status = AgentStatus.FAILED
        if self.last_execution:
            self.last_execution.update({
                'completed_at': datetime.utcnow(),
                'error': error,
                'status': 'failed'
            })
            self.execution_history.append(self.last_execution)
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'last_execution': self.last_execution,
            'execution_count': len(self.execution_history)
        }

class AgentRegistry:
    """Registry for managing agent instances"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
    
    def register(self, agent: BaseAgent):
        """Register an agent"""
        self.agents[agent.id] = agent
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Get agent by ID"""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List all agents"""
        return [agent.get_status() for agent in self.agents.values()]
    
    def remove_agent(self, agent_id: str):
        """Remove agent from registry"""
        if agent_id in self.agents:
            del self.agents[agent_id]

# Global agent registry
agent_registry = AgentRegistry()