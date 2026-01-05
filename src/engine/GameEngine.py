from domain.Phase import GameOverPhase
import asyncio
from typing import Optional

from domain.Engine import EngineProtocol, UserInput, Timeout, InputResult
from domain.GameState import GameState
from domain.Event import Event
from .logic import root_reducer
from .DriverFactory import get_driver_for

class GameEngine(EngineProtocol):
    def __init__(self, initial_state: GameState):
        self.state = initial_state
        self._input_queue: asyncio.Queue[UserInput] = asyncio.Queue()

    def apply(self, event: Event) -> None:
        """Applying event mutates the state by running the pure reducer."""
        print(f"[EVENT] Applying {event}")
        self.state = root_reducer(self.state, event)

    async def wait_for_input(self, timeout: float) -> InputResult:
        """
        Waits for input from the queue OR timeout.
        """
        try:
            # We wait for the next item in the queue
            return await asyncio.wait_for(self._input_queue.get(), timeout=timeout)
        except asyncio.TimeoutError:
            return Timeout()

    def broadcast(self, message: str) -> None:
        print(f"[GAME] {message}")

    async def start(self):
        print("Starting Game Engine...")
        while True:
            # 1. Get Driver
            phase = self.state.phase
            print(f"[PHASE] Processing {phase.__class__.__name__}")

            driver = get_driver_for(phase)

            # 2. Run Driver
            await driver.run(self)

            # 3. Check for end game
            if isinstance(phase, GameOverPhase):
                break
        print("Game over!")

    # For simulation: method to inject input
    async def queue_input(self, input_data: InputResult):
        if isinstance(input_data, UserInput):
             await self._input_queue.put(input_data)
