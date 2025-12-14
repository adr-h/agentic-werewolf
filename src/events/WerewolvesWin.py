
from dataclasses import dataclass

from GameState import GameState
from events.Event import Event, EventView


@dataclass
class WerewolvesWinEvent(Event):
   def get_view(self, state: GameState, observer) -> EventView:
      return EventView(description=f"The werewolves have cornered the villagers - werewolves win!")

   def apply(self, state: GameState):
      state.phase = 'game_over'
      state.winners = 'werewolves'