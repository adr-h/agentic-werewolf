from domain.Engine import EngineProtocol
from domain.Phase import GameOverPhase

from domain.SystemEvents import SystemAnnouncementEvent

class GameOverDriver:
    async def run(self, engine: EngineProtocol) -> None:
        if isinstance(engine.state.phase, GameOverPhase):
            engine.apply(SystemAnnouncementEvent(message=f"Game Over! The winner is: {engine.state.phase.winner}"))
        # Terminate loop
