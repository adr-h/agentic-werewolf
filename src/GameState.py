
from dataclasses import dataclass
from Autopsy import AutopsyBag
from Character import Character, CharacterView
from Hunt import HuntingBag
from Investigation import InvestigationBag
from Protection import ProtectionBag
from Role import Faction
from events.Event import Event, EventView
from phases.Phase import PhaseType, Phase
from player.Player import Player
from typing import Dict, Literal, Callable, Sequence
from Vote import VoteBag, VoteBagView

@dataclass
class GameView:
   characters: list[CharacterView]
   events: list[EventView]
   votes: VoteBagView
   phase: Phase
   is_chat_open: bool


Subscriber = Callable[["GameState", Event | None]]

@dataclass
class GameState:
   characters: list[Character]

   votes: VoteBag
   hunts: HuntingBag
   protection: ProtectionBag
   autopsy: AutopsyBag
   investigations: InvestigationBag

   events: list[Event]

   phase: Phase
   winners: Faction | None

   subscribers: list[Subscriber]
   is_chat_open: bool

   def subscribe(self, subscriber: Subscriber):
      self.subscribers.append(subscriber)

   def apply_event(self, event: Event):
      self.events.append(event)
      event.apply(self)

      for notify in self.subscribers:
         notify(self, event)

   def get_view(self, observer: Character)-> GameView:
      return GameView(
         phase = self.phase,
         characters = [c.get_view(observer) for c in self.characters],
         events = [e.get_view(self, observer) for e in self.events],
         votes = self.votes.get_view(observer),
         is_chat_open=self.is_chat_open
      )

   def get_character(self, character_id: str) -> Character:
      character = next(c for c in self.characters if c.id == character_id)
      if not character:
         raise Exception("Unable to find character with this ID! Debug.")

      return character
