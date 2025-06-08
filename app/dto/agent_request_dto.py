from dataclasses import dataclass


@dataclass(frozen=True)
class AgentRequestDto:
    user_prompt: str
