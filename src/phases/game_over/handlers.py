from typing import List
from domain.GameState import GameState
from domain.Event import Event
from domain.Command import Command

def handle_command(state: GameState, command: Command) -> List[Event]:
    # No commands supported in GameOver phase for now
    return []
