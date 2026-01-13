from dataclasses import dataclass
from domain.Event import Event

@dataclass(frozen=True, kw_only=True)
class SystemAnnouncementEvent(Event):
    """
    A generic system announcement event.
    """
    message: str
