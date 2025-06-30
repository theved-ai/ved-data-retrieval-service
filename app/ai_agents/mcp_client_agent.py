from __future__ import annotations

import os
from datetime import timedelta, datetime
from typing import AsyncGenerator, Optional

from agents import Agent, Runner
from agents.mcp.server import MCPServerStreamableHttp
from openai.types.responses import ResponseTextDeltaEvent

from app.ai_agents.ai_agent_base import AgentBase
from app.dto.agent_request import AgentRequestDto
from app.dto.llm_response_chunk import LlmResponseChunkDto
from app.enums.llm_response_event_type import LlmResponseEventType
from app.utils.application_constants import mcp_transport_name, mcp_hostname_key, ai_agent_name, \
    ai_agent_resp_raw_event_key, ai_agent_resp_stream_event_key, event_tool_item_type, user_id_header_key, \
    default_mcp_request_timeout_in_sec, \
    mcp_request_timeout_in_sec_key
from app.utils.application_constants import mcp_hostname_mandatory


def _make_headers(user_id) -> dict[str, str]:
    headers = {user_id_header_key: user_id}
    return headers


async def _new_transport(req) -> MCPServerStreamableHttp:
    mcp_hostname = os.getenv(mcp_hostname_key)
    mcp_timeout_in_sec = os.getenv(mcp_request_timeout_in_sec_key) or default_mcp_request_timeout_in_sec
    if mcp_hostname is None: raise KeyError(mcp_hostname_mandatory)
    return MCPServerStreamableHttp(
        name=mcp_transport_name,
        cache_tools_list=True,
        params={
            "url": mcp_hostname,
            "timeout": timedelta(seconds=mcp_timeout_in_sec),
            "headers": _make_headers(req.user_id),
        },
        client_session_timeout_seconds=mcp_timeout_in_sec+20,
    )


class MCPClientAgent(AgentBase):
    def __init__(self) -> None:
        self.agent: Optional[Agent] = None

    async def execute(self, req: AgentRequestDto) -> AsyncGenerator[LlmResponseChunkDto, None]:
        async with (await _new_transport(req)) as server:
            if self.agent is None:
                self.agent = Agent(
                    name=ai_agent_name,
                    instructions = req.model_metadata.model_instruction.format(date=datetime.now().strftime("%Y-%m-%d"), conversation_id=req.conversation_id),
                    model=req.model_metadata.model_name,
                    mcp_servers=[server],
                )
            else:
                self.agent.mcp_servers = [server]

            run = Runner.run_streamed(self.agent, req.user_prompt)
            async for ev in run.stream_events():
                if ev.type == ai_agent_resp_raw_event_key and isinstance(ev.data, ResponseTextDeltaEvent):
                    yield LlmResponseChunkDto(event_type=LlmResponseEventType.raw_response, data=ev.data.delta)
                elif ev.type == ai_agent_resp_stream_event_key and ev.item.type == event_tool_item_type:
                    yield LlmResponseChunkDto(event_type=LlmResponseEventType.tool_call_list, data=ev.item.raw_item.name)
