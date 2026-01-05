from dataclasses import replace
from typing import List

from domain.GameState import GameState
from domain.Phase import VotingPhase
from domain.Event import Event
from phases.voting.commands import CastVoteCommand
from phases.voting.events import VoteCastEvent, VoteExecutionEvent

def handle_cast_vote(state: GameState, command: CastVoteCommand) -> List[Event]:
    phase = state.phase
    if not isinstance(phase, VotingPhase):
        # TODO: Return ErrorEvent? For now, empty list means rejection
        return []

    # Validate voter is alive
    # (Assuming we have a helper to get character by ID)
    voter = next((c for c in state.characters if c.id == command.actor_id), None)
    if not voter or voter.status != "alive":
        return []

    # Validate target exists and is alive (optional rule)
    target = next((c for c in state.characters if c.id == command.target_id), None)
    if not target or target.status != "alive":
        return []

    return [VoteCastEvent(voter_id=command.actor_id, target_id=command.target_id)]

def apply_voting_logic(state: GameState, event: Event) -> GameState:
    match event:
        case VoteCastEvent(voter_id, target_id):
            if isinstance(state.phase, VotingPhase):
                new_ballots = {**state.phase.current_ballots, voter_id: target_id}
                new_phase = replace(state.phase, current_ballots=new_ballots)
                return replace(state, phase=new_phase)
            return state
        case VoteExecutionEvent(target_id):
            # Modular Death Logic for Voting
            new_characters = []
            for c in state.characters:
                if c.id == target_id:
                    new_characters.append(replace(c, status="dead"))
                else:
                    new_characters.append(c)
            return replace(state, characters=new_characters)
        case _:
            return state

def resolve_winner(state: GameState) -> str | None:
    phase = state.phase
    if not isinstance(phase, VotingPhase):
        return None

    # Simple tally
    counts = {}
    for target in phase.current_ballots.values():
        counts[target] = counts.get(target, 0) + 1

    if not counts:
        return None

    # Valid winner needs > 0 votes.
    # Logic: Max votes wins. Ties?
    # For MVP: Random or no one wins on tie?
    # Let's say: No one wins on tie.

    max_votes = max(counts.values())
    winners = [k for k, v in counts.items() if v == max_votes]

    if len(winners) == 1:
        return winners[0]

    return None
