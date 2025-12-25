from agents.agent import Agent
from typing import Literal
import os
from dotenv import load_dotenv
from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()

RecognisedModels = Literal["openai/gpt-4o", "qwen/qwen3-8b", "google/gemini-3-flash-preview", "anthropic/claude-opus-4.5"]

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

def create_agent(model_id: RecognisedModels) -> Agent:
   agent = Agent(
      name="Assistant",
      instructions="""
      You are an agent playing the social deception game, "Werewolf".
      """,
      model=create_model(model_id),
      tools=[],
   )

   # agent.tools.extend
   return agent
