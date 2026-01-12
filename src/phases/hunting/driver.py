import domain.Event
from domain.Phase import HuntingPhase
from phases.hunting.events import HuntExecutionEvent
from domain.Phase import GameOverPhase, DiscussionPhase
from engine.win_condition import get_win_result
from domain.Engine import EngineProtocol, UserInput, Timeout
from domain.GameState import GameState
from domain.PhaseEvents import PhaseChangeEvent
from phases.hunting.handlers import handle_command

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
        resolution_events = self._resolve_hunting(engine.state)
        for e in resolution_events:
            engine.apply(e)

        # Transition
        # Go to Day Discussion
        winner = get_win_result(engine.state)
        if winner != "no_winners_yet":
            engine.apply(PhaseChangeEvent(next_phase=GameOverPhase(winner=winner), flavor_text=f"Game Over! The winner is: {winner}"))
        else:
            engine.apply(PhaseChangeEvent(next_phase=DiscussionPhase(), flavor_text="The sun rises. It is day. Discuss who you suspect..."))

    def _resolve_hunting(self, state: GameState):
        phase = state.phase
        if not isinstance(phase, HuntingPhase):
            return []

        # 1. Tally Hunt Nominations
        votes = {}
        for target in phase.pending_hunts.values():
            votes[target] = votes.get(target, 0) + 1

        if not votes:
            return []

        # Majority / Max votes
        max_votes = max(votes.values())
        targets = [k for k, v in votes.items() if v == max_votes]

        # Tie-breaker: If tie, no one dies.
        if len(targets) != 1:
            return []

        victim_id = targets[0]

        # 2. Check Protection
        if victim_id in phase.protected_ids:
            # Saved by Bodyguard
            return []

        # 3. Execution
        victim = next((c for c in state.characters if c.id == victim_id), None)
        return [HuntExecutionEvent(target_id=victim_id, target_name=victim.name if victim else "Unknown")]