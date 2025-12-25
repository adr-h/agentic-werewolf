from typing import Awaitable
from typing import Callable
from typing import Type, Any
# from smolagents import Tool
from actions.Action import Action

# from agents import Agent, FunctionTool
from agents import RunContextWrapper, FunctionTool

def action_to_tool(action: Action, action_executer: Callable[[Action], Awaitable[Any]]) -> FunctionTool:
    async def execute_action(ctx: RunContextWrapper[Any], args: str):
        await action_executer(action)

    return FunctionTool(
        name=action.name.lower().replace(" ", "_"),
        description=action.description,
        on_invoke_tool=execute_action,
        params_json_schema={}
    )
