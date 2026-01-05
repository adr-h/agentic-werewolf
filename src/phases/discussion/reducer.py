from domain.Phase import VotingPhase
from dataclasses import replace
from domain.GameState import GameState
from domain.Event import Event
from domain.Phase import DiscussionPhase
from .events import StartVotingEvent

def apply_discussion_logic(state: GameState, event: Event) -> GameState:
    match event:
        case StartVotingEvent():
            return replace(state, phase=VotingPhase())
        case _:
            return state
