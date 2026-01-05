from domain.Character import Character
from domain.Event import Event
from domain.Phase import GameOverPhase

def render_game_over_event(event: Event, viewer: Character) -> str | None:
    # No specific game over events yet, but placeholder for consistency
    return None

def project_view_details(state, viewer_id):
    if isinstance(state.phase, GameOverPhase):
        return {"winner": state.phase.winner}
    return {}
