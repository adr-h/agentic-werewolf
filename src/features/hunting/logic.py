from dataclasses import replace
from typing import List

from domain.GameState import GameState
from domain.Phase import HuntingPhase
from domain.Role import WerewolfRole, BodyguardRole, DetectiveRole
from domain.Event import Event
from features.hunting.commands import NominateHuntCommand, ProtectCommand, InvestigateCommand
from features.hunting.events import HuntNominatedEvent, HuntExecutionEvent, ProtectionPlacedEvent, InvestigationResultEvent

def resolve_hunting(state: GameState) -> List[Event]:
    phase = state.phase
    if not isinstance(phase, HuntingPhase):
        return []

    # 1. Tally Hunt Nominations
    votes = {}
    for target in phase.pending_hunts.values():
        votes[target] = votes.get(target, 0) + 1

    if not votes:
        return []

    # Majority / Max votes
    max_votes = max(votes.values())
    targets = [k for k, v in votes.items() if v == max_votes]

    # Tie-breaker: If tie, no one dies.
    if len(targets) != 1:
        return []

    victim_id = targets[0]

    # 2. Check Protection
    if victim_id in phase.protected_ids:
        # Saved by Bodyguard
        return []

    # 3. Execution (Using feature-specific event)
    return [HuntExecutionEvent(target_id=victim_id)]

def handle_nominate_hunt(state: GameState, command: NominateHuntCommand) -> List[Event]:
    phase = state.phase
    if not isinstance(phase, HuntingPhase):
        return []

    actor = next((c for c in state.characters if c.id == command.actor_id), None)
    if not actor or actor.status != "alive" or not isinstance(actor.role, WerewolfRole):
        return []

    target = next((c for c in state.characters if c.id == command.target_id), None)
    if not target or target.status != "alive":
        return []

    return [HuntNominatedEvent(actor_id=command.actor_id, target_id=command.target_id)]

def handle_protect(state: GameState, command: ProtectCommand) -> List[Event]:
    phase = state.phase
    if not isinstance(phase, HuntingPhase):
        return []

    actor = next((c for c in state.characters if c.id == command.actor_id), None)
    if not actor or actor.status != "alive" or not isinstance(actor.role, BodyguardRole):
        return []

    target = next((c for c in state.characters if c.id == command.target_id), None)
    if not target or target.status != "alive":
        return []

    return [ProtectionPlacedEvent(doctor_id=command.actor_id, target_id=command.target_id)]

def handle_investigate(state: GameState, command: InvestigateCommand) -> List[Event]:
    phase = state.phase
    if not isinstance(phase, HuntingPhase):
        return []

    actor = next((c for c in state.characters if c.id == command.actor_id), None)
    if not actor or actor.status != "alive" or not isinstance(actor.role, DetectiveRole):
        return []

    if command.actor_id in phase.pending_investigations:
         return []

    target = next((c for c in state.characters if c.id == command.target_id), None)
    if not target:
        return []

    return [InvestigationResultEvent(
        detective_id=command.actor_id,
        target_id=command.target_id,
        found_role_name=target.role.name,
        found_faction=target.role.faction.value
    )]

def apply_hunting_logic(state: GameState, event: Event) -> GameState:
    match event:
        case HuntNominatedEvent(actor_id, target_id):
            if isinstance(state.phase, HuntingPhase):
                new_hunts = {**state.phase.pending_hunts, actor_id: target_id}
                new_phase = replace(state.phase, pending_hunts=new_hunts)
                return replace(state, phase=new_phase)
            return state

        case HuntExecutionEvent(target_id):
            # Modular Death Logic
            new_characters = []
            for c in state.characters:
                if c.id == target_id:
                    new_characters.append(replace(c, status="dead"))
                else:
                    new_characters.append(c)
            return replace(state, characters=new_characters)

        case ProtectionPlacedEvent(doc_id, target_id):
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
