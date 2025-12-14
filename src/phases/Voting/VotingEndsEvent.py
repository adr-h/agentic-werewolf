

from dataclasses import dataclass

from GameState import GameState
from events.Event import Event, EventView


@dataclass
class VotingEndsEvent(Event):
   def get_view(self, state: GameState, observer) -> EventView:
      return EventView(description=f"Voting phase is over!")

   def apply(self, state: GameState):
      state.votes.clear()
      state.phase = 'hunting'

