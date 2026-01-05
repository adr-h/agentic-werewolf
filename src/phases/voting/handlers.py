from typing import List
from domain.GameState import GameState
from domain.Phase import VotingPhase
from domain.Event import Event
from domain.Command import Command
from domain.ChatEvents import ChatSentEvent
from phases.voting.commands import CastVoteCommand, SendChatMessageCommand
from phases.voting.events import VoteCastEvent

def handle_command(state: GameState, command: Command) -> List[Event]:
    match command:
        case CastVoteCommand():
            return handle_cast_vote(state, command)
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
        sender_name=sender.name,
        message=command.message,
        rationale=command.rationale,
        strategy=command.strategy
    )]

def handle_cast_vote(state: GameState, command: CastVoteCommand) -> List[Event]:
    phase = state.phase
    if not isinstance(phase, VotingPhase):
        return []

    # Validate voter is alive
    voter = next((c for c in state.characters if c.id == command.actor_id), None)
    if not voter or voter.status != "alive":
        return []

    # Validate target exists and is alive
    target = next((c for c in state.characters if c.id == command.target_id), None)
    if not target or target.status != "alive":
        return []

    return [VoteCastEvent(
        voter_id=command.actor_id,
        voter_name=voter.name,
        target_id=command.target_id,
        target_name=target.name
    )]
