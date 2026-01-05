from phases.discussion.events import StartVotingEvent
from typing import Optional
from domain.GameState import GameState
from domain.Character import Character
from domain.Event import Event

def render_discussion_event(event: Event, viewer: Character) -> Optional[str]:
    match event:
        case StartVotingEvent():
            return f"Enough chit chat ... time to vote ..."

        case _:
            return None

def project_view_details(state: GameState, viewer_id: str) -> dict:
    return {}
