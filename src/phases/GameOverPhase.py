from dataclasses import dataclass
from typing import Literal

from phases.Phase import Phase
from .TimeOfDay import TimeOfDay

class GameOverPhase(Phase):
   type = Literal["game_over"]
   time = TimeOfDay.morning