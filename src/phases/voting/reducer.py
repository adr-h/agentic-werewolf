from dataclasses import replace
from domain.GameState import GameState
from domain.Event import Event
from domain.Phase import VotingPhase
from .events import VoteCastEvent, VoteExecutionEvent

def apply_voting_logic(state: GameState, event: Event) -> GameState:
    match event:
        case VoteCastEvent(voter_id, voter_name, target_id, target_name):
            if isinstance(state.phase, VotingPhase):
                new_ballots = {**state.phase.current_ballots, voter_id: target_id}
                new_phase = replace(state.phase, current_ballots=new_ballots)
                return replace(state, phase=new_phase)
            return state

        case VoteExecutionEvent(target_id):
            # Modular Death Logic for Voting
            new_characters = []
            for c in state.characters:
                if c.id == target_id:
                    new_characters.append(replace(c, status="dead"))
                else:
                    new_characters.append(c)
            return replace(state, characters=new_characters)
        case _:
            return state
