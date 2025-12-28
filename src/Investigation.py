from dataclasses import dataclass
from typing import Literal

@dataclass
class Investigation:
   examiner_id: str
   suspect_id: str

class InvestigationRegistry:
   investigation_relationships: dict[str, Investigation] = {}

   def add_investigation(self, investigation: Investigation):
      self.investigation_relationships[investigation.examiner_id] = investigation

   def clear(self):
      self.investigation_relationships = {}

   def has_already_performed_investigation(self, actor_id: str) -> bool:
      existing_investigation_relationship = self.investigation_relationships.get(actor_id, None)
      if existing_investigation_relationship is None:
         return True
      else:
         return False

   def to_dict(self):
      import dataclasses
      return {
         "investigation_relationships": {k: dataclasses.asdict(v) for k, v in self.investigation_relationships.items()}
      }

