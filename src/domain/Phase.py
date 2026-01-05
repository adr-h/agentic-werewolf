from dataclasses import dataclass, field
from typing import Dict, Set

from .Enums import TimeOfDay

@dataclass(frozen=True)
class DiscussionPhase:
    """
    Daytime discussion. No special state, just waiting for the timer or user consensus.
    """
    time_remaining: int
    time: TimeOfDay = TimeOfDay.DAY

@dataclass(frozen=True)
class VotingPhase:
    """
    Daytime voting.
    """
    current_ballots: Dict[str, str] = field(default_factory=dict) # voter_id -> target_id
    time: TimeOfDay = TimeOfDay.DAY

@dataclass(frozen=True)
class HuntingPhase:
    """
    Night time hunting.
    """
    # Map of HunterID -> TargetID
    pending_hunts: Dict[str, str] = field(default_factory=dict)

    # Set of TargetIDs who are protected
    protected_ids: Set[str] = field(default_factory=set)

    # Map of DoctorID -> AutopsyTargetID (if we want to track that here)
    pending_autopsies: Dict[str, str] = field(default_factory=dict)

    # Map of DetectiveID -> InvestigationTargetID
    pending_investigations: Dict[str, str] = field(default_factory=dict)

    time: TimeOfDay = TimeOfDay.NIGHT

@dataclass(frozen=True)
class GameOverPhase:
    winner: str # "villagers" or "werewolves"
    time: TimeOfDay = TimeOfDay.DAY

Phase = DiscussionPhase | VotingPhase | HuntingPhase | GameOverPhase
