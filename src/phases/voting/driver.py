from domain.Phase import GameOverPhase
from engine.win_condition import get_win_result
from domain.Engine import EngineProtocol, UserInput, Timeout
from domain.GameState import GameState
from domain.Phase import HuntingPhase, VotingPhase
from phases.voting.commands import CastVoteCommand
from phases.voting.handlers import handle_command, resolve_winner

class VotingDriver:
    async def run(self, engine: EngineProtocol) -> None:
        """
        Manages the Voting Phase loop.
        Ends when all alive players have voted OR timeout expires.
        """
        from phases.voting.events import VotingStartedEvent
        engine.apply(VotingStartedEvent())

        import time
        timeout_duration = 60.0
        deadline = time.monotonic() + timeout_duration

        while True:
            # Check Exit Condition A: All alive players voted
            if self._all_living_players_voted(engine.state):
                engine.broadcast("All votes cast. Tallying results...")
                break

            remaining = deadline - time.monotonic()
            if remaining <= 0:
                engine.broadcast("Time is up!")
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

                            from domain.ChatEvents import ChatSentEvent
                            from phases.voting.commands import SendChatMessageCommand
                            if isinstance(e, ChatSentEvent) and isinstance(command, SendChatMessageCommand):
                                engine.broadcast(f"{e.sender_name} says: {command.message}")

                    case Timeout():
                        engine.broadcast("Time is up!")
                        break

            except Exception as e:
                if time.monotonic() >= deadline:
                    break

        # Resolution
        from phases.voting.events import VoteExecutionEvent
        winner_id = resolve_winner(engine.state)
        if winner_id:
            victim = next((c for c in engine.state.characters if c.id == winner_id), None)
            victim_name = victim.name if victim else winner_id
            engine.broadcast(f"The village has spoken. {victim_name} will be executed.")
            engine.apply(VoteExecutionEvent(target_id=winner_id, target_name=victim_name))
        else:
            engine.broadcast("No valid target found or tie. No one will be executed.")

        # Transition
        # Go to Night Hunting
        winner = get_win_result(engine.state)
        if winner != "no_winners_yet":
            from phases.game_over.events import GameOverStartedEvent
            engine.apply(GameOverStartedEvent(winner=winner))
        else:
            from phases.hunting.events import HuntingStartedEvent
            engine.apply(HuntingStartedEvent())

    def _all_living_players_voted(self, state: GameState) -> bool:
        if not isinstance(state.phase, VotingPhase):
            return False

        # Get count of living voters
        living = [c for c in state.characters if c.status == "alive"]
        # In this game, maybe only villagers vote? Or everyone?
        # Assuming everyone alive votes (Vote Phase).

        # Get count of votes in registry (phase-local)
        # Note: phase is Union, need to check type strictness usually, but Driver is instantiated only for VotingPhase.
        # But state.phase might have changed if we applied an event?
        # No, 'handle_cast_vote' returns events, 'engine.apply' updates state.
        # So state.phase IS VotingPhase (unless we transitioned early, which we define here).

        total_votes = len(state.phase.current_ballots)
        return total_votes >= len(living)
