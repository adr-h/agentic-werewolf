from dataclasses import replace
from domain.GameState import GameState
from domain.Event import Event
from domain.SystemEvents import PhaseChangeEvent
from domain.Command import SendChatMessageCommand
from domain.ChatEvents import ChatSentEvent

# Feature Logic
from phases.voting.logic import apply_voting_logic
from phases.hunting.logic import apply_hunting_logic

def handle_send_chat(state: GameState, command: SendChatMessageCommand) -> list:
    """
    Handles a SendChatMessageCommand by producing a ChatSentEvent.
    """
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

def apply_system_logic(state: GameState, event: Event) -> GameState:
    match event:
        case PhaseChangeEvent(new_phase):
            return replace(state, phase=new_phase)
        case _:
            return state

def root_reducer(state: GameState, event: Event) -> GameState:
    # 1. Apply System Logic (Phase Changes, Deaths)
    state = apply_system_logic(state, event)

    # 2. Apply Feature Logic (Voting, Hunting)
    # Note: Order matters little if they handle disjoint events.
    state = apply_voting_logic(state, event)
    state = apply_hunting_logic(state, event)

    # 3. Append to History
    # (Using tuple concatenation for immutability style)
    return replace(state, events=[*state.events, event])
