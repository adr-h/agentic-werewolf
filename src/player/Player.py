from abc import ABC, abstractmethod
from typing import Callable, Coroutine, Sequence, TYPE_CHECKING

# if TYPE_CHECKING:
from actions.Action import Action
from events.Event import EventView
from GameState import GameView

type ActionsGetter = Callable[[], Sequence[Action]]
type ChatSender = Callable[[str], bool]

# Player = AgenticPlayer | ManualPlayer
class Player(ABC):
   id: str
   name: str
   character_id: str
   current_game_view: GameView | None = None
   possible_actions: Sequence["Action"] = []
   event_history: list["EventView"] = []

   on_update: Callable[[], None] | None = None
   on_action_sent: Callable[[Action], Coroutine[None, None, None]] | None = None
   on_chat_sent: Callable[["Player", str], Coroutine[None, None, None]] | None = None

   def receive_update(self, game_view: "GameView", actions: Sequence[Action], latest_event: None | EventView):
      self.current_game_view = game_view
      self.possible_actions = actions
      if latest_event:
         self.event_history.append(latest_event)

      if self.on_update:
         self.on_update()

   async def send_chat(self, message: str):
      if self.on_chat_sent:
         await self.on_chat_sent(self, message)

   async def send_action(self, action: Action):
      if self.on_action_sent:
         await self.on_action_sent(action)
