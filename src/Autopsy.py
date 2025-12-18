from dataclasses import dataclass
from typing import Literal

@dataclass
class Autopsy:
   examiner_id: str
   deceased_id: str

class AutopsyBag:
   autopsy_relationships: dict[str, Autopsy] = {}

   def add_autopsy(self, autopsy: Autopsy):
      self.autopsy_relationships[autopsy.examiner_id] = autopsy

   def clear(self):
      self.autopsy_relationships = {}

   def has_already_performed_autopsy(self, actor_id: str) -> bool:
      existing_autopsy_relationship = self.autopsy_relationships.get(actor_id, None)
      if existing_autopsy_relationship is None:
         return True
      else:
         return False

