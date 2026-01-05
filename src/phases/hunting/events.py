from dataclasses import dataclass
from domain.Event import Event

@dataclass(frozen=True)
class HuntNominatedEvent(Event):
    actor_id: str
    actor_name: str
    target_id: str
    target_name: str

@dataclass(frozen=True)
class HuntExecutionEvent(Event):
    target_id: str
    target_name: str

@dataclass(frozen=True)
class ProtectionPlacedEvent(Event):
    protector_id: str
    protector_name: str
    target_id: str
    target_name: str

@dataclass(frozen=True)
class InvestigationResultEvent(Event):
    detective_id: str
    detective_name: str
    target_id: str
    target_name: str
    found_role: str
    found_faction: str
