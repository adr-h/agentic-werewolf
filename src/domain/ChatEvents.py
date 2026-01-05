from dataclasses import dataclass
from domain.Event import Event

@dataclass(frozen=True)
class ChatSentEvent(Event):
    sender_id: str
    sender_name: str
    message: str
    rationale: str | None = None
    strategy: str | None = None
