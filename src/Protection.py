from dataclasses import dataclass
from typing import Literal

@dataclass
class Protection:
   protector_id: str
   protected_id: str

class ProtectionBag:
   protection_relationships: dict[str, Protection] = {}

   def add_protection(self, protection: Protection):
      self.protection_relationships[protection.protector_id] = protection

   def clear(self):
      self.protection_relationships = {}

   def is_protected(self, target_id: str) -> bool:
      return next(
         (
            True for relationship in self.protection_relationships.values()
            if relationship.protected_id == target_id
         ),
         False
      )

