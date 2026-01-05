from typing import Literal
from domain.GameState import GameState

WinResult = Literal["no_winners_yet", "werewolves", "villagers"]

def get_win_result(state: GameState) -> WinResult:
   living_werewolves = [
      w for w in state.characters if w.role.faction.value == "werewolves" and w.status != "dead"
   ]

   living_villagers = [
      v for v in state.characters if v.role.faction.value == "villagers" and v.status != "dead"
   ]

   if len(living_werewolves) == 0:
      return "villagers"

   if len(living_werewolves) >= len(living_villagers):
      return "werewolves"

   return "no_winners_yet"

