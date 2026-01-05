from dataclasses import replace
from domain.GameState import GameState
from domain.Event import Event
from domain.Phase import DiscussionPhase
from .events import DiscussionStartedEvent

def apply_discussion_logic(state: GameState, event: Event) -> GameState:
    match event:
        case DiscussionStartedEvent(time_remaining):
            return replace(state, phase=DiscussionPhase(time_remaining=time_remaining))
        case _:
            return state
