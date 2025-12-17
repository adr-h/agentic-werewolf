import asyncio
from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner, set_default_openai_client, SQLiteSession
import random
import string
from typing import Callable, Literal, Sequence

from GameState import GameView
from actions.Action import Action
from phases.Phase import PhaseType
from .Player import Player

type ActionsGetter = Callable[[], Sequence[Action]]

class AgenticPlayer(Player):
   id: str
   name: str
   type: Literal["agent_player"] = "agent_player"

   def __init__(self, name: str):
      self.id = 'agent_'.join(random.choices(string.ascii_uppercase + string.digits, k=10))
      self.name = 'agent_'.join(name)

   async def decide_action(self, prompt: str, game_view: GameView, get_actions: ActionsGetter) -> Action:
      possible_actions = get_actions()

      await asyncio.sleep(5)

      # TODO: get an option via AI
      return possible_actions[0]

   async def send_chat(self, message: str):
      raise NotImplementedError("TODO")