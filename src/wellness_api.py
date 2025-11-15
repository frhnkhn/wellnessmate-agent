"""
Simple Web API for the WellnessMate agent.

This is a lightweight version of the notebook logic, wrapped in FastAPI.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import time

# -----------------------------------------------------------------------------
# 1. Dummy wellness data (same style as the notebook)
#    In a real app, this could be replaced with a database or uploaded data.
# -----------------------------------------------------------------------------

data_example = {
    "date": pd.date_range(start="2024-01-01", periods=30, freq="D"),
    "sleep_hours": np.random.uniform(4, 9, 30),
    "steps": np.random.randint(2000, 12000, 30),
    "mood": np.random.randint(1, 6, 30),  # 1 to 5 rating
    "water_glasses": np.random.randint(3, 10, 30),
    "workout_minutes": np.random.randint(0, 60, 30),
}

df = pd.DataFrame(data_example)

# -----------------------------------------------------------------------------
# 2. Simple tools (very similar to the notebook)
# -----------------------------------------------------------------------------

def compute_basic_stats(df):
    metrics = ["sleep_hours", "steps", "mood", "water_glasses", "workout_minutes"]
    stats = {}
    for col in metrics:
        if col in df.columns:
            stats[col] = {
                "mean": float(df[col].mean()),
                "min": float(df[col].min()),
                "max": float(df[col].max()),
            }
    return stats


def compute_correlations(df):
    numeric_df = df.select_dtypes(include=["number"])
    if numeric_df.shape[1] < 2:
        return {}
    return numeric_df.corr().to_dict()


# -----------------------------------------------------------------------------
# 3. Tiny "agents" (much simpler than the full notebook, but same idea)
# -----------------------------------------------------------------------------

def planner_agent(user_query: str):
    """
    Decide what analysis to run based on the user query.
    """
    q = user_query.lower()
    plan = {"steps": []}

    if "trend" in q or "recent" in q or "last" in q:
        plan["steps"].append("basic_stats")

    if "relationship" in q or "effect" in q or "impact" in q or "correlat" in q:
        plan["steps"].append("correlations")

    if not plan["steps"]:
        plan["steps"] = ["basic_stats"]

    return plan


def analytics_agent(plan, df):
    """
    Run the tools based on the plan.
    """
    result = {}
    if "basic_stats" in plan.get("steps", []):
        result["basic_stats"] = compute_basic_stats(df)
    if "correlations" in plan.get("steps", []):
        result["correlations"] = compute_correlations(df)
    return result


def coach_agent(analysis_result):
    """
    Turn analysis into very simple tips.
    """
    tips = []
    stats = analysis_result.get("basic_stats", {})
    sleep_stats = stats.get("sleep_hours")
    mood_stats = stats.get("mood")

    if sleep_stats:
        if sleep_stats["mean"] < 7:
            tips.append("Try to get at least 7 hours of sleep on most nights.")
        else:
            tips.append("Your sleep duration looks okay. Focus on consistency.")

    if mood_stats and mood_stats["mean"] <= 3:
        tips.append("Your average mood is low. Consider relaxing activities and short breaks.")
    elif mood_stats:
        tips.append("Your mood looks fairly positive overall. Keep doing what works for you.")

    if not tips:
        tips.append("Maintain regular sleep, hydration, and gentle movement each day.")

    return tips


def run_wellness_agent(user_query: str):
    """
    End-to-end pipeline: planner -> analytics -> coach.
    Returns a dictionary that can be sent as JSON.
    """
    start = time.time()

    plan = planner_agent(user_query)
    analysis = analytics_agent(plan, df)
    tips = coach_agent(analysis)

    runtime = round(time.time() - start, 3)

    response = {
        "user_query": user_query,
        "plan": plan,
        "analysis": analysis,
        "tips": tips,
        "metrics": {
            "runtime_seconds": runtime,
            "tips_count": len(tips),
        },
    }
    return response


# -----------------------------------------------------------------------------
# 4. FastAPI app
# -----------------------------------------------------------------------------

app = FastAPI(title="WellnessMate Agent API", version="1.0.0")


class WellnessRequest(BaseModel):
    """Schema for incoming requests."""
    user_query: str


@app.get("/")
def root():
    return {"message": "WellnessMate Agent API is running."}


@app.post("/wellness-agent")
def wellness_endpoint(request: WellnessRequest):
    """
    POST /wellness-agent
    JSON body: { "user_query": "..." }
    """
    result = run_wellness_agent(request.user_query)
    return result
