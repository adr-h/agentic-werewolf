
import asyncio
import os
from GameEngine import GameEngine
from GameState import GameState, GameView
from Character import Character
from Role import NormalVillagerRole, WerewolfRole
from Vote import VoteRegistry
from Hunt import HuntingRegistry
from Protection import ProtectionRegistry
from Autopsy import AutopsyRegistry
from Investigation import InvestigationRegistry
from phases.Hunting.HuntingPhase import HuntingPhase
from player.ManualPlayer import ManualPlayer
from player.Player import Player
from player.agentic_player.AgenticPlayer import AgenticPlayer
from events.Event import Event
from dotenv import load_dotenv

load_dotenv()

def get_cast():
    villager_1 = Character(name="Julio", role=NormalVillagerRole(), state="alive")
    player_1 = ManualPlayer(name=villager_1.name, character_id=villager_1.id, character=villager_1)

    villager_2 = Character(name="Fernandez", role=NormalVillagerRole(), state="alive")
    player_2 = ManualPlayer(name=villager_2.name, character_id=villager_2.id, character=villager_2)

    werewolf_1 = Character(name="Yuri", role=WerewolfRole(), state="alive")
    player_5 = AgenticPlayer(
        name=werewolf_1.name,
        character_id=werewolf_1.id,
        character=werewolf_1,
        model_id="openai/gpt-4o"
    )

    return [(villager_1, player_1), (villager_2, player_2), (werewolf_1, player_5)]

async def main():
    if "OPENROUTER_API_KEY" not in os.environ:
        print("Error: OPENROUTER_API_KEY environment variable is not set.")
        return

    cast = get_cast()
    all_characters = [pair[0] for pair in cast]
    all_players: list[Player] = [pair[1] for pair in cast]

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

    game_engine = GameEngine(players=all_players, game_state=game_state)

    # Monitor events
    def on_event(state: GameState, event: Event | None):
        if event:
            print(f"\n[EVENT] {event}")
        print(f"[PHASE] Current phase: {state.phase.__class__.__name__}")

    game_state.subscribe(on_event)

    print("Starting Headless Playtest...")
    await game_engine.game_loop()
    print("\nGame Over!")
    print(f"Winners: {game_state.winners}")

if __name__ == "__main__":
    asyncio.run(main())
