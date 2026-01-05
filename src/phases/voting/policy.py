from typing import List, Type
from domain.GameState import GameState
from domain.Command import Command
from domain.Phase import VotingPhase
from .commands import CastVoteCommand

def get_available_commands(state: GameState, character_id: str) -> List[Type[Command]]:
    """
    Voting Feature Policy: CastVote is available during VotingPhase for alive players.
    """
    character = next((c for c in state.characters if c.id == character_id), None)
    if not character or character.status != "alive":
        return []

    if isinstance(state.phase, VotingPhase):
        return [CastVoteCommand]

    return []
