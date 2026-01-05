from typing import List, Type
from domain.GameState import GameState
from domain.Command import Command

# Import Feature Policies
from features.voting.policy import get_available_commands as get_voting_commands
from features.hunting.policy import get_available_commands as get_hunting_commands
from features.discussion.policy import get_available_commands as get_discussion_commands

def get_available_commands(state: GameState, character_id: str) -> List[Type[Command]]:
    """
    Composes command availability from modular feature policies.
    """
    commands: List[Type[Command]] = []

    # Simple composition: Every feature gets a chance to offer commands
    commands.extend(get_voting_commands(state, character_id))
    commands.extend(get_hunting_commands(state, character_id))
    commands.extend(get_discussion_commands(state, character_id))

    return commands
