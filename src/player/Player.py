from abc import ABC, abstractmethod
from typing import Callable, Coroutine, Sequence, TYPE_CHECKING

from actions.Action import Action
from events.Event import EventView
from GameState import GameView

if TYPE_CHECKING:
   from Character import Character

type ActionsGetter = Callable[[], Sequence[Action]]
type ChatSender = Callable[[str], bool]

class Player(ABC):
   id: str
   name: str

   # TODO: cleanup
   character: "Character"
   character_id: str

   current_game_view: GameView | None = None
   possible_actions: Sequence[Action] = []
   event_history: list[EventView] = []

   on_update: Callable[["Player"], None] | None = None
   on_action_sent: Callable[[Action], Coroutine[None, None, None]] | None = None
   on_chat_sent: Callable[["Player", str, str | None, str | None], Coroutine[None, None, None]] | None = None

   def receive_update(self, game_view: GameView, actions: Sequence[Action], latest_event: None | EventView):
      self.current_game_view = game_view
      self.possible_actions = actions
      if latest_event:
         self.event_history.append(latest_event)

      if self.on_update:
         self.on_update(self)

   async def send_chat(self, message: str, rationale: str | None = None, strategy: str | None = None):
      if self.on_chat_sent:
         await self.on_chat_sent(self, message, rationale, strategy)

   async def send_action(self, action: Action):
      if self.on_action_sent:
         await self.on_action_sent(action)
