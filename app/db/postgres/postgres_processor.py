import json
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo
from app.db.db_processor_base import DbProcessorBase
from app.db.postgres.pg_queries import query_model_metadata_by_category, query_fetch_conversation_by_conversation_id, \
    query_insert_conversation, query_insert_chat
from app.db.postgres.pg_utils import fetch_one
from app.dto.chat_persist_request_dto import ChatPersistRequest
from app.dto.create_conversation_dto import CreateConversation
from app.dto.db_chat_record import DbChatRecord
from app.dto.db_conversation_record import DbConversationRecord
from app.dto.db_model_metadata_dto import DbModelMetadataDto
from app.utils.app_utils import ensure, execute_if_or_else
from app.utils.exception_messages import no_default_active_model_for_category


class PostgresProcessor(DbProcessorBase):

    async def insert_conversation(self, req: CreateConversation) -> DbConversationRecord:
        row = await fetch_one(query_insert_conversation,req.user_id, req.title, datetime.now(tz=ZoneInfo('Asia/Kolkata')))
        return DbConversationRecord(**dict(row))

    async def insert_chat(self, req: ChatPersistRequest) -> DbChatRecord:
        row = await fetch_one(query_insert_chat,req.conversation_id, json.dumps(req.content), json.dumps(req.tools_called), req.model_metadata_id)
        return DbChatRecord(**dict(row))

    async def fetch_active_model_metadata_by_category(self, category: str) -> DbModelMetadataDto:
        row = await fetch_one(query_model_metadata_by_category, category)
        ensure(lambda: row is not None, ValueError(no_default_active_model_for_category.format(category=category)))
        return DbModelMetadataDto(**dict(row), model_configuration=row['model_config'])

    async def fetch_conversation_by_id(self, conversation_id: str) -> Optional[DbConversationRecord]:
        row = await fetch_one(query_fetch_conversation_by_conversation_id, conversation_id)
        return execute_if_or_else(
            row is not None,
            lambda: DbConversationRecord(**dict(row)),
            lambda: None
        )