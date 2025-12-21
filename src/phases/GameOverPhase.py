from dataclasses import dataclass
from typing import Literal

from phases.PhaseContract import PhaseContract
from .TimeOfDay import TimeOfDay

class GameOverPhase(PhaseContract):
   type = Literal["game_over"]
   time = TimeOfDay.morning

   async def run(self, state):
      pass

   async def next(self, state):
      return None

   def get_possible_actions(self, state, actor):
      return []