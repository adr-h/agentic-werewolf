from .Voting.VotingPhase import VotingPhase
from .Hunting.HuntingPhase import HuntingPhase
from .Discussion.DiscussionPhase import DiscussionPhase
from .GameOverPhase import GameOverPhase
from .PhaseContract import PhaseContract
from typing import Literal

Phase = VotingPhase | HuntingPhase | DiscussionPhase | GameOverPhase

PhaseType = Literal[VotingPhase.type | HuntingPhase.type | DiscussionPhase.type | GameOverPhase.type]