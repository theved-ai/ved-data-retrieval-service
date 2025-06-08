from datetime import timedelta
from typing import AsyncGenerator

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp
from openai.types.responses import ResponseTextDeltaEvent

from app.agents.base import AgentBase
from app.dto.agent_request_dto import AgentRequestDto


class MCPClientAgent(AgentBase):

    async def execute(
        self, req: AgentRequestDto
    ) -> AsyncGenerator[str, None]:
        async with MCPServerStreamableHttp(
            name="MCP Server",
            cache_tools_list=True,
            params={
                "url": "http://localhost:8080/mcp",
                "timeout": timedelta(minutes=10),
                "headers": {"user_uuid": "ec6a607d-c9c5-449e-9efa-db160c08148f"},
            },
            client_session_timeout_seconds=10000,
        ) as mcp_server:
            mcp_client_agent = Agent(
                name="MCP AI Agent",
                instructions="You are an expert virtual assistant capable of interacting with both Slack, gmail and calendar services via the MCP server",
                mcp_servers=[mcp_server],
            )
            result = Runner.run_streamed(mcp_client_agent, req.user_prompt)
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    yield event.data.delta

                elif (
                    event.type == "run_item_stream_event"
                    and event.item.type == "tool_call_item"
                ):
                    yield f"Calling tool: {event.item.raw_item.name}\n"
