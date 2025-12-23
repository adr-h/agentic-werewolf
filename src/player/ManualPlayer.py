from PIL.GifImagePlugin import TYPE_CHECKING
import asyncio
import random
import string
from typing import Callable, Literal, Sequence

from GameState import GameView
from actions.Action import Action
from .Player import Player

if TYPE_CHECKING:
   from Character import Character

class ManualPlayer(Player):
   id: str
   name: str
   type: Literal["manual_player"] = "manual_player"


   def __init__(self, name: str, character_id: str, character: "Character"):
      self.id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
      self.character_id=character_id
      self.name = name
      self.character = character


   # async def decide_action(self, prompt: str, game_view: GameView, get_actions: ActionsGetter) -> Action:
   #    possible_actions = get_actions()

   #    # TODO: get an option from the player
   #    await asyncio.sleep(5)
   #    chosen_action = possible_actions[0]
   #    return chosen_action