from datetime import timedelta, datetime
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
            current_date = datetime.now().strftime("%Y-%m-%d")
            mcp_client_agent = Agent(
                name="MCP AI Agent",
                instructions=(
                    "You are an expert virtual assistant capable of interacting with slack, gmail and calendar services via the MCP server. "
                    f"Today's date is {current_date}. Always use this as the current date for any reasoning or tool call. "
                    "Always use IST as the default timezone unless mentioned otherwise. "
                    "My username for slack is sharable2107"
                ),
                mcp_servers=[mcp_server],
                model='gpt-4.1-mini'
            )
            result = Runner.run_streamed(mcp_client_agent, req.user_prompt)
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    yield event.data.delta

                # elif (
                #     event.type == "run_item_stream_event"
                #     and event.item.type == "tool_call_item"
                # ):
                #     yield f"Calling tool: {event.item.raw_item.name}\n"
