import asyncio
from dataclasses import dataclass
from typing import Literal

from GameState import GameState
from WinConditions import get_win_result
from events.VillagersWin import VillagersWinEvent
from events.WerewolvesWin import WerewolvesWinEvent

from phases.Hunting.actions.Autopsy import AutopsyAction
from phases.Hunting.actions.Hunt import HuntAction
from phases.Hunting.actions.Protect import ProtectAction
from phases.Hunting.events.HuntingEndsEvent import HuntingEndsEvent
from phases.Hunting.events.PeacefulNightEvent import PeacefulNightEvent
from phases.Hunting.events.SuccessfulHuntEvent import SuccessfulHuntEvent
from phases.PhaseContract import PhaseContract
from ..TimeOfDay import TimeOfDay

class HuntingPhase(PhaseContract):
   type = "hunting"
   time = TimeOfDay.night

   async def run(self, state):
      await self._wait_for_player_actions(state)
      await self._resolve_hunting(state)

   async def _wait_for_player_actions(self, state: GameState):
      # give all players time to make their decisions; check every 5 secs
      timeout = 30
      interval = 10
      while timeout > 0:
         timeout -= interval
         # TODO: spooky random events?
         await asyncio.sleep(interval)

   async def _resolve_hunting(self, state: GameState):
      target_id = state.hunts.get_hunted()
      if (target_id is None):
         state.apply_event(PeacefulNightEvent())
         return

      target_was_protected = state.protection.is_protected(target_id)
      if (target_was_protected):
         state.apply_event(PeacefulNightEvent())
         return

      state.apply_event(
         SuccessfulHuntEvent(
            victim_id=target_id
         )
      )

   async def next(self, state):
      win_result = get_win_result(state)

      if win_result == "werewolves":
         return state.apply_event(WerewolvesWinEvent())

      if win_result == "villagers":
         return state.apply_event(VillagersWinEvent())

      state.apply_event(HuntingEndsEvent())

      from phases.Discussion.DiscussionPhase import DiscussionPhase
      return DiscussionPhase()

   def get_possible_actions(self, state, actor):
      living_characters = [
         character for character in state.characters
         if character.state == "alive"
      ]

      dead_characters = [
         character for character in state.characters
         if character.state == "dead"
      ]

      if actor.role.can_kill:
         return [
            HuntAction(
               targetId = char.id,
               targetName = char.name,
               actorId = actor.id
            )
            for char in living_characters
         ]

      if actor.role.can_protect and not state.protection.has_already_protected(actor.id):
         return [
            ProtectAction(
               targetId = char.id,
               targetName = char.name,
               actorId = actor.id
            )
            for char in living_characters
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