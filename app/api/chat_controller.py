import json
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from app.service.llm_orchestration_service import LLMOrchestrationService

app = FastAPI()
service = LLMOrchestrationService()

@app.post("/v1/chat")
async def llm_stream_view(request: Request):
    try:
        body = await request.body()
        data = json.loads(body.decode())
        user_prompt = data["user_prompt"]
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

    print("STREAMING STARTED")
    async def streamer():
        async for chunk in service.generate_response(user_prompt):
            yield json.dumps(chunk.__dict__) + "\n"
    return StreamingResponse(streamer(), media_type="application/x-ndjson")
