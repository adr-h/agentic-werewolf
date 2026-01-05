from phases.voting.events import EndGameEvent
from phases.voting.events import StartHuntEvent
from typing import Optional
from domain.GameState import GameState
from domain.Character import Character
from domain.Event import Event
from domain.Phase import VotingPhase
from phases.voting.events import VoteCastEvent, VoteExecutionEvent

def render_voting_event(event: Event, viewer: Character) -> Optional[str]:
    match event:
        case VoteCastEvent(voter_id, voter_name, target_id, target_name):
            if viewer.id == voter_id:
                return f"You cast a vote for {target_name}."
            else:
                return f"Player {voter_name} has cast a vote."
        case VoteExecutionEvent(target_id, target_name):
            return f"The village executed {target_name} after voting."

        case EndGameEvent(winner):
            return f"Game Over! The winner is: {winner}"

        case StartHuntEvent():
            return "The sun is rising. The village awakens."

        case _:
            return None

def project_view_details(state: GameState, viewer_id: str) -> dict:
    if isinstance(state.phase, VotingPhase):
        return {"ballots": state.phase.current_ballots}
    return {}
