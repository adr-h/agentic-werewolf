import asyncio
import random
import string
from typing import Optional

from agents.agent import Agent
from agents.run import Runner
from domain.Engine import EngineProtocol, UserInput
from domain.GameState import GameState
from domain.Character import Character
from domain.RecognisedModels import RecognisedModels
from .agent import create_agent
from .projections import get_agent_view, get_available_commands
from .tools.CommandAdapter import command_to_tool
from .tools.DoNothingTool import create_do_nothing_tool

class AgenticPlayer:
    def __init__(
        self,
        character_id: str,
        character_name: str,
        role_name: str,
        role_description: str,
        model_id: RecognisedModels,
        engine: EngineProtocol
    ):
        self.character_id = character_id
        self.character_name = character_name
        self.model_id = model_id
        self.engine = engine
        self.agent = create_agent(
            model_id=model_id,
            character_name=character_name,
            role_name=role_name,
            role_description=role_description
        )
        self.name = f"agent_{character_name}_{random.choice(string.ascii_uppercase)}"
        self.command_history = []

        print(f"[{self.name}] Initialized DMMF Agentic Player.")

    async def run_loop(self):
        """
        Periodically checks if it should act.
        In DMMF, this could also be triggered by a notification.
        """
        while True:
            await self.think_and_act()
            await asyncio.sleep(10) # Thinking interval

    async def think_and_act(self):
        state = self.engine.state

        # 1. Check if alive
        me = next((c for c in state.characters if c.id == self.character_id), None)
        if not me or me.status == "dead":
            return

        # 2. Get Available Commands
        cmd_classes = get_available_commands(state, self.character_id)

        # 3. Setup Tools
        tools = []
        for cmd_cls in cmd_classes:
            tool = command_to_tool(
                command_class=cmd_cls,
                actor_id=self.character_id,
                on_command=self._handle_command
            )
            tools.append(tool)

        # Add pure utility tools
        tools.append(create_do_nothing_tool())

        self.agent.tools.clear()
        self.agent.tools.extend(tools)

        # 4. Agent View
        view = get_agent_view(state, self.character_id)

        # 5. Run Agent
        try:
            print(f"[{self.name}] Thinking...")
            res = await Runner.run(
                starting_agent=self.agent,
                input=f"YOUR VIEW:\n{view}\n\nDecision time. Choose an action.",
                max_turns=3
            )
        except Exception as e:
            print(f"[{self.name}] Error during thinking: {e}")

    async def _handle_command(self, cmd):
        """Callback from tools."""
        print(f"[{self.name}] Pushing command {cmd}")
        self.command_history.append(cmd)
        # We need a way to push to the engine's queue.
        # Concrete GameEngine has `queue_input`. EngineProtocol might need it?
        # Or we cast it. DMMF usually has a "Sink".
        if hasattr(self.engine, 'queue_input'):
            await self.engine.queue_input(UserInput(cmd))
