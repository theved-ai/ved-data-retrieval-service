from app.controller.master_controller import MasterController
from fastapi import Request

from app.dto.conversation_create_response import ConversationCreateResponse
from app.dto.create_conversation_dto import CreateConversation
from app.service.impl.conversation_service import ConversationService


class ConversationMasterController(MasterController):

    def __init__(self):
        self.conversation_service = ConversationService()

    def _add_routes(self):

        @self.router.post("/v1/conversation")
        async def start_new_conversation(request: Request) -> ConversationCreateResponse:
            data = await request.json()
            conversation_creation_req = CreateConversation(**data)
            return await self.conversation_service.create_conversation(conversation_creation_req)