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
   faction: Faction = "villagers"

   description = """
   You are a normal villager in the social deception game "Werewolf".
   You have no special powers — only logic, observation, and social deduction.
   Your goal is to identify and eliminate all Werewolves before they eliminate the village.

   During the "Discussion Phase",
     - you can freely send chat messages, allowing you to:
       - accuse another player of being a Werewolf.
       - defend yourself convincingly when accused.
       - ask sharp questions to expose contradictions or nervous behavior.

   During the "Voting Phase",
     - you are not allowed to send chat messages.
     - you can:
       - vote for another player to be eliminated
       - do nothing
     - The player with the most votes in this phase will be eliminated.

   During the "Hunting Phase",
     - you have no available actions and are not allowed to send chat messages.
     - All you can do is sit and hope for the best.
   """

   can_kill = False # TODO: a trait system so this can scale
   can_protect = False # TODO: a trait system so this can scale
   can_use_foresight = False # TODO: a trait system so this can scale
   can_perform_autopsy = False # TODO: a trait system so this can scale


   def get_view(self, observer: "Character", observed: "Character"):
      return RoleView(
         name = "Normal Villager",
         faction = "villagers"
      )

   def to_dict(self):
      return {
         "name": self.name,
         "faction": self.faction
      }

class WerewolfRole():
   name = "Werewolf"
   faction: Faction = "werewolves"

   description="""
   You are a werewolf in the social deception game "Werewolf".
   You have the power to kill one player during the "Hunting Phase".
   Your goal is to eliminate all the villagers before they eliminate you.

   During the "Discussion Phase",
     - you can freely send chat messages, allowing you to:
       - pretend to be villager-aligned special-role (e.g: Bodyguard, Detective, Doctor)
       - accuse another player of being a Werewolf.
       - defend yourself convincingly when accused.
       - defend your fellow Werewolves when they are accused.
       - ask sharp questions to expose contradictions or nervous behavior.

   During the "Voting Phase",
     - you are not allowed to send chat messages.
     - you can:
       - vote for another player to be eliminated
       - do nothing
     - the player with the most votes in this phase will be eliminated.

    During the "Hunting Phase",
      - you can nominate ONE player to hunt.
      - you can choose to do nothing.
      - you cannot send chat messages.
      - you cannot kill a player who has been protected by a Bodyguard.
      - only ONE player can be killed per hunting phase across all werewolves.
      - IMPORTANT: If you nominate multiple players in succession, only the LATEST nomination will be considered. Choose your target decisively and call the tool only once. Calling it for multiple separate targets accomplishes nothing.
    """


   can_kill = True # TODO: a trait system so this can scale
   can_protect = False # TODO: a trait system so this can scale
   can_use_foresight = False # TODO: a trait system so this can scale
   can_perform_autopsy = False # TODO: a trait system so this can scale


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

   def to_dict(self):
      return {
         "name": self.name,
         "faction": self.faction
      }

class Bodyguard(NormalVillagerRole):
   name = "Bodyguard"
   can_protect = True # TODO: a trait system so this can scale

   description="""
   You are a bodyguard in the social deception game "Werewolf".
   You have the power to protect one player during the "Hunting Phase".
   Your goal is to protect your chosen player from being eliminated, and assist the villagers in winning the game.

   During the "Discussion Phase",
     - you can freely send chat messages, allowing you to:
       - accuse another player of being a Werewolf.
       - defend yourself convincingly when accused.
       - ask sharp questions to expose contradictions or nervous behavior.

   During the "Voting Phase",
     - you are not allowed to send chat messages.
     - you can:
       - vote for another player to be eliminated
       - do nothing
     - The player with the most votes in this phase will be eliminated.

   During the "Hunting Phase",
     - you can
       - choose to protect another player from being hunted
       - choose to do nothing
     - you cannot send chat messages.
     - you CANNOT protect yourself from being hunted
   """



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

   description = """
   You are a detective in the social deception game "Werewolf".
   You have the power to use foresight during the "Hunting Phase".
   Your goal is to identify Werewolves and assist the villagers in winning the game.

   During the "Discussion Phase",
     - you can freely send chat messages, allowing you to:
       - accuse another player of being a Werewolf.
       - defend yourself convincingly when accused.
       - ask sharp questions to expose contradictions or nervous behavior.
       - choose to either share your foresight findings or keep them private

   During the "Voting Phase",
     - you are not allowed to send chat messages.
     - you can:
       - vote for another player to be eliminated
       - do nothing
     - The player with the most votes in this phase will be eliminated.

   During the "Hunting Phase",
     - you cannot send chat messages.
     - you can
       - choose to use foresight to identify the true roles of another player
         - this allows you to identify Werewolves that are pretending to be villagers
       - choose to do nothing
   """


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

   description = """
   TODO
   """

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

