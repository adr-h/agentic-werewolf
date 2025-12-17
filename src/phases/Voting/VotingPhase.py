import asyncio
from dataclasses import dataclass
from typing import Literal, Sequence
from Character import Character
from GameState import GameState, Turn
from WinConditions import get_win_result
from actions.Action import Action
from phases.Voting.actions.Vote import VoteAction
from events.Event import Event
from events.VillagersWin import VillagersWinEvent
from events.WerewolvesWin import WerewolvesWinEvent
from phases.Hunting.HuntingPhase import HuntingPhase
from phases.Phase import PhaseContract
from phases.Voting.events.ExecuteCharacterEvent import ExecuteCharacterEvent
from phases.Voting.events.NoExecutionEvent import NoExecutionEvent
from phases.Voting.events.VotingEndsEvent import VotingEndsEvent

from ..TimeOfDay import TimeOfDay

class VotingPhase(PhaseContract):
   type = Literal["voting"]
   time = TimeOfDay.morning

   async def run(self, state: GameState):
      await self._collect_votes(state)
      await self._resolve_votes(state)

   async def next(self, state: GameState):
      win_result = get_win_result(state)

      if win_result == "werewolves":
         return state.apply_event(WerewolvesWinEvent())

      if win_result == "villagers":
         return state.apply_event(VillagersWinEvent())

      state.apply_event(VotingEndsEvent())

      return HuntingPhase()

   async def _collect_votes(self, state: GameState):
      timeout = 30
      interval = 5
      while timeout > 0:
         everyone_has_voted = state.votes.has_everyone_voted(state.characters)
         if (everyone_has_voted):
            break
         else:
            timeout -= interval
            await asyncio.sleep(interval)


   def get_possible_actions(self, state, actor) -> Sequence[Action]:
      living_characters_excluding_self = [
         c for c in state.characters if c.state != "dead" and c.id != actor.id
      ]

      actions = [
         VoteAction(
            name = f"Vote to execute {t.name}",
            actorId = actor.id,
            targetId = t.id
         ) for t in living_characters_excluding_self
      ]

      actions.append(
         # TODO: a dedicated "Asbtain" event instead
         VoteAction(
            name = "Abstain from voting anyone for execution",
            actorId = actor.id,
            targetId = None
         )
      )

      return actions

   async def _resolve_votes(self, state: GameState):
      winner = state.votes.get_most_voted()
      if winner is None:
         state.apply_event(NoExecutionEvent())
         return

      state.apply_event(ExecuteCharacterEvent(target_id=winner))

