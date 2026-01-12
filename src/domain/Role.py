from dataclasses import dataclass
from typing import Literal

from .Enums import Faction

@dataclass(frozen=True)
class VillagerRole:
    name: Literal["Normal Villager"] = "Normal Villager"
    faction: Faction = Faction.VILLAGERS

    @property
    def description(self) -> str:
        return "You are a normal villager. Your goal is to identify and eliminate all Werewolves using logic and deduction. You vote during the day."

@dataclass(frozen=True)
class WerewolfRole:
    name: Literal["Werewolf"] = "Werewolf"
    faction: Faction = Faction.WEREWOLVES

    @property
    def description(self) -> str:
        return "You are a werewolf. You can eliminate one player during the Hunting Phase (Night). Your goal is to eliminate all villagers."

@dataclass(frozen=True)
class BodyguardRole:
    name: Literal["Bodyguard"] = "Bodyguard"
    faction: Faction = Faction.VILLAGERS

    @property
    def description(self) -> str:
        return "You are a bodyguard. You can protect one player from being hunted each night. You cannot protect yourself."

@dataclass(frozen=True)
class DoctorRole:
    name: Literal["Doctor"] = "Doctor"
    faction: Faction = Faction.VILLAGERS

    @property
    def description(self) -> str:
        return "You are a doctor. You can save one player from being hunted each night."

@dataclass(frozen=True)
class DetectiveRole:
    name: Literal["Detective"] = "Detective"
    faction: Faction = Faction.VILLAGERS

    @property
    def description(self) -> str:
        return "You are a detective. You can investigate one player per night to reveal their true role."

Role = VillagerRole | WerewolfRole | BodyguardRole | DoctorRole | DetectiveRole

def project_role_view(
    observed_id: str,
    observed_role: Role,
    observer_role: Role,
    knowledge: dict[str, str]
) -> str:
    """
    Pure visibility logic: How does a role appear to an observer?
    """
    # 1. Check explicit knowledge (Investigation Memory)
    if observed_id in knowledge:
        return knowledge[observed_id]

    # 2. Knowledge by faction (Werewolves know each other)
    # Observer knowledge
    is_observer_werewolf = observer_role.faction == Faction.WEREWOLVES
    is_observed_werewolf = observed_role.faction == Faction.WEREWOLVES

    if is_observer_werewolf and is_observed_werewolf:
        return observed_role.name

    # 3. Default: appears as Normal Villager
    return VillagerRole().name
