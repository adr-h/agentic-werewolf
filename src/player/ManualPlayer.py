import asyncio
import random
import string
from typing import Callable, Coroutine, Literal, Sequence

from GameState import GameView
from actions.Action import Action
from phases.Phase import PhaseType
from .Player import Player

type ActionsGetter = Callable[[], Sequence[Action]]

class ManualPlayer(Player):
   id: str
   name: str
   type: Literal["manual_player"] = "manual_player"

   def __init__(self, name: str):
      self.id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
      self.name = name

   # async def decide_action(self, prompt: str, game_view: GameView, get_actions: ActionsGetter) -> Action:
   #    possible_actions = get_actions()

   #    # TODO: get an option from the player
   #    await asyncio.sleep(5)
   #    chosen_action = possible_actions[0]
   #    return chosen_action

   async def send_chat(self, message: str):
      raise NotImplementedError("TODO")