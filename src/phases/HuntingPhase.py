from dataclasses import dataclass
from typing import Literal

from phases.Phase import Phase
from .TimeOfDay import TimeOfDay

class HuntingPhase(Phase):
   type = Literal["hunting"]
   time = TimeOfDay.night