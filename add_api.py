"""API 1 - Addition API. Run with: uvicorn add_api:app --port 8001 --reload"""
from fastapi import FastAPI

app = FastAPI(title="Addition API")


@app.get("/add")
def add(a: int, b: int):
    return {"a": a, "b": b, "result": a + b}
