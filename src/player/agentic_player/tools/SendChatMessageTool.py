from typing import Callable, Awaitable, Any
from agents import FunctionTool, RunContextWrapper
import json

def create_send_chat_message_tool(chat_sender: Callable[[str], Awaitable[None]]) -> FunctionTool:
   async def send_chat_message(ctx: RunContextWrapper[Any], args: str):
      try:
         data = json.loads(args)
         message = data.get("message", "")
      except json.JSONDecodeError:
         message = args

      await chat_sender(message)
      return f"Sent chat message: {message}"

   return FunctionTool(
      name="send_chat_message",
      description="Send a chat message to all players",
      on_invoke_tool=send_chat_message,
      params_json_schema={
         "type": "object",
         "properties": {
            "message": {"type": "string", "description": "The message to send"}
         },
         "required": ["message"]
      }
   )