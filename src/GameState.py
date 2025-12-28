from typing import Dict, Literal, Callable, Sequence, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
   from Autopsy import AutopsyRegistry
   from Character import Character
   from Hunt import HuntingRegistry
   from Investigation import InvestigationRegistry
   from Protection import ProtectionRegistry
   from phases.Phase import Phase
   from player.Player import Player
   from Vote import VoteRegistry

from Character import CharacterView
from events.Event import EventView, Event
from Vote import VoteRegistryView
from Role import Faction


@dataclass
class GameView:
   characters: list[CharacterView]
   events: list[EventView]
   phase: "Phase"
   is_chat_open: bool



@dataclass
class GameState:
   characters: list["Character"]

   votes: "VoteRegistry"
   hunts: "HuntingRegistry"
   protection: "ProtectionRegistry"
   autopsy: "AutopsyRegistry"
   investigations: "InvestigationRegistry"

   events: list["Event"]

   phase: "Phase"
   winners: Faction | None

   subscribers: list["Subscriber"]
   is_chat_open: bool

   def subscribe(self, subscriber: "Subscriber"):
      self.subscribers.append(subscriber)

   def apply_event(self, event: "Event"):
      self.events.append(event)
      event.apply(self)

      for notify in self.subscribers:
         notify(self, event)

   def get_view(self, observer: "Character")-> "GameView":
      event_view = [e.get_view(self, observer) for e in self.events]
      return GameView(
         phase = self.phase,
         characters = [c.get_view(observer) for c in self.characters],
         events = event_view[::-1],
         # votes = self.votes.get_view(observer),
         is_chat_open=self.is_chat_open
      )

   def get_character(self, character_id: str) -> "Character":
      character = next(c for c in self.characters if c.id == character_id)
      if not character:
         raise Exception("Unable to find character with this ID! Debug.")

      return character

   def to_dict(self):
      return {
         "characters": [c.to_dict() for c in self.characters],
         "votes": self.votes.to_dict(),
         "hunts": self.hunts.to_dict(),
         "protection": self.protection.to_dict(),
         "autopsy": self.autopsy.to_dict(),
         "investigations": self.investigations.to_dict(),
         "events": [e.to_dict() for e in self.events],
         "phase": self.phase.to_dict(),
         "winners": self.winners,
         "is_chat_open": self.is_chat_open
      }

Subscriber = Callable[[GameState, Event | None], None]