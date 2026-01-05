from domain.Engine import EngineProtocol
from domain.Phase import GameOverPhase

class GameOverDriver:
    async def run(self, engine: EngineProtocol) -> None:
        if isinstance(engine.state.phase, GameOverPhase):
            from .events import GameOverStartedEvent
            engine.apply(GameOverStartedEvent(winner=engine.state.phase.winner))
            engine.broadcast(f"Game Over! The winner is: {engine.state.phase.winner}")
        # Terminate loop
