
from dataclasses import dataclass

from GameState import GameState
from events.Event import Event, EventView


@dataclass
class NoExecutionEvent(Event):
   def get_view(self, state: GameState, observer) -> EventView:
      return EventView(description=f"Nobody was executed!")

   def apply(self, state: GameState):
      # No actual modification of "state"; this event is only really useful for the "view" in the events
      pass