import asyncio
import os
import sys

# Add src to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from domain.GameState import GameState
from domain.Character import Character
from domain.Role import VillagerRole, WerewolfRole, BodyguardRole, DetectiveRole, DoctorRole, Role
from engine.GameEngine import GameEngine
from player.agentic_player.AgenticPlayer import AgenticPlayer
from ui.tui import WerewolfTUI
from domain.RecognisedModels import RecognisedModels
from typing import List, Any
from pydantic import BaseModel, field_validator
import json

ROLE_MAP = {
    "Villager": VillagerRole,
    "Werewolf": WerewolfRole,
    "Bodyguard": BodyguardRole,
    "Doctor": DoctorRole,
    "Detective": DetectiveRole,
}

class PlayerConfig(BaseModel):
    name: str
    role: Role
    model: RecognisedModels

    @field_validator("role", mode="before")
    @classmethod
    def parse_role(cls, v: Any) -> Role:
        if isinstance(v, str):
            role_class = ROLE_MAP.get(v)
            if not role_class:
                raise ValueError(f"Unknown role: {v}. Valid roles: {list(ROLE_MAP.keys())}")
            return role_class()
        return v

async def main():
    # 1. Load Player Config
    config_path = "players.json"
    player_configs: List[PlayerConfig] = []

    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            raw_configs = json.load(f)
            player_configs = [PlayerConfig.model_validate(c) for c in raw_configs]
    else:
        # Fallback if config missing
        player_configs = [
            PlayerConfig(name="Alice",   role="Werewolf",  model="openai/gpt-4o"),
            PlayerConfig(name="Bob",     role="Villager",  model="openai/gpt-4o"),
            PlayerConfig(name="Charlie", role="Bodyguard", model="openai/gpt-4o"),
            PlayerConfig(name="David",   role="Detective", model="openai/gpt-4o"),
        ]

    # 2. Define Characters
    chars = []
    for i, config in enumerate(player_configs, 1):
        chars.append(Character(
            id=f"p{i}",
            name=config.name,
            role=config.role
        ))

    # 3. Setup Engine
    initial_state = GameState.create(chars)
    engine = GameEngine(initial_state)

    # 4. Setup Agentic Players
    players = [
        AgenticPlayer(
            character_id=f"p{i}",
            character_name=config.name,
            role_name=config.role.name,
            role_description=config.role.description,
            model_id=config.model,
            engine=engine
        )
        for i, config in enumerate(player_configs, 1)
    ]

    # 5. Start Engine tasks
    game_task = asyncio.create_task(engine.start())

    # 5. Start Player loops
    player_tasks = [asyncio.create_task(p.run_loop()) for p in players]

    # 6. Run TUI
    # Textual's run_async can be used to run alongside other tasks
    app = WerewolfTUI(engine, players)

    try:
        await app.run_async()
    finally:
        # Cleanup
        game_task.cancel()
        for t in player_tasks:
            t.cancel()
        await asyncio.gather(game_task, *player_tasks, return_exceptions=True)

if __name__ == "__main__":
    if "OPENROUTER_API_KEY" not in os.environ:
        print("ERROR: OPENROUTER_API_KEY not found in environment.")
    else:
        # We need to use asyncio.run but Textual's run_async handles the loop.
        # However, Textual 0.x uses its own loop management.
        # Let's use the standard approach for Textual + external tasks.
        asyncio.run(main())
