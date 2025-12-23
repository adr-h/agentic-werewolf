from typing import Awaitable
from typing import Callable
from typing import Type, Any
from smolagents import Tool
from actions.Action import Action

def action_to_tool(action: Action, action_executer: Callable[[Action], Awaitable[Any]]) -> Tool:
    """
    Converts an Action class into a smolagents Tool.

    Args:
        action: The Action to convert.
        action_executer: The function that will execute the action.

    Returns:
        An instance of a smolagents Tool.
    """

    class GeneratedActionTool(Tool):
        name = action.name.lower().replace(" ", "_")
        description = action.description
        inputs = action.tool_inputs
        output_type = action.tool_output_type

        async def forward(self, **kwargs) -> None:
            await action_executer(action)

    return GeneratedActionTool()
