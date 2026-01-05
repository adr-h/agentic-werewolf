from dataclasses import dataclass, field
from typing import Sequence

from .Character import Character
from .Phase import Phase, HuntingPhase
from .Event import Event

@dataclass(frozen=True)
class GameState:
    """
    The root of the domain model.
    Held immutably. Transitions create new instances.
    """
    characters: Sequence[Character]
    phase: Phase
    events: Sequence[Event] = field(default_factory=list)

    @staticmethod
    def create(characters: Sequence[Character]) -> "GameState":
        return GameState(
            characters=characters,
            phase=HuntingPhase(),
            events=[]
        )
