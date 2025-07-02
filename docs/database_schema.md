# Database Schema Documentation

## Overview
The AI Agent Platform uses PostgreSQL as the primary database with the following main entities:

## Tables

### Users
Stores user account information and authentication data.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| email | String | Unique email address |
| username | String | Unique username |
| hashed_password | String | Bcrypt hashed password |
| full_name | String | User's full name |
| is_active | Boolean | Account status |
| is_superuser | Boolean | Admin privileges |
| created_at | DateTime | Account creation timestamp |
| updated_at | DateTime | Last update timestamp |

### Agents
Stores AI agent definitions and configurations.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | String | Agent name |
| description | Text | Agent description |
| agent_type | String | automation or assistive |
| status | String | created, running, stopped, error |
| configuration | JSON | Agent-specific settings |
| owner_id | UUID | Foreign key to users |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### Workflows
Stores workflow definitions and templates.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | String | Workflow name |
| description | Text | Workflow description |
| definition | JSON | LangGraph workflow definition |
| version | Integer | Version number |
| is_active | Boolean | Active status |
| owner_id | UUID | Foreign key to users |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### Executions
Tracks agent execution instances and results.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| agent_id | UUID | Foreign key to agents |
| workflow_id | UUID | Foreign key to workflows (optional) |
| status | String | pending, running, completed, failed, cancelled |
| input_data | JSON | Execution input parameters |
| output_data | JSON | Execution results |
| error_message | Text | Error details if failed |
| trace_id | String | LangFuse trace identifier |
| started_at | DateTime | Execution start time |
| completed_at | DateTime | Execution completion time |
| created_at | DateTime | Record creation timestamp |

### Execution Steps
Detailed step-by-step execution tracking.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| execution_id | UUID | Foreign key to executions |
| step_name | String | Step identifier |
| step_type | String | tool, llm_call, decision, etc. |
| input_data | JSON | Step input data |
| output_data | JSON | Step output data |
| error_message | Text | Step error details |
| started_at | DateTime | Step start time |
| completed_at | DateTime | Step completion time |
| created_at | DateTime | Record creation timestamp |

### Tools
Registry of available tools and integrations.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | String | Unique tool name |
| description | Text | Tool description |
| tool_type | String | api, database, file, custom |
| configuration | JSON | Tool-specific configuration |
| is_active | Boolean | Tool availability status |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

## Relationships

- Users have many Agents (one-to-many)
- Users have many Workflows (one-to-many)
- Agents have many Executions (one-to-many)
- Workflows have many Executions (one-to-many)
- Executions have many ExecutionSteps (one-to-many)

## Indexes

Key indexes for performance:
- users.email (unique)
- users.username (unique)
- agents.owner_id
- workflows.owner_id
- executions.agent_id
- executions.workflow_id
- executions.trace_id
- execution_steps.execution_id
- tools.name (unique)