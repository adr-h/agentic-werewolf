from typing import List, Type
from domain.GameState import GameState
from domain.Command import Command
from domain.Phase import HuntingPhase
from domain.Role import WerewolfRole, BodyguardRole, DetectiveRole
from .commands import NominateHuntCommand, ProtectCommand, InvestigateCommand

def get_available_commands(state: GameState, character_id: str) -> List[Type[Command]]:
    """
    Hunting Feature Policy: Role-based actions during HuntingPhase.
    """
    character = next((c for c in state.characters if c.id == character_id), None)
    if not character or character.status != "alive":
        return []

    if not isinstance(state.phase, HuntingPhase):
        return []

    commands: List[Type[Command]] = []
    if isinstance(character.role, WerewolfRole):
        commands.append(NominateHuntCommand)
    elif isinstance(character.role, BodyguardRole):
        commands.append(ProtectCommand)
    elif isinstance(character.role, DetectiveRole):
        # Only allow investigation once per phase
        if character_id not in state.phase.pending_investigations:
            commands.append(InvestigateCommand)

    return commands
