from domain.Phase import HuntingPhase
from phases.voting.events import StartHuntEvent
from domain.Phase import GameOverPhase
from dataclasses import replace
from domain.GameState import GameState
from domain.Phase import VotingPhase
from domain.Event import Event
from .events import EndGameEvent, VoteCastEvent, VoteExecutionEvent

def apply_voting_logic(state: GameState, event: Event) -> GameState:
    match event:
        case StartHuntEvent():
            return replace(state, phase=HuntingPhase())

        case EndGameEvent(winner):
            return replace(state, phase=GameOverPhase(winner=winner))

        case VoteCastEvent(voter_id, target_id):
            if isinstance(state.phase, VotingPhase):
                new_ballots = {**state.phase.current_ballots, voter_id: target_id}
                new_phase = replace(state.phase, current_ballots=new_ballots)
                return replace(state, phase=new_phase)
            return state

        case VoteExecutionEvent(target_id):
            # Modular Death Logic for Voting
            new_characters = []
            for c in state.characters:
                position_to_replace = -1
                if c.id == target_id:
                    new_characters.append(replace(c, status="dead"))
                else:
                    new_characters.append(c)
            return replace(state, characters=new_characters)
        case _:
            return state
