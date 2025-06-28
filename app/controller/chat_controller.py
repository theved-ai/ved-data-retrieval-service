from fastapi import Request
from fastapi.responses import StreamingResponse

from app.controller.master_controller import MasterController
from app.dto.chat_persist_request_dto import ChatPersistRequest
from app.dto.chat_request_dto import ChatRequest
from app.service.impl.chat_service import ChatService
from app.service.impl.llm_orchestration_service import LLMOrchestrationService


class ChatMasterController(MasterController):

    def __init__(self):
        self.orchestration_service = LLMOrchestrationService()
        self.chat_service = ChatService()

    def _add_routes(self):

        @self.router.post("/v1/chat")
        async def stream_chat(request: Request):
            data = await request.json()
            chat_request = ChatRequest(**data)
            async def streamer():
                async for chunk in self.orchestration_service.generate_response(chat_request):
                    yield chunk.model_dump_json()
            return StreamingResponse(streamer(), media_type="application/x-ndjson")

        @self.router.post("/v1/chat/save")
        async def save_chat(request: Request):
            data = await request.json()
            save_chat_request = ChatPersistRequest(**data)
            return await self.chat_service.save_chat(save_chat_request)
