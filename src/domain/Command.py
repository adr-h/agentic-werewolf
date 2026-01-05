from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable, Any

@dataclass(frozen=True)
class Command:
    """Base class for all commands."""
    actor_id: str

@runtime_checkable
class CommandProtocol(Protocol):
    actor_id: str
