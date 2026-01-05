from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, runtime_checkable

@dataclass(frozen=True, kw_only=True)
class Event:
    """Base class/Mixin for all events."""
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def name(self) -> str:
        return self.__class__.__name__

# If we want a Protocol for structural typing
@runtime_checkable
class EventProtocol(Protocol):
    timestamp: datetime
    name: str
