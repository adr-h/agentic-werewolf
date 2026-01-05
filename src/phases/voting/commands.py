from dataclasses import dataclass, field
from domain.Command import Command

@dataclass(frozen=True)
class CastVoteCommand(Command):
    """
    Formally casts a vote for a player to be executed.
    This is the primary tool to eliminate suspected werewolves during the day.

    Strategic Note: Voting for someone who is already under heavy suspicion can
    help secure a majority, but stay alert for 'bus-throwing' where werewolves
    vote for each other to appear innocent.
    """
    target_id: str = field(metadata={"description": "The ID of the player you wish to vote for."})

@dataclass(frozen=True)
class SendChatMessageCommand(Command):
    """
    Broadcasts a message to all players during the voting phase.
    Use this for last-minute appeals or to explain your vote.
    """
    message: str = field(metadata={"description": "The message text to send."})
    rationale: str | None = field(default=None, metadata={"description": "Why you are sending this."})
    strategy: str | None = field(default=None, metadata={"description": "The strategy category (deception, investigation, etc.)"})
