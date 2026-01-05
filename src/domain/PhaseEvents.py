from dataclasses import dataclass
from typing import Optional
from domain.Event import Event
from domain.Phase import Phase

@dataclass(frozen=True, kw_only=True)
class PhaseChangeEvent(Event):
    """
    A global event that triggers a transition to a new phase.
    """
    next_phase: Phase
    flavor_text: Optional[str] = None
