from dataclasses import dataclass
from events.Event import Event, EventView

@dataclass
class ChatOpenedEvent(Event):
   def get_view(self, state, observer) -> EventView:
      return EventView(description=f"Let the discussion begin!")

   def apply(self, state):
      state.is_chat_open = True
