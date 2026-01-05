from dataclasses import dataclass
from domain.Event import Event
from domain.Phase import Phase

@dataclass(frozen=True)
class PhaseChangeEvent(Event):
    new_phase: Phase

