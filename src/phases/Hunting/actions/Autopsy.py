from dataclasses import dataclass
from datetime import datetime

from Autopsy import Autopsy
from GameState import GameState
from Hunt import Hunting
from actions.Action import Action
from events.Event import Event, EventView
from Protection import Protection

@dataclass
class AutopsyAction(Action):
   targetId: str
   targetName: str

   @property
   def name(self) -> str:
      return f"Perform autopsy on {self.targetName}"

   @property
   def description(self) -> str:
      return f"Performs an autopsy on {self.targetName} to reveal their role."
   tool_inputs = {}
   tool_output_type = "string"

   def resolve(self, gameState: GameState):
      target = gameState.get_character(self.targetId)
      actor = self.actorId

      if (gameState.autopsy.has_already_performed_autopsy(self.actorId)):
         raise Exception("Autopsy was already performed. This should not have happened. Debug")

      if (target.state != "dead"):
         raise Exception(f"Target is not dead; this should not have been allowed in the first place. Debug.")

      return AutopsyEvent(self.actorId, self.targetId)

@dataclass
class AutopsyEvent(Event):
   actorId: str
   targetId: str

   def get_view(self, state: GameState, observer) -> EventView:
      target = state.get_character(self.targetId)
      actor = state.get_character(self.actorId)

      if observer == actor:
         target_role = target.get_view(actor).role.name
         return EventView(description=f"You performed an autopsy on {target.name} - and discovered that they are a '{target_role}'!")

      return EventView(description=f"...")

   def apply(self, state: GameState):
      actor = state.get_character(self.actorId)

      actor.observed[self.targetId] = True

      state.autopsy.add_autopsy(Autopsy(
         examiner_id=actor.id,
         deceased_id=self.targetId)
      )

