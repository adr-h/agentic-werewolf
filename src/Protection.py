from dataclasses import dataclass
from typing import Literal

@dataclass
class Protection:
   protector_id: str
   protected_id: str

class ProtectionRegistry:
   protection_relationships: dict[str, Protection] = {}

   def add_protection(self, protection: Protection):
      self.protection_relationships[protection.protector_id] = protection

   def clear(self):
      self.protection_relationships = {}

   def has_already_protected(self, actor_id: str) -> bool:
      existing_protection_relationship = self.protection_relationships.get(actor_id, None)
      if existing_protection_relationship is None:
         return True
      else:
         return False


   def is_protected(self, target_id: str) -> bool:
      return next(
         (
            True for relationship in self.protection_relationships.values()
            if relationship.protected_id == target_id
         ),
         False
      )

   def to_dict(self):
      import dataclasses
      return {
         "protection_relationships": {k: dataclasses.asdict(v) for k, v in self.protection_relationships.items()}
      }

