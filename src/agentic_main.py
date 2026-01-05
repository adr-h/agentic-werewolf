import asyncio
import os
from domain.GameState import GameState
from domain.Character import Character
from domain.Role import VillagerRole, WerewolfRole, BodyguardRole, DetectiveRole
from engine.GameEngine import GameEngine
from player.agentic_player.DMMFAgenticPlayer import DMMFAgenticPlayer

# Role Descriptions (from old Role.py)
VILLAGER_DESC = "You are a normal villager. Your goal is to identify and eliminate all Werewolves using logic and deduction. You vote during the day."
WEREWOLF_DESC = "You are a werewolf. You can eliminate one player during the Hunting Phase (Night). Your goal is to eliminate all villagers."
BODYGUARD_DESC = "You are a bodyguard. You can protect one player from being hunted each night. You cannot protect yourself."
DETECTIVE_DESC = "You are a detective. You can investigate one player per night to reveal their true role."

async def main():
    print("=== STARTING AGENTIC WEREWOLF (DMMF) ===")

    # 1. Define Characters
    chars = [
        Character(id="p1", name="Alice",   role=WerewolfRole()),
        Character(id="p2", name="Bob",     role=VillagerRole()),
        Character(id="p3", name="Charlie", role=BodyguardRole()),
        Character(id="p4", name="David",   role=DetectiveRole()),
    ]

    # 2. Setup Engine
    initial_state = GameState.create(chars)
    engine = GameEngine(initial_state)

    # 3. Setup Agentic Players
    players = [
        DMMFAgenticPlayer("p1", "Alice", "Werewolf", WEREWOLF_DESC, "openai/gpt-4o", engine),
        DMMFAgenticPlayer("p2", "Bob", "Normal Villager", VILLAGER_DESC, "openai/gpt-4o", engine),
        DMMFAgenticPlayer("p3", "Charlie", "Bodyguard", BODYGUARD_DESC, "openai/gpt-4o", engine),
        DMMFAgenticPlayer("p4", "David", "Detective", DETECTIVE_DESC, "openai/gpt-4o", engine),
    ]

    # 4. Start Engine tasks
    game_task = asyncio.create_task(engine.start())

    # 5. Start Player loops
    player_tasks = [asyncio.create_task(p.run_loop()) for p in players]

    print("=== LIVE SIMULATION RUNNING ===")

    try:
        # Run for a reasonable amount of time or until game over
        # For a quick test, let's run for 3 minutes or until end.
        while True:
            await asyncio.sleep(5)
            # Check for Game Over (this is a bit simplistic)
            # In DMMF, we'd check state.phase
            from domain.Phase import GameOverPhase
            if isinstance(engine.state.phase, GameOverPhase):
                print(f"!!! GAME OVER: Winner is {engine.state.phase.winner} !!!")
                break

    except asyncio.CancelledError:
        pass
    finally:
        game_task.cancel()
        for t in player_tasks:
            t.cancel()
        print("=== SIMULATION ENDED ===")

if __name__ == "__main__":
    # Ensure API Key
    if "OPENROUTER_API_KEY" not in os.environ:
        print("ERROR: OPENROUTER_API_KEY not found in environment.")
    else:
        asyncio.run(main())
