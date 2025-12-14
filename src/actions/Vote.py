from dataclasses import dataclass, field
from datetime import datetime

from GameState import GameState
from Vote import AbstainVote, NormalVote
from actions.Action import Action
from events.Event import Event, EventView
from datetime import datetime

@dataclass
class VoteAction(Action):
   targetId: str | None
   name: str = "Vote for Execution"
   timestamp: datetime = field(default_factory=datetime.now)

   def resolve(self, gameState: GameState):
      # TODO: abstraining from voting should be its own action!
      if (self.targetId is None):
         return AbstainSucceededEvent(self.actorId)

      target = gameState.get_character(self.targetId)
      if (target.state == "dead"):
         raise Exception("Target is already dead; this should not have been allowed in the first place. Debug.")

      return VoteSucceededEvent(self.actorId, self.targetId)

@dataclass
class AbstainSucceededEvent(Event):
   actorId: str

   def get_view(self, state: GameState, observer) -> EventView:
      actor = state.get_character(self.actorId)

      if observer == actor:
         return EventView(description=f"You abstained from voting!")

      return EventView(description=f"{actor.name} has abstained from voting!")

   def apply(self, state: GameState):
      phase = state.phase

      if phase == "voting":
         state.votes.add_vote(
            self.actorId,
            AbstainVote(voter_id= self.actorId)
         )

@dataclass
class VoteSucceededEvent(Event):
   actorId: str
   targetId: str

   def get_view(self, state: GameState, observer) -> EventView:
      target = state.get_character(self.targetId)
      actor = state.get_character(self.actorId)

      if observer == actor:
         return EventView(description=f"You voted for {target.name}!")

      return EventView(description=f"{actor.name} cast their vote!")


   def apply(self, state: GameState):
      phase = state.phase

      if phase == "voting":
         state.votes.add_vote(
            self.actorId,
            NormalVote(voter_id= self.actorId, target_id = self.targetId)
         )
      else:
         raise Exception('Cannot vote when it is not the voting phase! Debug')

