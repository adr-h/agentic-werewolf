from domain.Phase import VotingPhase
from phases.hunting.commands import NominateHuntCommand
import asyncio

from domain.GameState import GameState
from domain.Phase import HuntingPhase
from domain.Character import Character
from domain.Role import VillagerRole, WerewolfRole, BodyguardRole, DoctorRole
from engine.GameEngine import GameEngine
from domain.Engine import UserInput
from phases.voting.commands import CastVoteCommand

async def main():
    await voting_main()
    # await hunting_main()

async def hunting_main():
    # 1. Setup Data (Pure Data)
    chars = [
        Character(id="p1", name="Alice", role=VillagerRole()),
        Character(id="p2", name="Bob",   role=WerewolfRole()),
        Character(id="p3", name="Charlie", role=BodyguardRole()),
    ]

    initial_state = GameState(characters=tuple(chars), phase=HuntingPhase())
    engine = GameEngine(initial_state)

    # 2. Start Engine in background
    game_task = asyncio.create_task(engine.start())

    await asyncio.sleep(0.5) # Brief wait for engine to start

    # Cast Votes
    print(">>> Sending Votes...")
    await engine.queue_input(UserInput(NominateHuntCommand(actor_id="p2", target_id="p1")))

    # Wait for processing
    await asyncio.sleep(1)

    # Allow engine to execute (VotingDriver logic check should trigger)
    # VotingDriver checks "all_living_players_voted". 3 alive. 3 votes.
    # It should break loop and transition.

    await asyncio.sleep(2)

    print(">>> Game State after Hunting:")
    for e in engine.state.events:
        print(f"  - {e}")

    # Cleanup
    game_task.cancel()

async def voting_main():
    # 1. Setup Data (Pure Data)
    chars = [
        Character(id="p1", name="Alice", role=VillagerRole()),
        Character(id="p2", name="Bob",   role=WerewolfRole()),
        Character(id="p3", name="Charlie", role=BodyguardRole()),
    ]

    initial_state = GameState(characters=tuple(chars), phase=VotingPhase())
    engine = GameEngine(initial_state)

    # 2. Start Engine in background
    game_task = asyncio.create_task(engine.start())

    await asyncio.sleep(0.5) # Brief wait for engine to start

    # Cast Votes
    print(">>> Sending Votes...")
    await engine.queue_input(UserInput(CastVoteCommand(actor_id="p1", target_id="p2")))
    await engine.queue_input(UserInput(CastVoteCommand(actor_id="p3", target_id="p2")))
    await engine.queue_input(UserInput(CastVoteCommand(actor_id="p2", target_id="p1")))

    # Wait for processing
    await asyncio.sleep(1)

    # Allow engine to execute (VotingDriver logic check should trigger)
    # VotingDriver checks "all_living_players_voted". 3 alive. 3 votes.
    # It should break loop and transition.

    await asyncio.sleep(2)

    print(">>> Game State after Voting:")
    for e in engine.state.events:
        print(f"  - {e}")

    # Check if Bob died
    dead_bob = next((c for c in engine.state.characters if c.id == "p2"), None)
    if dead_bob and dead_bob.status == "dead":
        print(">>> SUCCESS: Bob (Werewolf) was executed!")
    else:
        print(">>> FAILURE: Bob is still alive.")

    # Cleanup
    game_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
