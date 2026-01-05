from dataclasses import replace
from domain.GameState import GameState
from domain.Event import Event
from domain.Phase import GameOverPhase

def apply_game_over_logic(state: GameState, event: Event) -> GameState:
    match event:
        case _:
            return state
