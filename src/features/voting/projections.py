from typing import Optional
from domain.GameState import GameState
from domain.Character import Character
from domain.Event import Event
from domain.Phase import VotingPhase
from features.voting.events import VoteCastEvent, VoteExecutionEvent

def render_voting_event(event: Event, viewer: Character) -> Optional[str]:
    match event:
        case VoteCastEvent(voter_id, target_id):
            if viewer.id == voter_id:
                return f"You cast a vote for {target_id}."
            else:
                return f"Player {voter_id} has cast a vote."
        case VoteExecutionEvent(target_id):
            return f"The village executed {target_id} after voting."
        case _:
            return None

def project_view_details(state: GameState, viewer_id: str) -> dict:
    if isinstance(state.phase, VotingPhase):
        return {"ballots": state.phase.current_ballots}
    return {}
