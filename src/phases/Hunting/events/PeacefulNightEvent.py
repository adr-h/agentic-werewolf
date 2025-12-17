from dataclasses import dataclass
from events.Event import Event, EventView

@dataclass
class PeacefulNightEvent(Event):
   def get_view(self, state, observer) -> EventView:
      return EventView(description=f"A peaceful night has passed ...")

   def apply(self, state):
      pass
