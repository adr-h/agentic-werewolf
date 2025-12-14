
from dataclasses import dataclass

from GameState import GameState
from events.Event import Event, EventView


@dataclass
class ExecuteCharacterEvent(Event):
   target_id: str

   def get_view(self, state: GameState, observer) -> EventView:
      target = state.get_character(self.target_id)

      return EventView(description=f"{target.name} was executed!")

   def apply(self, state: GameState):
      target = state.get_character(self.target_id)
      target.state = "dead"