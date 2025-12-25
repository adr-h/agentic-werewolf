from smolagents import Tool

class DoNothingTool(Tool):
   name = "do_nothing"
   description = "Stay silent and do nothing... for now."
   inputs = {}
   output_type = "string"

   def __init__(self):
      super().__init__()

   def forward(self) -> str:
      return "Did nothing."