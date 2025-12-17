from abc import ABC, abstractmethod
from typing import Callable, Sequence

from GameState import GameView
from actions.Action import Action
from .AgenticPlayer import AgenticPlayer
from .ManualPlayer import ManualPlayer

type ActionsGetter = Callable[[], Sequence[Action]]
type ChatSender = Callable[[str], bool]

# Player = AgenticPlayer | ManualPlayer
class Player(ABC):
   id: str

   def get_public_view(self) -> GameView:
      raise NotImplementedError("TODO")

   def receive_possible_actions(self, actions: Sequence[Action]):
      raise NotImplementedError("TODO")

   async def send_chat(self, message: str):
      raise NotImplementedError("TODO")

   async def send_action(self, action: Action):
      raise NotImplementedError("TODO")

   # @abstractmethod
   # async def decide_action(self, prompt: str, game_view: GameView, get_actions: ActionsGetter) -> Action:
   #    raise NotImplementedError("TODO")
