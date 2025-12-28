from dataclasses import dataclass
from datetime import datetime
import random
import string
from typing import Callable, Literal


from Role import Role, RoleView
from actions.Action import Action


CharacterState = Literal["alive", "dead"]

@dataclass
class CharacterView:
   name: str
   role: RoleView
   state: CharacterState

class Character:
   id: str

   name: str
   role: Role
   state: CharacterState

   last_turn_timestamp: datetime
   observed: dict[str, bool] = {}

   def __init__(self, name: str, role: Role, state: CharacterState):
      self.id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
      self.name = name
      self.role = role
      self.state = state

   def get_view(self, observer: "Character"):
      return CharacterView(
         name = self.name,
         role = self.role.get_view(
            observer=observer,
            observed=self
         ),
         state = self.state
      )

   def to_dict(self):
      return {
         "id": self.id,
         "name": self.name,
         "role": self.role.to_dict(),
         "state": self.state,
         "observed": self.observed
      }


   # async def act(self):
   #    # events_since_last_turn = sorted_events
   #    # if (self.last_turn_timestamp):
   #    #    events_since_last_turn = [x for x in events_since_last_turn if x['timestamp'] > self.last_turn_timestamp]
   #    print("todo")
