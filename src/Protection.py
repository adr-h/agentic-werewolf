from dataclasses import dataclass
from typing import Literal

@dataclass
class UnprotectedStatus:
   is_protected: Literal[False] = False

@dataclass
class ProtectedStatus:
   protector_id: str
   is_protected: Literal[True] = True

ProtectionStatus = ProtectedStatus | UnprotectedStatus