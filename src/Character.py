from dataclasses import dataclass
from datetime import datetime
import random
import string
from typing import Callable, Literal

from GameState import GameView
from Role import Role, RoleView
from actions.Action import Action
from player.Player import Player

CharacterState = Literal["alive", "dead"]

@dataclass
class CharacterView:
   name: str
   role: RoleView

class Character:
   id: str
   player_id: str

   name: str
   role: Role
   state: CharacterState

   last_turn_timestamp: datetime

   def __init__(self, name: str, role: Role, state: CharacterState, player_id: str):
      self.id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
      self.name = name
      self.role = role
      self.state = state
      self.player_id = player_id

   def get_view(self, observer: "Character"):
      return CharacterView(
         name = self.name,
         role = self.role.get_view(observer)
      )


   # async def act(self):
   #    # events_since_last_turn = sorted_events
   #    # if (self.last_turn_timestamp):
   #    #    events_since_last_turn = [x for x in events_since_last_turn if x['timestamp'] > self.last_turn_timestamp]
   #    print("todo")
