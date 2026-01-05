from dataclasses import dataclass
from domain.Event import Event

@dataclass(frozen=True)
class VoteCastEvent(Event):
    voter_id: str
    voter_name: str
    target_id: str
    target_name: str

@dataclass(frozen=True)
class VoteExecutionEvent(Event):
    target_id: str
    target_name: str