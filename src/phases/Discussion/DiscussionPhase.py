from phases.Hunting.actions.Autopsy import AutopsyAction
import asyncio
from dataclasses import dataclass
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
   from Character import Character
   from GameState import GameState

from actions.Chat import ChatAction
from phases.Discussion.events.ChatReminderEvent import ChatReminderEvent

from .events.ChatClosedEvent import ChatClosedEvent
from .events.ChatOpenedEvent import ChatOpenedEvent
from phases.PhaseContract import PhaseContract
from ..TimeOfDay import TimeOfDay

class DiscussionPhase(PhaseContract):
   type = "discussion"
   time = TimeOfDay.morning

   async def run(self, state: "GameState"):
      state.apply_event(ChatOpenedEvent())

      # give all players time to make their decisions; check every 5 secs
      timeout = 30
      interval = 10

      while timeout > 0:
         state.apply_event(ChatReminderEvent(time_left=timeout))
         timeout -= interval
         await asyncio.sleep(interval)

   async def next(self, state: "GameState"):
      state.apply_event(ChatClosedEvent())
      from phases.Voting.VotingPhase import VotingPhase
      return VotingPhase()

   def get_possible_actions(self, state: "GameState", actor: "Character"):
      if actor.state == "dead":
         return []

      dead_characters = [
         character for character in state.characters
         if character.state == "dead"
      ]

      if actor.role.can_perform_autopsy and not state.autopsy.has_already_performed_autopsy(actor.id):
         return [
            AutopsyAction(
               targetId = char.id,
               targetName = char.name,
               actorId = actor.id
            )
            for char in dead_characters
         ]

      return []
