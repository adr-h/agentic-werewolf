from dataclasses import dataclass
from domain.Event import Event

@dataclass(frozen=True)
class GameOverStartedEvent(Event):
    winner: str
