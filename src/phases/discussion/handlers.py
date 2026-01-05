from phases.discussion.commands import SendChatMessageCommand
from typing import List
from domain.GameState import GameState
from domain.Event import Event
from domain.Command import Command
from domain.ChatEvents import ChatSentEvent

def handle_command(state: GameState, command: Command) -> List[Event]:
    match command:
        case SendChatMessageCommand():
            return handle_send_chat(state, command)
        case _:
            return []

def handle_send_chat(state: GameState, command: SendChatMessageCommand) -> List[Event]:
    # Validation: Is sender alive?
    sender = next((c for c in state.characters if c.id == command.actor_id), None)
    if not sender or sender.status != "alive":
        return []

    return [ChatSentEvent(
        sender_id=command.actor_id,
        message=command.message,
        rationale=command.rationale,
        strategy=command.strategy
    )]
