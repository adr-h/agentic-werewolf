from dataclasses import dataclass
from datetime import datetime

from GameState import GameState
from actions.Action import Action
from events.Event import Event, EventView
from Protection import ProtectedStatus

@dataclass
class KillAction(Action):
   name = "Kill Character",
   timestamp: datetime
   targetId: str

   def resolve(self, gameState: GameState):
      target = gameState.get_character(self.targetId)

      if (target.state == "dead"):
         raise Exception("Target is already dead; this should not have been allowed in the first place. Debug.")

      if isinstance(target.protection, ProtectedStatus):
         protector = gameState.get_character(target.protection.protector_id)
         if (protector.state == "alive"):
            return KillingFailedEvent(self.actorId, self.targetId)

      return KillingSucceededEvent(self.actorId, self.targetId)

@dataclass
class KillingFailedEvent(Event):
   actorId: str
   targetId: str

   def get_view(self, state: GameState, observer) -> EventView:
      target = state.get_character(self.targetId)
      actor = state.get_character(self.actorId)

      if observer == actor:
         return EventView(description=f"You tried to kill {target.name}, but failed because they were protected!")

      if observer.role.faction == actor.role.faction:
         return EventView(description=f"${actor.name} tried to kill {target.name}, but failed because they were protected!")

      if isinstance(target.protection, ProtectedStatus) and target.protection.protector_id == observer.id:
         return EventView(description=f"You successfully protected ${target.name}!")

      # this doesn't work for the typechecker - I am sad
      # if target.protection.is_protected and target.protection.protector_id == observerId:
         # return f"You successfully protected ${target.name}!"

      return EventView(description="An attempted killing was protected against!")


   def apply(self, state: GameState):
      return


@dataclass
class KillingSucceededEvent(Event):
   actorId: str
   targetId: str

   def get_view(self, state: GameState, observer) -> EventView:
      target = state.get_character(self.targetId)
      actor = state.get_character(self.actorId)

      if observer == target:
         return EventView(description="You were killed!")

      if observer == actor:
         return EventView(description=f"You killed {target.name}!")

      if observer.role.faction == actor.role.faction:
         return EventView(description=f"f{target.name} was killed by ${actor.name}!")

      return EventView(description=f"{target.name} was killed!")


   def apply(self, state: GameState):
      target = state.get_character(self.targetId)
      target.state = "dead"
