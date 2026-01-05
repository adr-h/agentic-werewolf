from dataclasses import dataclass
from domain.Event import Event
from domain.Phase import Phase

@dataclass(frozen=True)
class PhaseChangeEvent(Event):
    new_phase: Phase

@dataclass(frozen=True)
class ExecutionEvent(Event):
    target_id: str
    reason: str = "voted_out"

@dataclass(frozen=True)
class GameEndedEvent(Event):
    winner_faction: str
