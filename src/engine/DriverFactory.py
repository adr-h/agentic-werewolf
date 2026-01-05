from typing import Protocol

from domain.Engine import EngineProtocol
from domain.Phase import Phase, DiscussionPhase, VotingPhase, HuntingPhase, GameOverPhase

# Import Drivers
from phases.discussion.driver import DiscussionDriver
from phases.voting.driver import VotingDriver
from phases.hunting.driver import HuntingDriver
from phases.game_over.driver import GameOverDriver

class PhaseDriver(Protocol):
    async def run(self, engine: EngineProtocol) -> None:
        ...

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
