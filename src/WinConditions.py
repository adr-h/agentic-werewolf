from typing import Literal, TYPE_CHECKING

WinResult = Literal["no_winners_yet", "werewolves", "villagers"]

if TYPE_CHECKING:
   from GameState import GameState

def get_win_result(state: "GameState") -> WinResult:
   living_werewolves = [
      w for w in state.characters if w.role.faction == "werewolves" and w.state != "dead"
   ]

   living_villagers = [
      v for v in state.characters if v.role.faction == "villagers" and v.state != "dead"
   ]

   if living_werewolves == 0:
      return "villagers"

   if len(living_werewolves) >= len(living_villagers):
      return "werewolves"

   return "no_winners_yet"

