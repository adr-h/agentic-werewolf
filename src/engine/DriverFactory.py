from typing import Protocol

from domain.Engine import EngineProtocol
from domain.Phase import Phase, DiscussionPhase, VotingPhase, HuntingPhase, GameOverPhase

# Import Drivers
from features.discussion.driver import DiscussionDriver
from features.voting.driver import VotingDriver
from features.hunting.driver import HuntingDriver

class PhaseDriver(Protocol):
    async def run(self, engine: EngineProtocol) -> None:
        ...

class GameOverDriver:
    async def run(self, engine: EngineProtocol) -> None:
        if isinstance(engine.state.phase, GameOverPhase):
            engine.broadcast(f"Game Over! The winner is: {engine.state.phase.winner}")
        # Terminate loop

def get_driver_for(phase: Phase) -> PhaseDriver:
    match phase:
        case DiscussionPhase():
            return DiscussionDriver()
        case VotingPhase():
            return VotingDriver()
        case HuntingPhase():
            return HuntingDriver()
        case GameOverPhase():
            return GameOverDriver()
        case _:
            raise ValueError(f"No driver found for phase type: {type(phase)}")
