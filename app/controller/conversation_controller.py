from app.controller.master_controller import MasterController
from fastapi import Request

from app.decorators.try_catch_decorator import try_catch_wrapper
from app.dto.conversation_create_response import ConversationCreateResponse
from app.dto.create_conversation import CreateConversation
from app.service.impl.conversation_service import ConversationService
from app.utils.application_constants import create_new_conversation_endpoint, saving_conversation_error
from app.config.logging_config import logger

class ConversationMasterController(MasterController):

    def __init__(self):
        self.conversation_service = ConversationService()

    def _add_routes(self):

        @try_catch_wrapper(logger_fn= lambda e: logger.error(saving_conversation_error))
        @self.router.post(create_new_conversation_endpoint)
        async def start_new_conversation(request: Request) -> ConversationCreateResponse:
            data = await request.json()
            conversation_creation_req = CreateConversation(**data)
            return await self.conversation_service.create_conversation(conversation_creation_req)