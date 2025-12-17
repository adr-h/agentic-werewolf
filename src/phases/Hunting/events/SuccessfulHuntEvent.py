from dataclasses import dataclass
from events.Event import Event, EventView

@dataclass
class SuccessfulHuntEvent(Event):
   victim_id: str

   def get_view(self, state, observer) -> EventView:
      character = state.get_character(self.victim_id)
      return EventView(description=f"{character.name} was slain in the night by a werewolf!")

   def apply(self, state):
      character = state.get_character(self.victim_id)
      character.state = "dead"
