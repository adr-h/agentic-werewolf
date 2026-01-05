from dataclasses import dataclass, field
from domain.Command import Command

@dataclass(frozen=True)
class CastVoteCommand(Command):
    target_id: str = field(metadata={"description": "The ID of the player you wish to vote for."})
