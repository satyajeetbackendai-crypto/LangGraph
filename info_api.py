"""API 2 - Information API. Run with: uvicorn info_api:app --port 8002 --reload"""
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Information API")

INFO = {
    "python": "Python is a popular, easy-to-read programming language used for web apps, data science, AI and automation.",
    "fastapi": "FastAPI is a modern Python web framework for building APIs. It uses type hints for validation and generates Swagger docs automatically.",
    "langgraph": "LangGraph is a library for building stateful AI agents as graphs of nodes and edges, such as a model -> tool -> model loop.",
}


@app.get("/info")
def get_info(topic: str):
    key = topic.strip().lower()
    if key not in INFO:
        raise HTTPException(status_code=404,
                            detail=f"No information about '{topic}'. Try: python, fastapi, langgraph.")
    return {"topic": key, "info": INFO[key]}
