
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
   from GameState import GameState
from events.Event import Event

@dataclass
class Action:
   actorId: str
   rationale: str | None = field(default=None, kw_only=True)

   @property
   def name(self) -> str:
      return self.__class__.__name__.replace("Action", "")

   @property
   def description(self) -> str:
      return f"Perform {self.name}"

   def resolve(self, gameState: "GameState") -> Event:
      raise NotImplementedError("Action.resolve() must be implemented by subclasses.")