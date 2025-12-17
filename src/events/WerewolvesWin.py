
from dataclasses import dataclass

from GameState import GameState
from events.Event import Event, EventView
from phases.GameOverPhase import GameOverPhase


@dataclass
class WerewolvesWinEvent(Event):
   def get_view(self, state: GameState, observer) -> EventView:
      return EventView(description=f"The villagers have been wiped out - werewolves win!")

   def apply(self, state: GameState):
      state.phase = GameOverPhase()
      state.winners = 'werewolves'