from crewai import Agent, Task, Crew
from typing import Dict, Any, List, Optional
import asyncio

class CrewAIIntegration:
    """Integration with CrewAI for multi-agent collaboration"""
    
    def __init__(self):
        self.crews = {}
        self.agents = {}
    
    def create_agent(self, name: str, role: str, goal: str, backstory: str, tools: List[Any] = None) -> Agent:
        """Create a CrewAI agent"""
        agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools or [],
            verbose=True,
            allow_delegation=False
        )
        
        self.agents[name] = agent
        return agent
    
    def create_task(self, description: str, agent: Agent, expected_output: str = None) -> Task:
        """Create a task for an agent"""
        return Task(
            description=description,
            agent=agent,
            expected_output=expected_output or "Task completed successfully"
        )
    
    def create_crew(self, name: str, agents: List[Agent], tasks: List[Task], process: str = "sequential") -> Crew:
        """Create a crew of agents with tasks"""
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=process,
            verbose=2
        )
        
        self.crews[name] = crew
        return crew
    
    async def execute_crew(self, crew_name: str, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a crew workflow"""
        if crew_name not in self.crews:
            raise ValueError(f"Crew '{crew_name}' not found")
        
        crew = self.crews[crew_name]
        
        try:
            # Execute crew in a separate thread to avoid blocking
            result = await asyncio.to_thread(crew.kickoff, inputs or {})
            
            return {
                "status": "completed",
                "result": str(result),
                "crew_name": crew_name
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "crew_name": crew_name
            }
    
    def get_crew_status(self, crew_name: str) -> Dict[str, Any]:
        """Get status of a crew"""
        if crew_name not in self.crews:
            return {"error": "Crew not found"}
        
        crew = self.crews[crew_name]
        return {
            "name": crew_name,
            "agents_count": len(crew.agents),
            "tasks_count": len(crew.tasks),
            "process": crew.process
        }
    
    def list_crews(self) -> List[str]:
        """List all available crews"""
        return list(self.crews.keys())

# Example: Employee Onboarding Crew
def create_employee_onboarding_crew(crewai_integration: CrewAIIntegration) -> str:
    """Create a multi-agent crew for employee onboarding"""
    
    # HR Agent
    hr_agent = crewai_integration.create_agent(
        name="hr_specialist",
        role="HR Specialist",
        goal="Handle all HR-related onboarding tasks efficiently",
        backstory="You are an experienced HR professional who ensures smooth employee onboarding processes."
    )
    
    # IT Agent
    it_agent = crewai_integration.create_agent(
        name="it_specialist", 
        role="IT Specialist",
        goal="Set up all technical requirements for new employees",
        backstory="You are a skilled IT professional responsible for provisioning accounts and equipment."
    )
    
    # Finance Agent
    finance_agent = crewai_integration.create_agent(
        name="finance_specialist",
        role="Finance Specialist", 
        goal="Handle payroll setup and financial onboarding",
        backstory="You are a detail-oriented finance professional who manages employee financial setup."
    )
    
    # Create tasks
    hr_task = crewai_integration.create_task(
        description="Create employee record, send welcome email, and schedule orientation",
        agent=hr_agent,
        expected_output="Employee record created and orientation scheduled"
    )
    
    it_task = crewai_integration.create_task(
        description="Create user accounts, assign equipment, and set up access permissions",
        agent=it_agent,
        expected_output="All IT accounts and equipment provisioned"
    )
    
    finance_task = crewai_integration.create_task(
        description="Set up payroll, benefits enrollment, and tax forms",
        agent=finance_agent,
        expected_output="Payroll and benefits configured"
    )
    
    # Create crew
    crew = crewai_integration.create_crew(
        name="employee_onboarding",
        agents=[hr_agent, it_agent, finance_agent],
        tasks=[hr_task, it_task, finance_task],
        process="sequential"
    )
    
    return "employee_onboarding"

# Global CrewAI integration instance
crewai_integration = CrewAIIntegration()

# Initialize example crew
create_employee_onboarding_crew(crewai_integration)