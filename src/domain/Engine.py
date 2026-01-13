from dataclasses import dataclass
from typing import Protocol, runtime_checkable
from .GameState import GameState
from .Event import Event
from .Command import Command

@dataclass
class UserInput:
    command: Command

class Timeout:
    pass

InputResult = UserInput | Timeout

@runtime_checkable
class EngineProtocol(Protocol):
    state: GameState

    def apply(self, event: Event) -> None:
        ...

    async def wait_for_input(self, timeout: float) -> InputResult:
        ...

    async def queue_input(self, input_data: InputResult) -> None:
        ...
