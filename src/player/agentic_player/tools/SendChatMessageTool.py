from typing import Callable, Awaitable
from smolagents import Tool

class SendChatMessageTool(Tool):
   name = "send_chat_message"
   description = "Send a chat message to all players"
   inputs = {"message": "str"}
   output_type = None

   chat_sender: Callable[[str], Awaitable[None]]

   def __init__(self, chat_sender: Callable[[str], Awaitable[None]]):
      self.chat_sender = chat_sender

   async def forward(self, message: str) -> None:
      self.chat_sender(message)