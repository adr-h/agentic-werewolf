from agents import FunctionTool, RunContextWrapper
from typing import Any

def create_do_nothing_tool() -> FunctionTool:
   async def do_nothing(ctx: RunContextWrapper[Any], args: str):
      return "Did nothing."

   return FunctionTool(
      name="do_nothing",
      description="Stay silent and do nothing... for now. Always provide a 'rationale'.",
      on_invoke_tool=do_nothing,
      params_json_schema={
         "type": "object",
         "properties": {
            "rationale": {"type": "string", "description": "Why are you doing nothing?"}
         },
         "required": ["rationale"]
      }
   )