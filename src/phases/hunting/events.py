from dataclasses import dataclass
from domain.Event import Event

@dataclass(frozen=True)
class HuntingStartedEvent(Event):
    pass

@dataclass(frozen=True)
class HuntNominatedEvent(Event):
    actor_id: str
    target_id: str

@dataclass(frozen=True)
class HuntExecutionEvent(Event):
    target_id: str

@dataclass(frozen=True)
class ProtectionPlacedEvent(Event):
    protector_id: str
    target_id: str

@dataclass(frozen=True)
class InvestigationResultEvent(Event):
    detective_id: str
    target_id: str
    found_role: str
    found_faction: str
