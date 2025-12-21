import asyncio
from dataclasses import dataclass
from typing import Literal

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

   async def run(self, state: GameState):
      state.apply_event(ChatOpenedEvent())

      # give all players time to make their decisions; check every 5 secs
      timeout = 30
      interval = 10

      while timeout > 0:
         state.apply_event(ChatReminderEvent(time_left=timeout))
         timeout -= interval
         await asyncio.sleep(interval)

   async def next(self, state: GameState):
      state.apply_event(ChatClosedEvent())
      from phases.Voting.VotingPhase import VotingPhase
      return VotingPhase()

   def get_possible_actions(self, state, actor):
      return [
         # chatting is a special action initiated by Players themselves; no need to return anything here
      ]
