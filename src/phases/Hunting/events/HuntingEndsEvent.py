

from dataclasses import dataclass

from GameState import GameState
from events.Event import Event, EventView


@dataclass
class HuntingEndsEvent(Event):
   def get_view(self, state: GameState, observer) -> EventView:
      return EventView(description=f"Night is coming to an end. The sun rises. Time to discuss the night's events.")

   def apply(self, state: GameState):
      state.hunting.clear()
      state.protection.clear()
      state.autopsy.clear()
      state.investigations.clear()
