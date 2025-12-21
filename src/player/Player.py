from abc import ABC, abstractmethod
from typing import Callable, Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from GameState import GameView
from actions.Action import Action
from events.Event import Event, EventView

type ActionsGetter = Callable[[], Sequence[Action]]
type ChatSender = Callable[[str], bool]

# Player = AgenticPlayer | ManualPlayer
class Player(ABC):
   id: str
   character_id: str

   def get_public_view(self) -> "GameView":
      raise NotImplementedError("TODO")

   def receive_update(self, game_view: "GameView", actions: Sequence[Action], latest_event: None | EventView):
      raise NotImplementedError("TODO")

   async def send_chat(self, message: str):
      raise NotImplementedError("TODO")

   async def send_action(self, action: Action):
      raise NotImplementedError("TODO")

   # @abstractmethod
   # async def decide_action(self, prompt: str, game_view: GameView, get_actions: ActionsGetter) -> Action:
   #    raise NotImplementedError("TODO")
