from abc import ABC, abstractmethod
from typing import Callable, Sequence, TYPE_CHECKING

# if TYPE_CHECKING:
from actions.Action import Action
from events.Event import EventView
from GameState import GameView

type ActionsGetter = Callable[[], Sequence[Action]]
type ChatSender = Callable[[str], bool]

# Player = AgenticPlayer | ManualPlayer
class Player(ABC):
   id: str
   character_id: str
   current_game_view: GameView | None = None
   possible_actions: Sequence["Action"] = []
   event_history: list["EventView"] = []

   on_update: Callable[[], None] | None = None

   def get_public_view(self) -> "GameView":
      raise NotImplementedError("TODO")

   def receive_update(self, game_view: "GameView", actions: Sequence[Action], latest_event: None | EventView):
      self.current_game_view = game_view
      self.possible_actions = actions
      if latest_event:
         self.event_history.append(latest_event)

      if self.on_update:
         self.on_update()

   async def send_chat(self, message: str):
      raise NotImplementedError("TODO")

   async def send_action(self, action: Action):
      raise NotImplementedError("TODO")

   # @abstractmethod
   # async def decide_action(self, prompt: str, game_view: GameView, get_actions: ActionsGetter) -> Action:
   #    raise NotImplementedError("TODO")
