from dataclasses import dataclass, field
from domain.Command import Command

@dataclass(frozen=True, kw_only=True)
class SendChatMessageCommand(Command):
    """
    Broadcasts a message to all players.
    Use this to share findings, express suspicions, or attempt to sway the group's opinion.

    Strategic Note: Effective communication is the primary weapon of the villagers,
    but it's also the werewolves' best tool for deception. Be careful not to
    reveal too much about your role if it's sensitive.
    """
    message: str = field(metadata={"description": "The message text to send."})
    strategy: str | None = field(default=None, metadata={"description": "The strategy category (deception, investigation, etc.)"})
