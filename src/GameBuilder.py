
from Autopsy import AutopsyRegistry
from Character import Character
from GameEngine import GameEngine
from GameState import GameState
from Hunt import HuntingRegistry
from Investigation import InvestigationRegistry
from Protection import ProtectionRegistry
from Role import NormalVillagerRole, WerewolfRole
from Vote import VoteRegistry
from phases.Hunting.HuntingPhase import HuntingPhase
from player.ManualPlayer import ManualPlayer
from player.Player import Player

class GameBuilder:
    def __init__(self):
        self.players = []
        self.characters = []
        self.initial_phase = HuntingPhase()

    def add_player(self, name: str, role_type: str = "villager", is_manual: bool = True):
        role = NormalVillagerRole() if role_type == "villager" else WerewolfRole()
        char = Character(name=name, role=role, state="alive")
        self.characters.append(char)

        if is_manual:
            player = ManualPlayer(name=name, character_id=char.id)
        else:
            from player.AgenticPlayer import AgenticPlayer
            player = AgenticPlayer(name=name, character_id=char.id)

        self.players.append(player)
        return self

    def build_state(self) -> GameState:
        return GameState(
            characters=self.characters,
            votes=VoteRegistry(),
            hunts=HuntingRegistry(),
            protection=ProtectionRegistry(),
            autopsy=AutopsyRegistry(),
            investigations=InvestigationRegistry(),
            events=[],
            phase=self.initial_phase,
            winners=None,
            subscribers=[],
            is_chat_open=False
        )

    def build_engine(self) -> GameEngine:
        state = self.build_state()
        return GameEngine(players=self.players, game_state=state)

    def get_players(self) -> list[Player]:
        return self.players
