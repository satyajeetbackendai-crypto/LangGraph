# FastAPI + LangGraph agent

Three FastAPI apps. A LangGraph agent running on Ollama decides which of the other two APIs to call.
This follows [codeInfo/FastAPI_LangGraph_Agent_Guide.pdf](codeInfo/FastAPI_LangGraph_Agent_Guide.pdf).

| App | File | Purpose | Address |
|---|---|---|---|
| API 1 | `add_api.py` | Addition (`GET /add?a=10&b=20`) | http://127.0.0.1:8001 |
| API 2 | `info_api.py` | Information (`GET /info?topic=python`) | http://127.0.0.1:8002 |
| API 3 | `agent.py` | LangGraph agent (`POST /ask`) | http://127.0.0.1:8003 |

## Setup

```powershell
pip install -r requirements.txt
ollama pull qwen2.5:7b
```

The Ollama service must be running, and the model must support tool calling.

## Run (one terminal each, from this folder)

```powershell
uvicorn add_api:app --port 8001 --reload     # Terminal 1
uvicorn info_api:app --port 8002 --reload    # Terminal 2
uvicorn agent:app --port 8003 --reload       # Terminal 3
```

Test API 1 and API 2 in Swagger (`/docs`) first, then start API 3.
If something fails, you then know which part to troubleshoot.

## Test the agent

Open http://127.0.0.1:8003/docs, then go to **POST /ask** and click **Try it out**:

```json
{ "question": "Add 10 and 20" }
{ "question": "Tell me about Python" }
{ "question": "What is LangGraph?" }
```

Expected (wording varies): `{"answer": "The sum of 10 and 20 is 30."}`

## How the agent works

`START → agent → (tool call?) → tools → agent → ... → END`

The model requests a tool, `ToolNode` runs it (an HTTP call to API 1 or API 2), and the model gets the result back before it writes its answer.
`tools_condition` ends the graph when the model replies without asking for a tool.
