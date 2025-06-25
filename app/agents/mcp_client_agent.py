from __future__ import annotations

from datetime import datetime, timedelta
from typing import AsyncGenerator, Optional

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp
from openai.types.responses import ResponseTextDeltaEvent

from app.agents.base import AgentBase
from app.dto.agent_request_dto import AgentRequestDto


class MCPClientAgent(AgentBase):
    def __init__(self, user_uuid: str) -> None:
        self.user_uuid = user_uuid
        self._session_id: Optional[str] = None          # <-- cached here
        self.agent: Optional[Agent] = None              # created lazily

    def _make_headers(self) -> dict[str, str]:
        headers = {"user_uuid": self.user_uuid}
        if self._session_id:
            headers["Mcp-Session-Id"] = self._session_id
        return headers

    async def _new_transport(self) -> MCPServerStreamableHttp:
        return MCPServerStreamableHttp(
            name="MCP Server",
            cache_tools_list=True,
            params={
                "url": "http://localhost:8080/mcp",          # final path
                "timeout": timedelta(minutes=10),
                "headers": self._make_headers(),
            },
            client_session_timeout_seconds=10_000,
        )


    async def execute(self, req: AgentRequestDto) -> AsyncGenerator[str, None]:
        async with (await self._new_transport()) as server:
            if self.agent is None:
                self.agent = Agent(
                    name="MCP AI Agent",
                    instructions = f"""
                        You are an AI assistant operating via MCP.
                        
                        Context
                        -------
                        • Today is {datetime.now():%Y-%m-%d}.  
                        • Use IST unless a different timezone is specified.  
                        • User’s Slack handle: @sharable2107.
                        
                        Meeting-Summary Workflow
                        ------------------------
                        For any query that asks to *summarise*, *recap*, *review*, or *explain what happened*:
                        
                        1. **Search the calendar** for the most recent event that matches the topic.  
                        2. **Search Slack messages** (channel or DM) for relevant discussion.  
                        3. **Search email** for threads or messages related to the same topic.
                        4. **Search the personal-notes store** (Pensieve/vector DB) for the user’s own reflections.  
                        
                        Always run all four searches, unless explicitly mentioned, in that order, even if earlier searches return data.  
                        
                        Other Rules
                        -----------
                        • If the email search by subject returns nothing, retry with a mail search by keyword-only query.
                        • Consider larger number of results while listing calendar events
                        • Searching messages in slack channel require channel ID so fetch channel ID first
                        • For TODOs, use google tasks(unless mentioned otherwise); when creating tasks, set due dates; if none found, default to +2 days.  
                        • When scheduling events, propose only future time slots. If not explicitly mentioned by user then choose any FREE timeslot between 10am to 7pm
                        
                        Response
                        --------
                        After gathering data, return a concise, human-readable answer that stitches insights from every source.
                    """,
                    model="gpt-4.1-mini",
                    mcp_servers=[server],
                )
            else:
                self.agent.mcp_servers = [server]

            run = Runner.run_streamed(self.agent, req.user_prompt)
            async for ev in run.stream_events():
                if ev.type == "raw_response_event" and isinstance(ev.data, ResponseTextDeltaEvent):
                    yield ev.data.delta
                elif ev.type == "run_item_stream_event" and ev.item.type == "tool_call_item":
                    yield f"Calling tool: {ev.item.raw_item.name}\n\n"
