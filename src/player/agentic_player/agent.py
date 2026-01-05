from agents.agent import Agent
from typing import Literal
import os
from dotenv import load_dotenv
from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()

RecognisedModels = Literal[
   "openai/gpt-4o",
   "openai/gpt-oss-120b",
   "minimax/minimax-m2",
   "qwen/qwen3-8b",
   "qwen/qwen3-14b",
   "google/gemini-2.5-flash-lite",
   "google/gemini-3-flash-preview",
   "anthropic/claude-opus-4.5",
   "x-ai/grok-4.1-fast"
]

def create_model(model_id: RecognisedModels) -> LitellmModel:
   # return OpenAIModel(
   #    model_id=model_id,
   #    api_base="https://openrouter.ai/api/v1", # Leave this blank to query OpenAI servers.
   #    api_key=os.environ["OPENROUTER_API_KEY"],
   # )
   return LitellmModel(
      model=f"openrouter/{model_id}",
      api_key=os.environ["OPENROUTER_API_KEY"],
      base_url="https://openrouter.ai/api/v1",
   )

def create_agent(model_id: RecognisedModels, character_name: str, role_name: str, role_description: str) -> Agent:
   agent = Agent(
      name="Werewolf Player",
      instructions=f"""
      You are an agent playing the social deception game, "Werewolf".

      RULES:
      Werewolf is a social deception game where players are divided into two factions: the Villagers and the Werewolves. The game progresses through three main phases: the Discussion Phase where players talk and deduce; the Voting Phase where players vote to eliminate a suspect; and the Hunting Phase where Werewolves and special roles perform secret actions. Villagers win if all Werewolves are eliminated, while Werewolves win if they equal or outnumber the living Villagers.

      ROLES:
      - Normal Villager: Uses logic and deduction to find werewolves; has no special powers.
      - Werewolf: Can eliminate one player per night during the Hunting Phase.
      - Bodyguard: Protects one player (excluding themselves) from being hunted each night.
      - Detective: Investigates one player per Hunting Phase to reveal their true role.
      - Doctor: Performs an autopsy on a deceased player during the Discussion Phase to reveal their role.
      Note that the only guaranteed roles to appear for each game are Normal Villager and Werewolf. The other roles may or may not appear.

      TECHNICAL RULES:
      1. You MUST use one of the provided tools to take an action.
      2. If you don't want to do anything, call the 'do_nothing' tool.
      3. You MUST provide a 'rationale' for every tool call explaining your goal.
      4. For chat messages, you MUST provide a 'strategy' (e.g., 'deception', 'investigation', 'defense', 'accusation', 'other').

      ROLE:
         Your character's name is "{character_name}".
         Your character's role is "{role_name}".
         {role_description}
      """,
      model=create_model(model_id),
      tools=[],
   )

   # agent.tools.extend
   return agent
