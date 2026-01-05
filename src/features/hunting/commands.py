from dataclasses import dataclass, field
from domain.Command import Command

@dataclass(frozen=True)
class NominateHuntCommand(Command):
    target_id: str = field(metadata={"description": "The ID of the player the werewolves should hunt."})

@dataclass(frozen=True)
class ProtectCommand(Command):
    target_id: str = field(metadata={"description": "The ID of the player to protect from death tonight."})

@dataclass(frozen=True)
class InvestigateCommand(Command):
    target_id: str = field(metadata={"description": "The ID of the player to reveal the role of."})
