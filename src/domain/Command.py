from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, runtime_checkable, Any

@dataclass(frozen=True, kw_only=True)
class Command:
    """Base class for all commands."""
    actor_id: str
    rationale: str | None = field(default=None)
    timestamp: datetime = field(default_factory=datetime.now)

@runtime_checkable
class CommandProtocol(Protocol):
    actor_id: str
