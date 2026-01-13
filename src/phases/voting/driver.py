from engine.win_condition import get_win_result
from domain.Engine import EngineProtocol, UserInput, Timeout
from domain.GameState import GameState
from domain.Phase import VotingPhase, HuntingPhase, GameOverPhase
from domain.PhaseEvents import PhaseChangeEvent
from phases.voting.handlers import handle_command
from domain.ChatEvents import ChatSentEvent
from domain.SystemEvents import SystemAnnouncementEvent

class VotingDriver:
    async def run(self, engine: EngineProtocol) -> None:
        """
        Manages the Voting Phase loop.
        Ends when all alive players have voted OR timeout expires.
        """

        import time
        timeout_duration = 40.0
        deadline = time.monotonic() + timeout_duration

        engine.apply(SystemAnnouncementEvent(message=f"You have {timeout_duration} seconds to vote ... make your time count."))

        while True:
            # Check Exit Condition A: All alive players voted
            if self._all_living_players_voted(engine.state):
                engine.apply(SystemAnnouncementEvent(message="All votes cast. Tallying results..."))
                break

            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break

            # Wait for input
            try:
                trigger = await engine.wait_for_input(timeout=remaining)

                match trigger:
                    case UserInput(command):
                        from phases.voting.handlers import handle_command
                        events = handle_command(engine.state, command)
                        for e in events:
                            engine.apply(e)

                    case Timeout():
                        break

            except Exception as e:
                if time.monotonic() >= deadline:
                    break

        engine.apply(SystemAnnouncementEvent(message="Time is up!"))

        # Resolution
        from phases.voting.events import VoteExecutionEvent
        voted_id = self._resolve_voted(engine.state)
        if voted_id:
            victim = next((c for c in engine.state.characters if c.id == voted_id), None)
            victim_name = victim.name if victim else voted_id
            engine.apply(SystemAnnouncementEvent(message=f"The village has spoken. {victim_name} received the most votes."))
            engine.apply(VoteExecutionEvent(target_id=voted_id, target_name=victim_name))
        else:
            engine.apply(SystemAnnouncementEvent(message="No valid target found or tie. No one will be executed."))

        # Transition
        # Go to Night Hunting
        winner = get_win_result(engine.state)
        if winner != "no_winners_yet":
            # Phase transition
            engine.apply(PhaseChangeEvent(next_phase=GameOverPhase(winner=winner), flavor_text=f"Game Over! The winner is: {winner}"))
        else:
            engine.apply(PhaseChangeEvent(next_phase=HuntingPhase(), flavor_text="The sun is setting. It is night. The hunt begins..."))

    def _all_living_players_voted(self, state: GameState) -> bool:
        if not isinstance(state.phase, VotingPhase):
            return False

        # Get count of living voters
        living = [c for c in state.characters if c.status == "alive"]
        # In this game, maybe only villagers vote? Or everyone?
        # Assuming everyone alive votes (Vote Phase).

        # Get count of votes in registry (phase-local)
        total_votes = len(state.phase.current_ballots)
        return total_votes >= len(living)

    def _resolve_voted(self, state: GameState) -> str | None:
        phase = state.phase
        if not isinstance(phase, VotingPhase):
            return None

        # Simple tally
        counts = {}
        for target in phase.current_ballots.values():
            counts[target] = counts.get(target, 0) + 1

        if not counts:
            return None

        max_votes = max(counts.values())
        winners = [k for k, v in counts.items() if v == max_votes]

        if len(winners) == 1:
            return winners[0]

        return None
