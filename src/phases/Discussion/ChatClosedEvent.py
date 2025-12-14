from dataclasses import dataclass
from events.Event import Event, EventView

@dataclass
class ChatClosedEvent(Event):
   def get_view(self, state, observer) -> EventView:
      return EventView(description=f"The time for chit-chat is over ...")

   def apply(self, state):
      state.is_chat_open = False
