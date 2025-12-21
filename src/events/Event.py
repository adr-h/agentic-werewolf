from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from ..GameState import GameState
    from Character import Character

@dataclass
class EventView:
    description: str

@dataclass
class Event:
    """
    Base class for all game events.

    Events represent *facts* that happened in the game.
    They are immutable data until applied to GameState.
    """
    timestamp: datetime = field(default_factory=datetime.now, kw_only=True)

    # TODO: for now, this is intended to directly mutate GameState to make implementation easier.
    # But to make "undo" possible, it will make more sense to have `apply` return a new GameState
    def apply(self, state: "GameState") -> None:
        raise NotImplementedError("Event.apply() must be implemented by subclasses.")

    def get_view(self, state: "GameState", observer: "Character") -> EventView:
        raise NotImplementedError("Event.describe() must be implemented by subclasses.")


    # def undo(self, state: GameState) -> None:
    #     raise NotImplementedError("Event.undo() must be implemented by subclasses.")

    # def to_dict(self) -> Dict[str, Any]:
    #     """
    #     Serialize the event for logging, networking, or replay.
    #     """
    #     return {
    #         "type": self.__class__.__name__,
    #         "timestamp": self.timestamp.isoformat(),
    #     }

    # def _fields_dict(self) -> Dict[str, Any]:
    #     """
    #     Subclasses override this to list their fields.
    #     """
    #     return {}