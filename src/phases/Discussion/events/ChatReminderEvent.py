from dataclasses import dataclass
from events.Event import Event, EventView

@dataclass
class ChatReminderEvent(Event):
   time_left: int

   def get_view(self, state, observer) -> EventView:
      return EventView(description=f"There's {self.time_left} seconds left for open discussion!")

   def apply(self, state):
      pass