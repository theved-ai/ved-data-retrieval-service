from fastapi import Request
from fastapi.responses import StreamingResponse

from app.config.logging_config import logger
from app.controller.master_controller import MasterController
from app.decorators.try_catch_decorator import try_catch_wrapper
from app.dto.chat_persist_request import ChatPersistRequest
from app.dto.chat_request import ChatRequest
from app.service.impl.chat_service import ChatService
from app.service.impl.llm_orchestration_service import LLMOrchestrationService
from app.utils.application_constants import chat_endpoint, persist_chat_endpoint, chat_controller_failed, \
    saving_chat_error


class ChatMasterController(MasterController):

    def __init__(self):
        self.orchestration_service = LLMOrchestrationService()
        self.chat_service = ChatService()

    def _add_routes(self):

        @self.router.post(chat_endpoint)
        async def stream_chat(request: Request):
            data = await request.json()
            chat_request = ChatRequest(**data)
            async def streamer():
                async for chunk in self.orchestration_service.generate_response(chat_request):
                    yield chunk.model_dump_json()
            return StreamingResponse(streamer(), media_type="application/x-ndjson")


        @try_catch_wrapper(logger_fn= lambda e: logger.error(saving_chat_error))
        @self.router.post(persist_chat_endpoint)
        async def save_chat(request: Request):
            data = await request.json()
            save_chat_request = ChatPersistRequest(**data)
            return await self.chat_service.save_chat(save_chat_request)
