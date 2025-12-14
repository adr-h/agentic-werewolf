from dataclasses import dataclass
from datetime import datetime

from GameState import GameState
from Vote import AbstainVote, NormalVote
from actions.Action import Action
from events.Event import Event, EventView

@dataclass
class ChatAction(Action):
   name = "Chat",
   timestamp: datetime
   targetId: str | None
   message: str

   def resolve(self, gameState: GameState):
      return ChatEvent(self.actorId, self.message)

@dataclass
class ChatEvent(Event):
   actorId: str
   message: str

   def get_view(self, state: GameState, observer) -> EventView:
      actor = state.get_character(self.actorId)

      if observer == actor:
         return EventView(description=f"{actor.name} (You) said: \"{self.message}\"")

      return EventView(description=f"{actor.name} said \"{self.message}\"!")


   def apply(self, state: GameState):
      # No actual modification of "state"; this event is only really useful for the "view" in the events
      pass

