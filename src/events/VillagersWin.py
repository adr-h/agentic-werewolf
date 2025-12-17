
from dataclasses import dataclass

from GameState import GameState
from events.Event import Event, EventView
from phases.GameOverPhase import GameOverPhase

@dataclass
class VillagersWinEvent(Event):
   def get_view(self, state: GameState, observer) -> EventView:
      return EventView(description=f"Werewolves have been wiped out - the villagers win!")

   def apply(self, state: GameState):
      state.phase = GameOverPhase()
      state.winners = 'villagers'