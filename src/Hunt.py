from dataclasses import dataclass

@dataclass
class Hunting:
   hunter_id: str
   prey_id: str

class HuntingRegistry:
   latest_hunt: Hunting | None = None

   def add_hunting(self, hunting: Hunting):
      self.latest_hunt = hunting

   def clear(self):
      self.latest_hunt = None

   def get_hunted(self) -> str | None:
      if self.latest_hunt is None:
         return None

      return self.latest_hunt.prey_id

   def to_dict(self):
      import dataclasses
      return {
         "latest_hunt": dataclasses.asdict(self.latest_hunt) if self.latest_hunt else None
      }
