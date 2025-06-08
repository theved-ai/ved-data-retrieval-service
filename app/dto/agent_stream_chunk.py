from dataclasses import dataclass


@dataclass
class AgentStreamChunk:
    content: str
    data_source: str = None
    event_type: str = None
