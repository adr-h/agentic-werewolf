from dataclasses import replace
from domain.GameState import GameState
from domain.Event import Event
from domain.GameState import GameState
from domain.Event import Event

# Phase Reducers
from phases.voting.reducer import apply_voting_logic
from phases.hunting.reducer import apply_hunting_logic
from phases.discussion.reducer import apply_discussion_logic
from phases.game_over.reducer import apply_game_over_logic

def root_reducer(state: GameState, event: Event) -> GameState:
    # Delegate to all phases (Self-initialization & Phase logic)
    state = apply_voting_logic(state, event)
    state = apply_hunting_logic(state, event)
    state = apply_discussion_logic(state, event)
    state = apply_game_over_logic(state, event)

    # 3. Append to History
    # (Using tuple concatenation for immutability style)
    return replace(state, events=[*state.events, event])
