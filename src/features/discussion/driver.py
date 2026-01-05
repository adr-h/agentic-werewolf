from domain.Engine import EngineProtocol, UserInput, Timeout
from domain.GameState import GameState
from domain.Phase import VotingPhase
from domain.SystemEvents import PhaseChangeEvent

class DiscussionDriver:
    async def run(self, engine: EngineProtocol) -> None:
        """
        Manages the Discussion Phase.
        Simple timer-based discussion.
        """
        engine.broadcast("Sun rises. It is day. Discuss who you suspect...")

        import time
        if hasattr(engine.state.phase, 'time_remaining'):
            timeout_duration = float(getattr(engine.state.phase, 'time_remaining'))
        else:
            timeout_duration = 30.0

        deadline = time.monotonic() + timeout_duration

        from domain.Command import SendChatMessageCommand
        from engine.logic import handle_send_chat

        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                engine.broadcast("Discussion ends.")
                break

            try:
                trigger = await engine.wait_for_input(timeout=remaining)

                match trigger:
                    case UserInput(cmd):
                        if isinstance(cmd, SendChatMessageCommand):
                            events = handle_send_chat(engine.state, cmd)
                            for e in events:
                                engine.apply(e)
                                # Also broadcast to UI
                                engine.broadcast(f"{cmd.actor_id} says: {cmd.message}")
                    case Timeout():
                        engine.broadcast("Discussion ends.")
                        break
            except Exception:
                if time.monotonic() >= deadline:
                    break

        # Transition to Voting
        engine.broadcast("It is time to vote.")
        engine.apply(PhaseChangeEvent(new_phase=VotingPhase()))
