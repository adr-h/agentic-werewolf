from domain.Phase import GameOverPhase
from engine.win_condition import get_win_result
from domain.Engine import EngineProtocol, UserInput, Timeout
from domain.GameState import GameState
from domain.Phase import DiscussionPhase
from domain.SystemEvents import ExecutionEvent, PhaseChangeEvent
from phases.hunting.commands import NominateHuntCommand, ProtectCommand, InvestigateCommand
from phases.hunting.logic import resolve_hunting, handle_nominate_hunt, handle_protect, handle_investigate

class HuntingDriver:
    async def run(self, engine: EngineProtocol) -> None:
        """
        Manages the Night/Hunting Phase.
        Resolves when timeout expires.
        """
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
                        events = []
                        if isinstance(command, NominateHuntCommand):
                            events = handle_nominate_hunt(engine.state, command)
                        elif isinstance(command, ProtectCommand):
                            events = handle_protect(engine.state, command)
                        elif isinstance(command, InvestigateCommand):
                            events = handle_investigate(engine.state, command)

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
            if isinstance(e, ExecutionEvent):
                death_occurred = True
                engine.broadcast(f"Tragedy! {e.target_id} was found dead this morning.")

        if not death_occurred:
            engine.broadcast("It was a quiet night. No one died.")

        # Transition
        # Go to Day Discussion
        winner = get_win_result(engine.state)
        if winner != "no_winners_yet":
            engine.apply(PhaseChangeEvent(new_phase=GameOverPhase(winner=winner)))
        else:
            engine.apply(PhaseChangeEvent(new_phase=DiscussionPhase(time_remaining=30)))
