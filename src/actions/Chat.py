from dataclasses import dataclass
from datetime import datetime

from GameState import GameState
from Vote import AbstainVote, NormalVote
from actions.Action import Action
from events.Event import Event, EventView

@dataclass
class ChatAction(Action):
   message: str
   strategy: str | None = None

   @property
   def name(self) -> str:
      return "Chat"

   @property
   def description(self) -> str:
      return "Sends a chat message to all players."

   def resolve(self, gameState: GameState):
      return ChatEvent(
         actorId=self.actorId,
         message=self.message,
         rationale=self.rationale,
         strategy=self.strategy
      )

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

