from phases.GameOverPhase import GameOverPhase
from player.agentic_player.tools.DoNothingTool import DoNothingTool
from smolagents import Tool
from player.agentic_player.model import create_agent
from .model import RecognisedModels, CodeAgent
from .tools.ToolAdapter import action_to_tool
from .tools.SendChatMessageTool import SendChatMessageTool
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
   agent: CodeAgent

   def __init__(self, name: str, character_id: str, character: "Character", model_id: RecognisedModels):
      self.id = 'agent_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
      self.character_id=character_id
      self.character = character
      self.name = f"agent_{name}"
      self.agent = create_agent(model_id)

      print(f"[{self.name}] Initializing AgenticPlayer...")
      asyncio.create_task(self.agent_loop())

   def log_message(self, message: str):
      with open("agent.log", "a") as f:
         f.write(f"[{self.name}] {message}\n")

   async def agent_loop(self) -> None:
      interval = 5
      # Decide on an action every interval until the game ends.
      is_end_of_game = False
      while not is_end_of_game:
         await self.decide_action()
         is_end_of_game = self.current_game_view and isinstance(self.current_game_view.phase, GameOverPhase)
         await asyncio.sleep(interval)

   def get_tools(self) -> list[Tool]:
      tools = [
         action_to_tool(action, self.send_action) for action in self.possible_actions
      ]

      if self.current_game_view and self.current_game_view.is_chat_open:
         tools.append(
            SendChatMessageTool(
               chat_sender=self.send_chat
            )
         )

      tools.append(
         DoNothingTool()
      )

      return tools

   async def decide_action(self) -> None:
      tools = self.get_tools()

      self.agent._setup_tools(
         tools=tools,
         add_base_tools=False
      )

      self.log_message("Thinking...")
      # Run the synchronous agent.run in a separate thread to avoid blocking the event loop
      try:
         res = await asyncio.to_thread(
            self.agent.run,
            f"""
            You are an agent playing "Werewolf".

            TECHNICAL RULES:
            1. You MUST use one of the provided tools to take an action.
            2. If you don't want to do anything, call the 'do_nothing' tool.
            3. All tool calls MUST be wrapped in <code></code> blocks.
            4. When you are finished with your actions for this turn, you MUST call 'final_answer' with a brief status message to end your thinking process.

            ROLE:
            Your character is "{self.character.role.name}".
            {self.character.role.description}

            CURRENT STATE:
            {self.current_game_view}

            Based on your role and the state above, decide which tool to call.
            """
         )
         self.log_message(f"Final decision: {res}")
      except Exception as e:
         self.log_message(f"Error during decide_action: {e}")
         import traceback
         with open("agent.log", "a") as f:
            traceback.print_exc(file=f)