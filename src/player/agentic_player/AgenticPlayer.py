from agents.run import Runner
from agents.agent import Agent
from phases.GameOverPhase import GameOverPhase
from smolagents import Tool
from player.agentic_player.model import create_agent
from .model import RecognisedModels
from .tools.ToolAdapter import action_to_tool
from .tools.DoNothingTool import create_do_nothing_tool
from .tools.SendChatMessageTool import create_send_chat_message_tool
import asyncio
import random
import string
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
   from GameState import GameView
   from Character import Character

from actions.Action import Action
from ..Player import Player

class AgenticPlayer(Player):
   id: str
   name: str
   type: Literal["agent_player"] = "agent_player"
   agent: Agent

   def __init__(self, name: str, character_id: str, character: "Character", model_id: RecognisedModels):
      self.id = 'agent_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
      self.character_id=character_id
      self.character = character
      self.name = f"agent_{name}"
      self.agent = create_agent(
         model_id=model_id,
         character_name=character.name,
         role_name= character.role.name,
         role_description=character.role.description,
      )

      print(f"[{self.name}] Initializing AgenticPlayer...")
      asyncio.create_task(self.agent_loop())

   def log_message(self, message: str):
      with open(f"{self.name}.log", "a") as f:
         f.write(f"[{self.name}] {message}\n")

   async def agent_loop(self) -> None:
      interval = 5
      # Decide on an action every interval until the game ends.
      is_end_of_game = False
      while not is_end_of_game:
         await self.decide_action()
         is_end_of_game = self.current_game_view and isinstance(self.current_game_view.phase, GameOverPhase)
         await asyncio.sleep(interval)

   def can_send_chat(self) -> bool:
      return bool(self.current_game_view and self.current_game_view.is_chat_open and self.character.state == "alive")

   def get_tools(self) -> list[Tool]:
      tools = [
         action_to_tool(action, self.send_action) for action in self.possible_actions
      ]

      if self.can_send_chat():
         tools.append(
            create_send_chat_message_tool(
               chat_sender=self.send_chat
            )
         )

      tools.append(
         create_do_nothing_tool()
      )

      return tools

   async def decide_action(self) -> None:
      if self.character.state == "dead":
         self.log_message("Character is already dead; no need to decide on any actions")
         return

      tools = self.get_tools()

      self.agent.tools.clear()
      self.agent.tools.extend([t for t in tools])

      self.log_message("Thinking...")
      try:
         #    TECHNICAL RULES:
         #    1. You MUST use one of the provided tools to take an action.
         #    2. If you don't want to do anything, call the 'do_nothing' tool.
         #    3. All tool calls MUST be wrapped in <code></code> blocks.
         #    4. When you are finished with your actions for this turn, you MUST call 'final_answer' with a brief status message to end your thinking process.

         #          ROLE:
         # Your character's name is "{self.character.name}".
         # Your character's role is "{self.character.role.name}".
         # {self.character.role.description}

         res = await Runner.run(
            starting_agent=self.agent,
            input=f"""
            CURRENT_PHASE: {self.current_game_view and self.current_game_view.phase.type}

            YOUR STATE: {self.character.state}

            VISIBLE_GAME_STATE:
            {self.current_game_view}
            Note: this is the visible game state, not the full, "true" game state.
            All players will appear to be "Normal Villagers" by default, even if they are werewolves/special roles (unless you have the investigation ability and have investigated them)

            Based on your role and the state above, decide which action to undertake (tool to call). Do not overthink this (perform this in 1-2 turns at most).
            """,
            max_turns=5,
         )

         self.log_message("output:"+res.final_output_as(str))
      except Exception as e:
         self.log_message(f"Error during decide_action: {e}")
         import traceback
         with open("agent_debug.log", "a") as f:
            traceback.print_exc(file=f)