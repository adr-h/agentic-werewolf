from phases.hunting.events import HuntExecutionEvent
from domain.Phase import GameOverPhase
from engine.win_condition import get_win_result
from domain.Engine import EngineProtocol, UserInput, Timeout
from domain.GameState import GameState
from domain.Phase import DiscussionPhase
from phases.hunting.commands import NominateHuntCommand, ProtectCommand, InvestigateCommand
from phases.hunting.handlers import resolve_hunting, handle_command

class HuntingDriver:
    async def run(self, engine: EngineProtocol) -> None:
        """
        Manages the Night/Hunting Phase.
        Resolves when timeout expires.
        """
        from phases.hunting.events import HuntingStartedEvent
        engine.apply(HuntingStartedEvent())

        engine.broadcast("Night falls. The village sleeps. Special roles, wake up.")

        import time
        # Night is strictly timer based for now (to avoid metagaming by timing analysis)
        timeout_duration = 30.0
        deadline = time.monotonic() + timeout_duration

        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                engine.broadcast("The sun is rising...")
                break

            try:
                trigger = await engine.wait_for_input(timeout=remaining)

                match trigger:
                    case UserInput(command):
                        from phases.hunting.handlers import handle_command
                        events = handle_command(engine.state, command)
                        for e in events:
                            engine.apply(e)

                    case Timeout():
                        engine.broadcast("The sun is rising...")
                        break

            except Exception:
                # On unexpected errors, we break to avoid infinite loops,
                # but only if we are close to deadline or it's a terminal error.
                if time.monotonic() >= deadline:
                    break

        # Resolution
        resolution_events = resolve_hunting(engine.state)

        death_occurred = False
        for e in resolution_events:
            engine.apply(e)
            if isinstance(e, HuntExecutionEvent):
                death_occurred = True
                engine.broadcast(f"Tragedy! {e.target_name} was found dead this morning.")

        if not death_occurred:
            engine.broadcast("It was a quiet night. No one died.")

        # Transition
        # Go to Day Discussion
        winner = get_win_result(engine.state)
        if winner != "no_winners_yet":
            from phases.game_over.events import GameOverStartedEvent
            engine.apply(GameOverStartedEvent(winner=winner))
        else:
            from phases.discussion.events import DiscussionStartedEvent
            engine.apply(DiscussionStartedEvent(time_remaining=30))
