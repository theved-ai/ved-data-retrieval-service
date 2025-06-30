
# Default Values
default_mcp_request_timeout_in_sec=300
testing_user_id = '7dcb16b8-c05c-4ec4-9524-0003e11acd2a'
ai_agent_name = 'MCP AI Agent'
mcp_transport_name = 'MCP streamable http transport object'
default_ingestion_service_hostname="http://localhost:8085"

# Env Variables
mcp_request_timeout_in_sec_key= 'MCP_REQUEST_TIMEOUT_IN_SEC'
mcp_hostname_key = 'MCP_SERVER_HOSTNAME'
root_log_level_key='ROOT_LOG_LEVEL'
ingestion_service_hostname_key='INGEST_BASE_URL'
app_env_key='APP_ENV'
db_url_key='DB_URL'
main_path_key='MAIN_PATH'

# Fields
user_id_header_key="user_uuid"
default_category = 'default'
controller_package = 'app.controller'
chat_ingest_input_source = 'chat'
ai_agent_resp_raw_event_key = 'raw_response_event'
ai_agent_resp_stream_event_key = 'run_item_stream_event'
event_tool_item_type = 'tool_call_item'

# Local Endpoints
base_endpoint='/v1'
chat_endpoint=f"{base_endpoint}/chat"
persist_chat_endpoint=f"{base_endpoint}/chat/save"
create_new_conversation_endpoint=f"{base_endpoint}/conversation"

# Remote Endpoints
data_ingestion_endpoint= "/v1/ingest"

# Exceptions
mcp_hostname_mandatory = 'MCP hostname is mandatory'
no_default_active_model_for_category = "No active model found for category '{category}'"
chat_controller_failed='Chat stream failed'
saving_chat_error='Exception while saving chat'
saving_chat_service_error='[ChatService] Exception while saving chat'
saving_conversation_error='Exception while starting new conversation'
data_ingestion_error="Failed to send ingestion request"
data_ingestion_service_error="[IngestionClientService] Failed to send ingestion request"
db_conversation_insertion_failed='Exception while inserting conversation in db'
db_chat_insertion_failed='Exception while inserting chat in db'
db_model_metadata_fetch_failed='Exception while fetching model metadata from db'
model_metadata_fetch_failed='Exception while fetching model metadata'
db_conversation_fetch_failed='Exception while fetching conversation from db'
openai_orchestration_failed='Exception in openai orchestrator'
conversation_not_exist='Conversation does not exist: {conversation_id}'
llm_orchestration_failed='Exception at llm orchestration'
conversation_fetch_failed='Exception while fetching conversation'
db_details_not_found="Database details not found"