from smolagents import Tool

class DoNothingTool(Tool):
   name = "do_nothing"
   description = "Stay silent and do nothing... for now."
   inputs = {}
   output_type = None

   def __init__(self):
      pass

   async def forward(self) -> None:
      pass