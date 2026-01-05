from typing import Optional
from domain.Character import Character
from domain.Event import Event
from domain.Role import WerewolfRole
from domain.GameState import GameState
from phases.hunting.events import HuntNominatedEvent, HuntExecutionEvent, ProtectionPlacedEvent, InvestigationResultEvent

def render_hunting_event(event: Event, viewer: Character) -> Optional[str]:
    match event:
        case HuntNominatedEvent(actor_id, actor_name, target_id, target_name):
            if isinstance(viewer.role, WerewolfRole):
                if viewer.id == actor_id:
                    return f"You nominated {target_name}."
                else:
                    return f"Packmate {actor_name} nominated {target_name}."
            return None

        case ProtectionPlacedEvent(doc_id, doc_name, target_id, target_name):
            if viewer.id == doc_id:
                return f"You are protecting {target_name} tonight."
            return None

        case InvestigationResultEvent(det_id, det_name, target_id, target_name, found_role, found_faction):
            if viewer.id == det_id:
                return f"Investigation Result: {target_name} is a {found_role} ({found_faction})."
            return None

        case HuntExecutionEvent(target_id, target_name):
            return f"Tragedy! {target_name} was found dead!"

        case _:
            return None

def project_view_details(state: GameState, viewer_id: str) -> dict:
    return {}
