from dataclasses import dataclass
from domain.Event import Event

@dataclass(frozen=True)
class VotingStartedEvent(Event):
    pass

@dataclass(frozen=True)
class VoteCastEvent(Event):
    voter_id: str
    target_id: str

@dataclass(frozen=True)
class VoteExecutionEvent(Event):
    target_id: str
