from collections import Counter
from dataclasses import dataclass
from typing import Dict, Literal

from Character import Character

@dataclass
class NormalVote:
   voter_id: str
   target_id: str

@dataclass
class AbstainVote:
   voter_id: str

Vote = NormalVote | AbstainVote

@dataclass
class VoteBagView:
   votes: Dict[str, Vote] = {}

class VoteBag:
   votes: Dict[str, Vote] = {}

   def add_vote(self, voter_id: str, vote: Vote):
      self.votes[voter_id] = vote

   def clear(self):
      self.votes = {}

   def has_everyone_voted(self, everyone: list[Character]) -> bool:
      for voter in everyone:
         if (self.votes.get(voter.id) is None):
            return False

      return True

   def get_view(self, observer: Character) -> VoteBagView:
      own_vote = self.votes[observer.id]
      return VoteBagView(votes = {
         observer.id: own_vote
      })
      # for now, just return the character's own vote

   def get_most_voted(self) -> str | None:
      all_voted_targets = [v.target_id for v in self.votes.values() if isinstance(v, NormalVote)]
      if len(all_voted_targets) == 0:
         return None

      counts = Counter(all_voted_targets)
      winner, count = counts.most_common(1)[0]

      return winner

   # def remove_vote(self, voter_id: str):
   #    votes[]
