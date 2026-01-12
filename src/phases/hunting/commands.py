from dataclasses import dataclass, field
from domain.Command import Command

@dataclass(frozen=True, kw_only=True)
class NominateHuntCommand(Command):
    """
    Nominate a target for the werewolves to kill during the night.
    Available only to the Werewolf role.

    Strategic Note: Coordinate with your pack to target players who are
    perceived as threats (like known Detectives) or those whose deaths
    will cause the most confusion among the villagers.
    """
    target_id: str = field(metadata={"description": "The ID of the player the werewolves should hunt."})

@dataclass(frozen=True, kw_only=True)
class ProtectCommand(Command):
    """
    Choose a player to protect from death tonight.
    Available only to the Bodyguard role.

    Strategic Note: Protecting yourself is safe, but protecting a key leader
    like the Detective can turn the tide of the game. Try to predict who
    the werewolves will target next.
    """
    target_id: str = field(metadata={"description": "The ID of the player to protect from death tonight."})

@dataclass(frozen=True, kw_only=True)
class InvestigateCommand(Command):
    """
    Reveal the secret role of a target player.
    Available only to the Detective role.

    Strategic Note: Information is power. Once you identify a werewolf,
    you must carefully choose when and how to reveal this to the village
    without painting a target on your own back.
    """
    target_id: str = field(metadata={"description": "The ID of the player to reveal the role of."})
