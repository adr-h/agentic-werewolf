from dataclasses import dataclass
from domain.Event import Event

# @dataclass(frozen=True)
# class DiscussionStartedEvent(Event):
#     time_remaining: int

@dataclass(frozen=True)
class StartVotingEvent(Event):
    pass