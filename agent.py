"""API 3 - LangGraph agent. Run with: uvicorn agent:app --port 8003 --reload

Ollama decides which API to call: the Addition API (8001) or the Information API (8002).
"""
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

app = FastAPI()


# Tool 1: Call Addition API
@tool
def add_numbers(a: int, b: int):
    """Use this tool when the user wants to add two numbers."""
    r = requests.get("http://127.0.0.1:8001/add",
                     params={"a": a, "b": b})
    return r.json()


# Tool 2: Call Information API
@tool
def get_info(topic: str):
    """Get information about Python, FastAPI, or LangGraph."""
    r = requests.get("http://127.0.0.1:8002/info",
                     params={"topic": topic})
    return r.json()


# Ollama model
tools = [add_numbers, get_info]
model = ChatOllama(model="qwen2.5:7b", temperature=0)
llm = model.bind_tools(tools)


# LangGraph agent node
def agent(state: MessagesState):
    messages = [
        SystemMessage(content="Use the available tools when needed.")
    ] + state["messages"]
    return {"messages": [llm.invoke(messages)]}


# Build LangGraph
graph_builder = StateGraph(MessagesState)
graph_builder.add_node("agent", agent)
graph_builder.add_node("tools", ToolNode(tools))
graph_builder.add_edge(START, "agent")
graph_builder.add_conditional_edges("agent", tools_condition)
graph_builder.add_edge("tools", "agent")
graph = graph_builder.compile()


# Third API: Ask the agent
class Question(BaseModel):
    question: str


@app.post("/ask")
def ask(data: Question):
    result = graph.invoke({
        "messages": [HumanMessage(content=data.question)]
    })
    return {"answer": result["messages"][-1].content}
