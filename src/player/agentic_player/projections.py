from typing import List, Type
from domain.GameState import GameState
from domain.Command import Command
from engine.policy import get_available_commands as domain_get_available_commands
from engine.projections import project_game_view as domain_project_game_view

def get_available_commands(state: GameState, character_id: str) -> List[Type[Command]]:
    """Wrapper around domain policy."""
    return domain_get_available_commands(state, character_id)

def get_agent_view(state: GameState, character_id: str) -> str:
    """
    Produces a string summary for the AI agent by stringifying the domain GameView.
    """
    view = domain_project_game_view(state, character_id)

    output = []
    output.append(f"NAME: {view.me.name}")
    output.append(f"ROLE: {view.me.role_name}")
    output.append(f"STATUS: {view.me.status}")
    output.append(f"PHASE: {view.current_phase}")

    if view.phase_details:
        output.append(f"PHASE DETAILS: {view.phase_details}")

    output.append("\nPLAYERS:")
    for p in view.players:
        output.append(f"- {p.name} ({p.id}): [{p.status.upper()}] (Role: {p.role_name})")

    output.append("\nRECENT EVENTS:")
    for e_str, ts in view.recent_events:
        output.append(f"  - [{ts.strftime('%I:%M:%S%p').lower()}] {e_str}")

    return "\n".join(output)
