from typing import Callable, Awaitable, Any
from agents import FunctionTool, RunContextWrapper
import json

def create_send_chat_message_tool(chat_sender: Callable[[str, str | None, str | None], Awaitable[None]]) -> FunctionTool:
   async def send_chat_message(ctx: RunContextWrapper[Any], args: str):
      try:
         data = json.loads(args)
         message = data.get("message", "")
         rationale = data.get("rationale")
         strategy = data.get("strategy")
      except json.JSONDecodeError:
         message = args
         rationale = None
         strategy = None

      await chat_sender(message, rationale, strategy)
      return f"Sent chat message: {message}"

   return FunctionTool(
      name="send_chat_message",
      description="Send a chat message to all players. Use 'strategy' to categorize your message (e.g., 'deception', 'investigation', 'defense', 'accusation', 'other'). Always provide a 'rationale'.",
      on_invoke_tool=send_chat_message,
      params_json_schema={
         "type": "object",
         "properties": {
            "message": {"type": "string", "description": "The message to send"},
            "rationale": {"type": "string", "description": "Why are you sending this message? What is your goal?"},
            "strategy": {"type": "string", "description": "The category of your chat strategy."}
         },
         "required": ["message", "rationale", "strategy"]
      }
   )