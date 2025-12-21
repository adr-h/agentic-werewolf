from dataclasses import dataclass
from typing import Literal, TypedDict, Callable, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from Character import Character

Faction = Literal["werewolves", "villagers"]

@dataclass
class RoleView():
   name: str
   faction: Faction

class NormalVillagerRole():
   name = "Normal Villager"

   can_kill = False # TODO: a trait system so this can scale
   can_protect = False # TODO: a trait system so this can scale
   can_use_foresight = False # TODO: a trait system so this can scale
   can_perform_autopsy = False # TODO: a trait system so this can scale

   faction: Faction = "villagers"

   def get_view(self, observer: "Character", observed: "Character"):
      return RoleView(
         name = "Normal Villager",
         faction = "villagers"
      )

class WerewolfRole():
   name = "Werewolf"
   can_kill = True # TODO: a trait system so this can scale
   can_protect = False # TODO: a trait system so this can scale
   can_use_foresight = False # TODO: a trait system so this can scale
   can_perform_autopsy = False # TODO: a trait system so this can scale

   faction: Faction = "werewolves"

   def get_view(self, observer: "Character", observed: "Character"):
      if (observer.role.faction == "werewolves" or observer.observed.get(observed.id, False)):
         return RoleView(
            name = "Werewolf",
            faction = "werewolves"
         )

      return RoleView(
         name = "Normal Villager",
         faction = "villagers"
      )

class Bodyguard(NormalVillagerRole):
   name = "Bodyguard"
   can_protect = True # TODO: a trait system so this can scale

   def get_view(self, observer: "Character", observed: "Character"):
      if (observer.observed.get(observed.id, False)):
         return RoleView(
            name = "Bodyguard",
            faction = "villagers"
         )

      return RoleView(
         name = "Normal Villager",
         faction = "villagers"
      )

class Detective(NormalVillagerRole):
   name = "Detective"
   can_use_foresight = True # TODO: a trait system so this can scale

   def get_view(self, observer: "Character", observed: "Character"):
      if (observer.observed.get(observed.id, False)):
         return RoleView(
            name = "Detective",
            faction = "villagers"
         )

      return RoleView(
         name = "Normal Villager",
         faction = "villagers"
      )

class Doctor(NormalVillagerRole):
   name = "Doctor"
   can_perform_autopsy = True

   def get_view(self, observer: "Character", observed: "Character"):
      if (observer.observed.get(observed.id, False)):
         return RoleView(
            name = "Doctor",
            faction = "villagers"
         )

      return RoleView(
         name = "Normal Villager",
         faction = "villagers"
      )

Role = NormalVillagerRole | WerewolfRole | Bodyguard | Doctor | Detective

# carl: Role = Bodyguard()

# carl.can_protect

# NormalVillagerRole = {
#    "name": "Normal Villager",
#    "faction": "villager",
   # "initial_prompt": lambda self: f"""
   #       **Name:** Your name is "{self.name}".
   #       **Role:** You are a **Villager** in the social deception game, "Werewolf".

   #       You have **no special powers** — only logic, observation, and social deduction.
   #       Your goal is to **identify and eliminate all Werewolves** before they eliminate the village.

   #       ---

   #       ### Your Responsibilities
   #       - Participate actively during daytime discussions.
   #       - Observe behavior, inconsistencies, voting patterns, and emotional cues.
   #       - Form suspicions and challenge questionable reasoning.
   #       - Defend yourself convincingly when accused.
   #       - Vote strategically — every vote matters.

   #       ---

   #       ### What You Know
   #       - You know **you are Human**.
   #       - You do **not** know who else is Human, who is a Werewolf, or who has special roles.

   #       ---

   #       ### How to Play
   #       - **Accuse boldly**, but justify your suspicion.
   #       - **Ask sharp questions** to expose contradictions or nervous behavior.
   #       - **Watch for alliances, sudden shifts, or quiet players** — they may be hiding something.
   #       - **Stay calm**; panic makes you look guilty.
   #       - **Trust cautiously** — Werewolves lie well.

   #       ---

   #       ### Victory Condition
   #       You win if **all Werewolves are eliminated**, even if you personally die during the game.
   #    """,
   # "day_actions": [
   #     # TODO: create an Action type OR these should be tools
   #    "accuse another player",
   #    "stay silent",
   #    "ask what another player's role is",
   #    "defend a player from an accusation"
   # ],
   # "night_actions": [
   #     # TODO: create an Action type OR these should be tools
   # ]
# }

# WEREWOLF = {
#    "name": "Normal Villager",
#    "faction": "werewolf",
#    "initial_prompt": lambda Player: f"""
#          **Role:** You are a **Villager** in the social deception game, "Werewolf".

#          You have **no special powers** — only logic, observation, and social deduction.
#          Your goal is to **identify and eliminate all Werewolves** before they eliminate the village.

#          ---

#          ### Your Responsibilities
#          - Participate actively during daytime discussions.
#          - Observe behavior, inconsistencies, voting patterns, and emotional cues.
#          - Form suspicions and challenge questionable reasoning.
#          - Defend yourself convincingly when accused.
#          - Vote strategically — every vote matters.

#          ---

#          ### What You Know
#          - You know **you are Human**.
#          - You do **not** know who else is Human, who is a Werewolf, or who has special roles.

#          ---

#          ### How to Play
#          - **Accuse boldly**, but justify your suspicion.
#          - **Ask sharp questions** to expose contradictions or nervous behavior.
#          - **Watch for alliances, sudden shifts, or quiet players** — they may be hiding something.
#          - **Stay calm**; panic makes you look guilty.
#          - **Trust cautiously** — Werewolves lie well.

#          ---

#          ### Victory Condition
#          You win if **all Werewolves are eliminated**, even if you personally die during the game.
#       """,
#    "day_actions": [
#       "accuse a player",
#       "stay silent",
#       "ask what another player's role is",
#       "defend a player from an accusation"
#    ],
#    "night_actions": []
# }

