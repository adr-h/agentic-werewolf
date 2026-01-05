from enum import Enum

class Faction(Enum):
    VILLAGERS = "villagers"
    WEREWOLVES = "werewolves"
    NO_WINNERS_YET = "no_winners_yet"

class TimeOfDay(Enum):
    DAY = "day"
    NIGHT = "night"
