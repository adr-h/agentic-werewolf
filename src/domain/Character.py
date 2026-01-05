from dataclasses import dataclass, field
from typing import Literal

from .Role import Role

@dataclass(frozen=True)
class Character:
    id: str
    name: str
    role: Role
    status: Literal["alive", "dead"] = "alive"

    # Private knowledge this character has gathered
    # e.g., {"p2": "Werewolf"}
    knowledge: dict[str, str] = field(default_factory=dict)
