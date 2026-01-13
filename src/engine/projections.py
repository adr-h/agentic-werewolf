from phases.discussion.projections import render_discussion_event
from typing import List, Tuple
from datetime import datetime
from dataclasses import dataclass
from domain.GameState import GameState
from domain.Role import project_role_view
from domain.ChatEvents import ChatSentEvent
from domain.PhaseEvents import PhaseChangeEvent
from domain.SystemEvents import SystemAnnouncementEvent
from domain.Phase import VotingPhase, HuntingPhase, DiscussionPhase, GameOverPhase

# Modular Projections
from phases.voting.projections import render_voting_event, project_view_details as voting_details
from phases.hunting.projections import render_hunting_event, project_view_details as hunting_details
from phases.discussion.projections import project_view_details as discussion_details

@dataclass(frozen=True)
class PlayerView:
    id: str
    name: str
    status: str
    role_name: str

@dataclass(frozen=True)
class GameView:
    viewer_id: str
    current_phase: str
    me: PlayerView
    players: List[PlayerView]
    recent_events: List[Tuple[str, datetime]]
    phase_details: dict

def project_game_view(state: GameState, viewer_id: str) -> GameView:
    """
    Modular Domain Projection: Orchestrates visibility and details.
    """
    viewer = next((c for c in state.characters if c.id == viewer_id), None)
    if not viewer:
        raise ValueError(f"Viewer {viewer_id} not found.")

    # 1. Project Players (Using decentralized Role logic)
    players = []
    for c in state.characters:
        role_view = project_role_view(
            observed_id=c.id,
            observed_role=c.role,
            observer_role=viewer.role,
            knowledge=viewer.knowledge
        )
        players.append(PlayerView(c.id, c.name, c.status, role_view))

    # 2. Compose Phase Details (Modular)
    phase_details = {}
    phase_details.update(voting_details(state, viewer_id))
    phase_details.update(hunting_details(state, viewer_id))
    phase_details.update(discussion_details(state, viewer_id))

    # 3. Render Events (Modular)
    rendered_events = []
    for event in state.events[-100:]:
        rendered = None

        # Centralized event rendering
        if isinstance(event, PhaseChangeEvent):
            rendered = event.flavor_text or f"Changing to {event.next_phase.__class__.__name__} phase"
        elif isinstance(event, ChatSentEvent):
            rendered = f"{event.sender_name}: {event.message}"
        elif isinstance(event, SystemAnnouncementEvent):
            rendered = event.message

        # Delegate to modular renderers if not handled centrally
        if not rendered:
            rendered = render_voting_event(event, viewer) or \
                       render_hunting_event(event, viewer) or \
                       render_discussion_event(event, viewer)

        if rendered:
            rendered_events.append((rendered, event.timestamp))

    me_view = next(p for p in players if p.id == viewer_id)

    return GameView(
        viewer_id=viewer_id,
        current_phase=state.phase.__class__.__name__,
        me=me_view,
        players=players,
        recent_events=rendered_events,
        phase_details=phase_details
    )
