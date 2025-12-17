from collections import Counter
from dataclasses import dataclass
from typing import Literal

@dataclass
class Hunting:
   hunter_id: str
   prey_id: str

class HuntingBag:
   hunting_relationships: dict[str, Hunting] = {}

   def add_hunting(self, hunting: Hunting):
      self.hunting_relationships[hunting.hunter_id] = hunting

   def clear(self):
      self.hunting_relationships = {}

   def get_hunted(self) -> str | None:
      # hunted_id = next(
      #    relationship.hunted_id for relationship in self.hunting_relationships.values()
      # )

      # return hunted_ids
      all_potential_prey = [v.prey_id for v in self.hunting_relationships.values()]
      if len(all_potential_prey) == 0:
         return None

      counts = Counter(all_potential_prey)
      winner, count = counts.most_common(1)[0]

      return winner
