# WellnessMate: Multi-Agent Health & Wellness Assistant

This project is my capstone submission for the Kaggle x Google AI Agents Intensive.

WellnessMate is a multi-agent AI system that:

- Reads a wellness log (sleep, steps, mood, water, workouts, etc.).
- Uses multiple agents (Planner, Analytics, Coach) and custom tools.
- Analyses trends and patterns in the data.
- Generates simple, personalised wellness tips for the user.
- Uses memory, logging, and basic evaluation to demonstrate key agent concepts.

  ## How to Run the WellnessMate Agent API (FastAPI)

This project also includes a simple **Web API** built with **FastAPI** in  
`src/wellness_api.py`. The API exposes the agent as a REST endpoint.

### 1. Install dependencies (Python 3.10+ recommended)

```bash
pip install fastapi uvicorn "pydantic>=2,<3" numpy pandas

