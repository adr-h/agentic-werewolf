from dataclasses import dataclass
from datetime import datetime

from Autopsy import Autopsy
from GameState import GameState
from Hunt import Hunting
from Investigation import Investigation
from actions.Action import Action
from events.Event import Event, EventView
from Protection import Protection

@dataclass
class InvestigateAction(Action):
   targetId: str
   targetName: str

   @property
   def name(self) -> str:
      return f"Investigate {self.targetName}"

   @property
   def description(self) -> str:
      return f"Investigates {self.targetName} to reveal their role."

   def resolve(self, gameState: GameState):
      target = gameState.get_character(self.targetId)
      actor = self.actorId

      if (gameState.investigations.has_already_performed_investigation(self.actorId)):
         raise Exception("Investigation was already performed. This should not have happened. Debug")

      if (target.state == "dead"):
         raise Exception(f"Target is dead; this should not have been allowed in the first place. Debug.")

      return InvestigationEvent(actorId=self.actorId, targetId=self.targetId, rationale=self.rationale)

@dataclass
class InvestigationEvent(Event):
   actorId: str
   targetId: str

   def get_view(self, state: GameState, observer) -> EventView:
      target = state.get_character(self.targetId)
      actor = state.get_character(self.actorId)

      if observer == actor:
         target_role = target.get_view(actor).role.name
         return EventView(description=f"You investigated {target.name} - and discovered that they are a '{target_role}'!")

      return EventView(description=f"...")

   def apply(self, state: GameState):
      actor = state.get_character(self.actorId)

      actor.observed[self.targetId] = True

      state.investigations.add_investigation(
         Investigation(
            examiner_id=self.actorId,
            suspect_id=self.targetId
         )
      )

