
from dataclasses import dataclass
from datetime import datetime

from GameState import GameState
from events.Event import Event

@dataclass
class Action:
   timestamp: datetime
   actorId: str

   def resolve(self, gameState: GameState) -> Event:
      raise NotImplementedError("Action.resolve() must be implemented by subclasses.")