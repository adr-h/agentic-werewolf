from domain.PhaseEvents import PhaseChangeEvent
from domain.Phase import VotingPhase
from phases.discussion.commands import SendChatMessageCommand
from domain.Engine import EngineProtocol, UserInput, Timeout
from domain.ChatEvents import ChatSentEvent

class DiscussionDriver:
    async def run(self, engine: EngineProtocol) -> None:
        """
        Manages the Discussion Phase.
        Simple timer-based discussion.
        """
        # Extract initial time from current state if it's there, otherwise default
        initial_time = 30
        if hasattr(engine.state.phase, 'time_remaining'):
            initial_time = int(getattr(engine.state.phase, 'time_remaining'))

        engine.broadcast("Sun rises. It is day. Discuss who you suspect...")

        import time
        timeout_duration = float(initial_time)
        deadline = time.monotonic() + timeout_duration

        from phases.discussion.handlers import handle_command

        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                engine.broadcast("Discussion ends.")
                break

            try:
                trigger = await engine.wait_for_input(timeout=remaining)

                match trigger:
                    case UserInput(cmd):
                        events = handle_command(engine.state, cmd)
                        for e in events:
                            engine.apply(e)
                            # Custom broadcast for chat?
                            # If we want the driver to broadcast chat to UI, it needs to check event type.
                            # But ideally the engine or projection handles this.
                            # For parity with previous logic:
                            if isinstance(e, ChatSentEvent):
                                engine.broadcast(f"{e.sender_name} says: {e.message}")
                    case Timeout():
                        engine.broadcast("Discussion ends.")
                        break
            except Exception:
                if time.monotonic() >= deadline:
                    break

        # Transition to Voting
        engine.apply(PhaseChangeEvent(next_phase=VotingPhase(), flavor_text="It is time to vote."))
