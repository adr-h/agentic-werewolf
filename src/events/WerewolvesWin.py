
from dataclasses import dataclass

from phases.GameOverPhase import GameOverPhase
from typing import TYPE_CHECKING
from events.Event import Event, EventView

if TYPE_CHECKING:
    from GameState import GameState


@dataclass
class WerewolvesWinEvent(Event):
   def get_view(self, state: "GameState", observer) -> EventView:
      return EventView(description=f"The villagers have been wiped out - werewolves win!")

   def apply(self, state: "GameState"):
      state.phase = GameOverPhase()
      state.winners = 'werewolves'