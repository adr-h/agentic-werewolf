from dataclasses import dataclass
from datetime import datetime

from GameState import GameState
from Hunt import Hunting
from actions.Action import Action
from events.Event import Event, EventView
from Protection import Protection

@dataclass
class HuntAction(Action):
   targetId: str
   name: str = "Hunt Character"

   def resolve(self, gameState: GameState):
      target = gameState.get_character(self.targetId)

      if (target.state == "dead"):
         raise Exception("Target is already dead; this should not have been allowed in the first place. Debug.")

      return MarkedForHuntEvent(self.actorId, self.targetId)

@dataclass
class MarkedForHuntEvent(Event):
   actorId: str
   targetId: str

   def get_view(self, state: GameState, observer) -> EventView:
      target = state.get_character(self.targetId)
      actor = state.get_character(self.actorId)

      if observer == actor:
         return EventView(description=f"You are marking {target.name} for death ...")

      if observer.role.faction == actor.role.faction:
         return EventView(description=f"f{target.name} is marking ${actor.name} for death ...")

      return EventView(description=f"...")


   def apply(self, state: GameState):
      state.hunts.add_hunting(Hunting(
         hunter_id = self.actorId,
         prey_id = self.targetId,
      ))
