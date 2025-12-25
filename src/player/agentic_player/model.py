from smolagents.agents import CodeAgent
import huggingface_hub.inference._generated.types.zero_shot_image_classification
from typing import Literal
import os
from smolagents import OpenAIModel, LiteLLMModel
from dotenv import load_dotenv

load_dotenv()

RecognisedModels = Literal["openai/gpt-4o", "qwen/qwen3-8b", "google/gemini-3-flash-preview", "anthropic/claude-opus-4.5"]

def create_model(model_id: RecognisedModels) -> OpenAIModel:
   # return OpenAIModel(
   #    model_id=model_id,
   #    api_base="https://openrouter.ai/api/v1", # Leave this blank to query OpenAI servers.
   #    api_key=os.environ["OPENROUTER_API_KEY"],
   # )
   return LiteLLMModel(
      model_id=f"openrouter/{model_id}",
      base_url="https://openrouter.ai/api/v1",
      api_key=os.environ["OPENROUTER_API_KEY"]
   )

def create_agent(model_id: RecognisedModels) -> CodeAgent:
   return CodeAgent(
      model=create_model(model_id),
      tools=[],
      verbosity_level=0,
   )
