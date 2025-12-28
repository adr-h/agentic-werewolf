from typing import Awaitable
from typing import Callable
from typing import Type, Any
# from smolagents import Tool
from actions.Action import Action

# from agents import Agent, FunctionTool
from agents import RunContextWrapper, FunctionTool
import json

def action_to_tool(action: Action, action_executer: Callable[[Action], Awaitable[Any]]) -> FunctionTool:
    async def execute_action(ctx: RunContextWrapper[Any], args: str):
        try:
            data = json.loads(args)
            action.rationale = data.get("rationale")
        except json.JSONDecodeError:
            pass

        await action_executer(action)

    return FunctionTool(
        name=action.name.lower().replace(" ", "_"),
        description=action.description + ". Always provide a 'rationale'.",
        on_invoke_tool=execute_action,
        params_json_schema={
            "type": "object",
            "properties": {
                "rationale": {"type": "string", "description": "Why are you performing this action? What is your goal?"}
            },
            "required": ["rationale"]
        }
    )
