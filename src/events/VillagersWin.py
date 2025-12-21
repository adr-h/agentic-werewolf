
from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
   from GameState import GameState

from phases.GameOverPhase import GameOverPhase
from events.Event import Event, EventView

@dataclass
class VillagersWinEvent(Event):
   def get_view(self, state: "GameState", observer) -> EventView:
      return EventView(description=f"Werewolves have been wiped out - the villagers win!")

   def apply(self, state: "GameState"):
      state.phase = GameOverPhase()
      state.winners = 'villagers'