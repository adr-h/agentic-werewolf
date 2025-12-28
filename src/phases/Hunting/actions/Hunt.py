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
   targetName: str

   @property
   def name(self) -> str:
      return f"Mark {self.targetName} for Hunting"

   @property
   def description(self) -> str:
      return f"Marks {self.targetName} for hunting. If successful, {self.targetName} will be killed at the end of the Hunting phase."

   def resolve(self, gameState: GameState):
      target = gameState.get_character(self.targetId)

      if (target.state == "dead"):
         raise Exception("Target is already dead; this should not have been allowed in the first place. Debug.")

      return MarkedForHuntEvent(actorId=self.actorId, targetId=self.targetId, rationale=self.rationale)

@dataclass
class MarkedForHuntEvent(Event):
   actorId: str
   targetId: str

   def get_view(self, state: GameState, observer) -> EventView:
      target = state.get_character(self.targetId)
      actor = state.get_character(self.actorId)

      if observer == actor:
         return EventView(description=f"You are hunting {target.name} ...")

      if observer.role.faction == actor.role.faction:
         return EventView(description=f"{target.name} is being hunted by {actor.name} ...")

      return EventView(description=f"...")


   def apply(self, state: GameState):
      state.hunts.add_hunting(Hunting(
         hunter_id = self.actorId,
         prey_id = self.targetId,
      ))
