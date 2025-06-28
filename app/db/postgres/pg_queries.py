
query_model_metadata_by_category = """
select mm.model_metadata_id, sm.model_name, mm.model_instruction, mm.category, mm.model_config, mm.is_active, mm.created_at, mm.updated_at
from model_metadata mm join supported_models sm 
on mm.model_id = sm.model_key
where mm.is_active = true and mm.category = $1
"""

query_fetch_conversation_by_conversation_id = """
select conversation_id, user_id, title, created_at, last_message_at 
from conversations where conversation_id = $1 
"""

query_insert_conversation = """
INSERT INTO conversations (user_id, title, last_message_at)
VALUES ($1, $2, $3)
RETURNING conversation_id, user_id, title, created_at, last_message_at;
"""

query_insert_chat = """
INSERT INTO messages (conversation_id, content, tools_called, model_metadata_id)
VALUES ($1, $2::jsonb, $3::jsonb, $4)
RETURNING message_id, conversation_id, content, tools_called, model_metadata_id, created_at, updated_at;
"""
