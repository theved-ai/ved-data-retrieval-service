# ved-data-retrieval-service

A **fully-asynchronous, streaming micro-service** that retrieve data and execute delegated tasks via OpenAI agents SDK and mcp server.\
The service exposes a single chat-style REST endpoint that streams results back to the caller in real time.

---

## 1  |  What does it do?

| Aspect | Details |
|--------|---------|
| **Goal** | Let any Ved.ai product ask questions such as “Show my unread emails from last week and summarise them” and receive live, chunked answers that may involve *both* tool calls (emails, calendar) and RAG search (internal docs). |
| **Why async?** | We depend on long-running LLM + network calls; async keeps the event loop free and scales |
| **Why streaming?** | Users see progress immediately—tool calls, partial LLM tokens, RAG passages—rather than waiting for one big response. |

---

## 2  |  Repository layout

ved-data-retrieval-service/\
├── app/ # FastAPI application code\
│ ├── controller/ # REST / streaming endpoints\
│ ├── service/ # Business-logic layer\
│ ├── orchestrator/ # Per-model orchestrators (OpenAI, Llama 3…)\
│ ├── agents/ # Agent adapters (MCP, OpenAI Agents SDK)\
│ ├── config/ # All configuration objects / pydantic settings\
│ ├── db/ # Persistence helpers (asyncpg, migrations)\
│ ├── dto/ # Pydantic DTO classes\
│ ├── enums/ # Enum definitions\
│ ├── external_clients/ # Outbound HTTP / SDK clients (RAG, auth, etc.)\
│ └── utils/ # Pure-utility helpers\
├── tests/ # pytest test-suite\
├── requirements.txt\
└── README.md # ← you are here\

## 3  |  Getting started (local dev)

### 3.1  Prerequisites

| Tool | Version (min) |
|------|---------------|
| Python | 3.9 + |
| PostgreSQL | (only if you add persistence) |

### 3.2  Clone & install

```bash
git clone https://github.com/ved-ai/ved-data-retrieval-service.git
cd ved-data-retrieval-service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 3.3 Environment variables
Create .env in the repo root:

```
OPENAI_API_KEY=sk-…
MCP_URL=http://localhost:8080/mcp
DB_URL=postgresql://postgres:secret@localhost:5432/ved_master_db
INGEST_BASE_URL=http://localhost:8085
```

### 3.4 Run the service
```
uvicorn app.main:app --reload --port 8000
```
--reload auto-restarts on code changes—ideal for development. \
*Service can also be ran from IDE*

### 3.5 Quick smoke-test
```
curl -N -X POST http://localhost:8000/v1/chat \
-H "Content-Type: application/json" \
-d '{"user_prompt":"What Slack channels am I in?"}'
```
-N disables curl buffering so you’ll see streamed chunks like:
```
{"source":"rag","content":"..."}
{"source":"mcp","content":"Calling tool: list_channel"}
{"source":"mcp","content":"#general, #random"}
```

## 4 | Key concepts & classes

| Layer                | Main class / file                          | Responsibility                                                                       |
| -------------------- |--------------------------------------------|--------------------------------------------------------------------------------------|
| **API (controller)** | `app/api/chat_controller.py`               | Receives POST `/v1/chat`, calls agent async generators, returns `StreamingResponse`. |
| **Service**          | `LLMOrchestrationService`                  | Decides which orchestrators to invoke (OpenAI, llama3, claude etc).                  |
| **Orchestrators**    | `OpenAIOrchestrator`/ `Llama3Orchestrator` | Wrap model specifics, return `AsyncGenerator[str]`.                                  |
| **Agent layer**      | `MCPClientAgent`                           | Handles tool-calling via `MCPServerStreamableHttp`, streams back deltas.             |


## 5 | Contributing
Create a feature branch (feat/<your-feature>).\
Run tests: pytest -q.\
Format: black . && flake8.\
Open a PR; describe the behaviour and add screenshots or curl outputs for any new streaming flows.

## 6 | Open issues / TODO

🌐 Swagger / OpenAPI docs for all paths.

🛡️ Add auth middleware (JWT) once the auth service is ready.

📈 Prometheus metrics for streaming latency.