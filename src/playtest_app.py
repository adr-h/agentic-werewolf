

from player.agentic_player.AgenticPlayer import AgenticPlayer
from Autopsy import AutopsyRegistry
from Character import Character
from GameEngine import GameEngine
from GameState import GameState
from Hunt import HuntingRegistry
from Investigation import InvestigationRegistry
from Protection import ProtectionRegistry
from Role import NormalVillagerRole, WerewolfRole
from Vote import VoteRegistry
from phases.Discussion.DiscussionPhase import DiscussionPhase
from phases.Hunting.HuntingPhase import HuntingPhase
from player.ManualPlayer import ManualPlayer
from player.Player import Player
import asyncio
from ui.WerewolfApp import WerewolfApp


async def main():
   cast = get_cast()

   all_characters = [ pair[0] for pair in cast ]
   all_players = [ pair[1] for pair in cast ]

   game_state = GameState(
      characters=all_characters,
      votes=VoteRegistry(),
      hunts=HuntingRegistry(),
      protection=ProtectionRegistry(),
      autopsy=AutopsyRegistry(),
      investigations=InvestigationRegistry(),
      events=[],
      phase=HuntingPhase(),
      winners=None,
      subscribers=[],
      is_chat_open=False
   )

   game_engine = GameEngine(
      players=all_players,
      game_state=game_state
   )

   # Start game loop
   asyncio.create_task(game_engine.game_loop())

   app = WerewolfApp(players=all_players)
   await app.run_async()


def get_cast() -> list[tuple[Character, Player]]:
   villager_1 = Character(
      name="Julio",
      role=NormalVillagerRole(),
      state="alive",
   )
   player_1 = ManualPlayer(
      name=villager_1.name,
      character_id=villager_1.id,
      character=villager_1
   )

   villager_2 = Character(
      name="Fernandez",
      role=NormalVillagerRole(),
      state="alive",
   )
   player_2 = ManualPlayer(
      name=villager_2.name,
      character_id=villager_2.id,
      character=villager_2
   )

   villager_3 = Character(
      name="Rodriguez",
      role=NormalVillagerRole(),
      state="alive",
   )
   player_3 = ManualPlayer(
      name=villager_3.name,
      character_id=villager_3.id,
      character=villager_3
   )

   villager_4 = Character(
      name="Mikail",
      role=NormalVillagerRole(),
      state="alive",
   )
   player_4 = ManualPlayer(
      name=villager_4.name,
      character_id=villager_4.id,
      character=villager_4
   )

   werewolf_1 = Character(
      name="Yuri",
      role=WerewolfRole(),
      state="alive",
   )
   player_5 = AgenticPlayer(
      name=werewolf_1.name,
      character_id=werewolf_1.id,
      character=werewolf_1,
      model_id="openai/gpt-4o"
   )
   # player_5 = ManualPlayer(
   #    name=werewolf_1.name,
   #    character_id=werewolf_1.id,
   #    character=werewolf_1
   # )

   return [
      (villager_1, player_1),
      (villager_2, player_2),
      (villager_3, player_3),
      (villager_4, player_4),
      (werewolf_1, player_5)
   ]

if __name__ == "__main__":
   asyncio.run(main())