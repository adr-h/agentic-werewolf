
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
   from GameState import GameState
from events.Event import Event

@dataclass
class Action:
   actorId: str

   def resolve(self, gameState: "GameState") -> Event:
      raise NotImplementedError("Action.resolve() must be implemented by subclasses.")