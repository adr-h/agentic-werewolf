
from dataclasses import dataclass
from Character import Character, CharacterView
from Hunt import HuntingBag
from Protection import ProtectionBag
from Role import Faction
from events.Event import Event, EventView
from phases.Phase import PhaseType, Phase
from player.Player import Player
from typing import Dict, Literal
from Vote import VoteBag, VoteBagView

@dataclass
class GameView:
   characters: list[CharacterView]
   events: list[EventView]
   votes: VoteBagView
   phase: Phase
   is_chat_open: bool


@dataclass
class GameState:
   players: list[Player]
   characters: list[Character]

   votes: VoteBag
   hunting: HuntingBag
   protection: ProtectionBag

   events: list[Event]

   phase: Phase
   winners: Faction | None

   is_chat_open: bool

   # def __init__(self, players: list[Player], characters: list[Character], phase: PhaseType):
   #    self.players = players
   #    self.characters = characters
   #    self.phase = phase

   def apply_event(self, event: Event):
      self.events.append(event)
      event.apply(self)

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

   def get_player_by_character(self, character_id: str) -> Player:
      character = self.get_character(character_id)

      player = next(p for p in self.players if p.id == character.player_id)
      if not player:
         raise Exception("Unable to find player with this ID! Deb ug.")

      return player
