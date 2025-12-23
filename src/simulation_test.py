
import asyncio
import time
from GameBuilder import GameBuilder

async def run_simulation():
    print("Starting Headless Werewolf Simulation...")
    builder = GameBuilder()

    # Add 4 villagers and 1 werewolf (all agentic for simulation)
    builder.add_player("Julio", role_type="villager", is_manual=False)
    builder.add_player("Fernandez", role_type="villager", is_manual=False)
    builder.add_player("Rodriguez", role_type="villager", is_manual=False)
    builder.add_player("Mikail", role_type="villager", is_manual=False)
    builder.add_player("Yuri", role_type="werewolf", is_manual=False)

    engine = builder.build_engine()
    state = engine.game_state

    # Subscribe to state changes to log events
    def log_event(gs, event):
        if event:
            print(f"[EVENT] {event.__class__.__name__}")

    state.subscribe(log_event)

    start_time = time.time()

    # Run the game loop
    # We'll run it until the game is over (Phase is None after next transitions)
    # However, game_loop is an infinite loop that breaks internally.
    # We should run it as a task and wait for it.

    loop_task = asyncio.create_task(engine.game_loop())

    # Since our agents are currently placeholders that don't do anything,
    # and the phases wait for 30s but wake up on actions...
    # Oh wait, the agents don't actually SEND actions yet because they are placeholders.
    # So it will still wait 10s intervals.

    # To truly test "rapid" simulation, we'd need agents that act.
    # Let's mock an agent acting.

    print("Simulation started. Waiting for game to progress...")

    # Wait for a bit to see if it moves
    while not loop_task.done():
        await asyncio.sleep(0.1)
        # Force game over for testing purposes if it takes too long
        if time.time() - start_time > 5:
            print("Simulation timed out (expected as agents are placeholders).")
            break

    end_time = time.time()
    print(f"Simulation finished in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(run_simulation())
