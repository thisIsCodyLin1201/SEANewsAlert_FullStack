# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SEANewsAlert_FullStack is a multi-agent AI system for Southeast Asian financial news intelligence, combining Python backend (Agno/FastAPI) with React TypeScript frontend. The system automates news research, analysis, and report distribution via PDF/Excel email attachments.

## Common Development Commands

### Backend (Python/FastAPI)

```bash
# Setup environment and dependencies
cd SEANewsAlert
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r pyproject.toml

# Run FastAPI server (primary)
python -m uvicorn app.main:app --reload --port 8000

# Alternative: Streamlit UI (legacy)
streamlit run workflow.py

# Run tests
pytest tests/ -v
pytest tests/test_workflow.py  # Single test file

# Docker deployment
docker-compose up --build
```

### Frontend (React/TypeScript)

```bash
# Setup and run development server
cd FinancialNewsSearch
npm install
npm run dev  # Runs on http://localhost:5173

# Production build
npm run build

# Linting
npm run lint
```

## High-Level Architecture

### Agent System (Agno Framework)

The system uses four specialized agents orchestrated by a workflow manager:

1. **Research Agent** (`agents/research_agent.py`): Searches 18 trusted Southeast Asian news sources using DuckDuckGo, validates domains, returns structured JSON
2. **Analyst Agent** (`agents/analyst_agent.py`): Transforms raw search results into professional Markdown reports with market insights
3. **Report Generator** (`agents/report_agent.py`): Creates PDF (ReportLab) and Excel (Pandas) files with Chinese font support
4. **Email Agent** (`agents/email_agent.py`): Sends reports via SMTP/TLS with attachments

### API Layer

FastAPI application (`app/main.py`) provides two endpoints:
- `POST /api/tasks/news-report`: Creates background task with UUID
- `GET /api/tasks/{task_id}`: Returns task status, progress (0-100%), and artifacts

Task state management (`app/services/progress.py`) tracks: queued → running → succeeded/failed

### Frontend Architecture

React app polls task status every 2 seconds, displaying:
- Progress bar with current step name
- Real-time status updates
- Download links for completed reports

## Key Configuration

### Environment Variables (.env)

```bash
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4.1-2025-04-14
EMAIL_ADDRESS=sender@gmail.com
EMAIL_PASSWORD=app_specific_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### Agent Configuration

Models and tools are configured in `config.py`:
- OpenAI ChatGPT for analysis
- DuckDuckGo for web search
- 18 trusted news domains (viet-jo.com, cafef.vn, bangkokpost.com, etc.)
- Multi-language support: English, Chinese, Vietnamese, Thai, Malay, Indonesian

## Workflow Execution Flow

```
User Input → Parse Prompt (LLM) → Research (Web Search) →
Analysis (ChatGPT) → Report Generation (PDF/Excel) → Email Delivery
```

Total execution time: ~50 seconds

## Important Implementation Details

### Progress Tracking
- Background tasks update progress via callbacks
- Frontend polls `/api/tasks/{task_id}` endpoint
- Progress states: 20% (parsing), 40% (searching), 60% (analyzing), 80% (generating), 100% (complete)

### Error Handling
- Agent-level try/catch with graceful degradation
- Workflow validates each step before proceeding
- API returns structured error messages with task_id

### Report Generation
- PDF uses Chinese fonts (微軟正黑體 on Windows, Noto Sans on Linux/Mac)
- Excel includes structured data with timestamps
- Files saved to `reports/` directory with timestamp naming

### Email Configuration
- Gmail requires app-specific password (not regular password)
- Supports multiple recipients (comma-separated)
- HTML email body with PDF/Excel attachments

## Testing Approach

Run integration tests to verify complete workflow:
```bash
pytest tests/test_workflow.py::test_complete_workflow -v
```

For agent-specific testing:
```bash
pytest tests/test_agents.py::test_research_agent -v
```

## Common Development Tasks

### Adding a New News Source
1. Update trusted domains in `agents/research_agent.py` TRUSTED_SOURCES list
2. Test with: `pytest tests/test_agents.py::test_research_agent`

### Modifying Report Format
1. Edit Markdown template in `agents/analyst_agent.py`
2. Update PDF styling in `agents/report_agent.py`
3. Test generation: `python -m agents.report_agent`

### Debugging Task Failures
1. Check task status: `GET /api/tasks/{task_id}`
2. Review logs in terminal running uvicorn
3. Inspect `workflow.py` execute() method for step failures

### Updating Email Templates
1. Modify HTML template in `agents/email_agent.py`
2. Test with: `python -m agents.email_agent --test`

## Architecture Principles

- **Agent Independence**: Each agent can be tested/deployed separately
- **Async Processing**: Long-running tasks execute in background
- **Stateless API**: All state stored in task_manager (in-memory)
- **Configuration Externalization**: All settings via environment variables
- **Error Resilience**: Partial failures don't crash entire workflow