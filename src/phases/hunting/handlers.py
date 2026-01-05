from typing import List
from domain.GameState import GameState
from domain.Phase import HuntingPhase
from domain.Role import WerewolfRole, BodyguardRole, DetectiveRole
from domain.Event import Event
from domain.Command import Command
from phases.hunting.commands import NominateHuntCommand, ProtectCommand, InvestigateCommand
from phases.hunting.events import HuntNominatedEvent, ProtectionPlacedEvent, InvestigationResultEvent, HuntExecutionEvent

def handle_command(state: GameState, command: Command) -> List[Event]:
    match command:
        case NominateHuntCommand():
            return handle_nominate_hunt(state, command)
        case ProtectCommand():
            return handle_protect(state, command)
        case InvestigateCommand():
            return handle_investigate(state, command)
        case _:
            return []

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

    return [HuntNominatedEvent(
        actor_id=command.actor_id,
        actor_name=actor.name,
        target_id=command.target_id,
        target_name=target.name
    )]

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

    return [ProtectionPlacedEvent(
        protector_id=command.actor_id,
        protector_name=actor.name,
        target_id=command.target_id,
        target_name=target.name
    )]

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
        detective_name=actor.name,
        target_id=command.target_id,
        target_name=target.name,
        found_role=target.role.name,
        found_faction=target.role.faction.value
    )]
