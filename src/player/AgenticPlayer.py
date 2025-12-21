import asyncio
from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner, set_default_openai_client, SQLiteSession
import random
import string
from typing import Callable, Literal, Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from GameState import GameView

from actions.Action import Action
from phases.Phase import PhaseType
from .Player import Player

type ActionsGetter = Callable[[], Sequence[Action]]

class AgenticPlayer(Player):
   id: str
   name: str
   type: Literal["agent_player"] = "agent_player"

   def __init__(self, name: str, character_id: str):
      self.id = 'agent_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
      self.character_id=character_id
      self.name = f"agent_{name}"

   # async def decide_action(self, prompt: str, game_view: GameView, get_actions: ActionsGetter) -> Action:
   #    possible_actions = get_actions()

   #    await asyncio.sleep(5)

   #    # TODO: get an option via AI
   #    return possible_actions[0]