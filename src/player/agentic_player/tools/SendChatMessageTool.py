from typing import Callable, Awaitable
from smolagents import Tool
import asyncio

class SendChatMessageTool(Tool):
   name = "send_chat_message"
   description = "Send a chat message to all players"
   inputs = {"message": {"type": "string", "description": "The message to send"}}
   output_type = "string"

   chat_sender: Callable[[str], Awaitable[None]]

   def __init__(self, chat_sender: Callable[[str], Awaitable[None]]):
      super().__init__()
      self.chat_sender = chat_sender

   def forward(self, message: str) -> str:
      try:
         loop = asyncio.get_running_loop()
      except RuntimeError:
         loop = None

      if loop and loop.is_running():
         asyncio.run_coroutine_threadsafe(self.chat_sender(message), loop)
      else:
         asyncio.run(self.chat_sender(message))

      return f"Sent chat message: {message}"