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

        def forward(self) -> str:
            import asyncio
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                # We are in an event loop (likely the one we want to run the action in)
                # But since Tool.forward is called synchronously by smolagents,
                # and smolagents is running in a thread (asyncio.to_thread),
                # we should use run_coroutine_threadsafe.
                from typing import Any
                asyncio.run_coroutine_threadsafe(action_executer(action), loop) # type: ignore
            else:
                # Fallback if no loop is running (unlikely in this app)
                asyncio.run(action_executer(action)) # type: ignore

            return f"Action {action.name} submitted."

    return GeneratedActionTool()
