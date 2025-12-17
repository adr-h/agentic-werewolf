
from abc import ABC, abstractmethod
from typing import Sequence

from Character import Character
from GameState import GameState
from actions.Action import Action
from events.Event import Event
from .GameOverPhase import GameOverPhase
from .Discussion.DiscussionPhase import DiscussionPhase
from .Hunting.HuntingPhase import HuntingPhase
from .Voting.VotingPhase import VotingPhase

class PhaseContract(ABC):
   @abstractmethod
   async def run(self, state: GameState):
      raise NotImplementedError("Not implemented!")

   @abstractmethod
   async def next(self, state: GameState) -> "Phase | None":
      raise NotImplementedError("Not implemented!")

   @abstractmethod
   def get_possible_actions(self, state: GameState, actor: Character) -> Sequence[Action]:
      return []

Phase = VotingPhase | HuntingPhase | DiscussionPhase | GameOverPhase

PhaseType = VotingPhase.type | HuntingPhase.type | DiscussionPhase.type | GameOverPhase.type