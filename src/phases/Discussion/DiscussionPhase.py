from dataclasses import dataclass
from typing import Literal

from GameState import GameState
from .ChatClosedEvent import ChatClosedEvent
from .ChatOpenedEvent import ChatOpenedEvent
from phases.Phase import Phase
from ..TimeOfDay import TimeOfDay

class DiscussionPhase(Phase):
   type = Literal["discussion"]
   time = TimeOfDay.morning

   async def run(self, state: GameState):
      state.apply_event(ChatOpenedEvent())

      

      state.apply_event(ChatClosedEvent())


      # await self._collect_votes(state)
      # await self._resolve_votes(state)

   async def next(self, state: GameState):
      # state.apply_event(VotingEndsEvent())