from dataclasses import dataclass, field
from domain.Command import Command

@dataclass(frozen=True)
class SendChatMessageCommand(Command):
    """Broadcasts a message to all players."""
    message: str = field(metadata={"description": "The message text to send."})
    rationale: str | None = field(default=None, metadata={"description": "Why you are sending this."})
    strategy: str | None = field(default=None, metadata={"description": "The strategy category (deception, investigation, etc.)"})
