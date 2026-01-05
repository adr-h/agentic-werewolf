from phases.hunting.events import StartDiscussionEvent
from domain.Phase import DiscussionPhase
from domain.Phase import GameOverPhase
from dataclasses import replace
from domain.GameState import GameState
from domain.Phase import HuntingPhase
from domain.Event import Event
from .events import (
    EndGameEvent,
    HuntNominatedEvent,
    HuntExecutionEvent,
    ProtectionPlacedEvent,
    InvestigationResultEvent
)

def apply_hunting_logic(state: GameState, event: Event) -> GameState:
    match event:
        case StartDiscussionEvent():
            return replace(state, phase=DiscussionPhase())

        case EndGameEvent(winner):
            return replace(state, phase=GameOverPhase(winner=winner))

        case HuntNominatedEvent(actor_id, target_id):
            if isinstance(state.phase, HuntingPhase):
                new_hunts = {**state.phase.pending_hunts, actor_id: target_id}
                new_phase = replace(state.phase, pending_hunts=new_hunts)
                return replace(state, phase=new_phase)
            return state

        case HuntExecutionEvent(target_id):
            new_characters = []
            for c in state.characters:
                if c.id == target_id:
                    new_characters.append(replace(c, status="dead"))
                else:
                    new_characters.append(c)
            return replace(state, characters=new_characters)

        case ProtectionPlacedEvent(protector_id, target_id):
            if isinstance(state.phase, HuntingPhase):
                new_protected = state.phase.protected_ids | {target_id}
                new_phase = replace(state.phase, protected_ids=new_protected)
                return replace(state, phase=new_phase)
            return state

        case InvestigationResultEvent(det_id, target_id, found_role, found_faction):
            if isinstance(state.phase, HuntingPhase):
                new_inv = {**state.phase.pending_investigations, det_id: target_id}
                new_phase = replace(state.phase, pending_investigations=new_inv)
                state = replace(state, phase=new_phase)

                new_characters = []
                for c in state.characters:
                    if c.id == det_id:
                        new_knowledge = {**c.knowledge, target_id: found_role}
                        new_characters.append(replace(c, knowledge=new_knowledge))
                    else:
                        new_characters.append(c)

                return replace(state, characters=new_characters)
            return state

        case _:
            return state
