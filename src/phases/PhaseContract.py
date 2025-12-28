
from abc import ABC, abstractmethod
import asyncio
from typing import Sequence, TYPE_CHECKING

if TYPE_CHECKING:
   from Character import Character
   from GameState import GameState
   from .Phase import Phase

from actions.Action import Action
from events.Event import Event

class PhaseContract(ABC):
   async def run(self, state: "GameState") -> None:
      raise NotImplementedError("Not implemented!")
      return None

   @abstractmethod
   async def next(self, state: "GameState") -> "Phase | None":
      raise NotImplementedError("Not implemented!")

   @abstractmethod
   def get_possible_actions(self, state: "GameState", actor: "Character") -> Sequence[Action]:
      return []

   def to_dict(self):
      return {
         "type": self.__class__.__name__
      }
