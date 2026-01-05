from typing import Optional
from domain.Character import Character
from domain.Event import Event
from domain.Role import WerewolfRole
from domain.GameState import GameState
from features.hunting.events import HuntNominatedEvent, HuntExecutionEvent, ProtectionPlacedEvent, InvestigationResultEvent

def render_hunting_event(event: Event, viewer: Character) -> Optional[str]:
    match event:
        case HuntNominatedEvent(actor_id, target_id):
            if isinstance(viewer.role, WerewolfRole):
                if viewer.id == actor_id:
                    return f"You nominated {target_id}."
                else:
                    return f"Packmate {actor_id} nominated {target_id}."
            return None

        case ProtectionPlacedEvent(doc_id, target_id):
            if viewer.id == doc_id:
                return f"You are protecting {target_id} tonight."
            return None

        case InvestigationResultEvent(det_id, target_id, found_role, found_faction):
            if viewer.id == det_id:
                return f"Investigation Result: {target_id} is a {found_role} ({found_faction})."
            return None

        case HuntExecutionEvent(target_id):
            return f"The werewolves hunted {target_id} during the night."

        case _:
            return None

def project_view_details(state: GameState, viewer_id: str) -> dict:
    return {}
