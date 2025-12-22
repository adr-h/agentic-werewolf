from dataclasses import dataclass
from datetime import datetime

from GameState import GameState
from Hunt import Hunting
from actions.Action import Action
from events.Event import Event, EventView
from Protection import Protection

@dataclass
class ProtectAction(Action):
   targetId: str
   targetName: str

   @property
   def name(self) -> str:
      return f"Protect {self.targetName}"

   @property
   def description(self) -> str:
      return f"Protects {self.targetName} from being hunted."
   tool_inputs = {}
   tool_output_type = "None"

   def resolve(self, gameState: GameState):
      target = gameState.get_character(self.targetId)

      if (target.state == "dead"):
         raise Exception("Target is already dead; this should not have been allowed in the first place. Debug.")

      return MarkedForProtectionEvent(self.actorId, self.targetId)

@dataclass
class MarkedForProtectionEvent(Event):
   actorId: str
   targetId: str

   def get_view(self, state: GameState, observer) -> EventView:
      target = state.get_character(self.targetId)
      actor = state.get_character(self.actorId)

      if observer == actor:
         return EventView(description=f"You are protecting {target.name} ...")

      return EventView(description=f"...")

   def apply(self, state: GameState):
      state.protection.add_protection(Protection(
         protector_id = self.actorId,
         protected_id = self.targetId,
      ))
