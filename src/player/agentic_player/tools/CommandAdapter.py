import json
from typing import Type, Callable, Any, Awaitable
from dataclasses import fields, is_dataclass
from agents import FunctionTool, RunContextWrapper
from domain.Command import Command

def command_to_tool(
    command_class: Type[Command],
    actor_id: str,
    on_command: Callable[[Command], Awaitable[Any]]
) -> FunctionTool:
    """
    Converts a Command dataclass into a smolagents FunctionTool.
    """
    name = command_class.__name__.replace("Command", "").lower()

    # Introspect fields
    command_fields = fields(command_class)

    # We ignore 'actor_id' in the tool parameters as it's provided by the context
    param_fields = [f for f in command_fields if f.name != "actor_id"]

    # Build JSON schema properties
    properties = {}
    required = []

    # If the command class doesn't already have 'rationale', add it as a helpful tool param
    # (Though we might want to encourage adding it to all commands eventually)
    has_rationale = any(f.name == "rationale" for f in param_fields)

    if not has_rationale:
        properties["rationale"] = {
            "type": "string",
            "description": "Why you are taking this action (for internal log)."
        }
        required.append("rationale")

    for f in param_fields:
        desc = f.metadata.get("description", f"The {f.name} parameter.")

        # Simple type mapping
        json_type = "string"
        if f.type is int:
            json_type = "integer"
        elif f.type is bool:
            json_type = "boolean"

        properties[f.name] = {
            "type": json_type,
            "description": desc
        }
        # Check if field has a default value (making it optional in JSON schema)
        from dataclasses import MISSING
        if f.default is MISSING and f.default_factory is MISSING:
            required.append(f.name)

    async def execute_wrapper(ctx: RunContextWrapper[Any], args: str):
        data = json.loads(args)

        # Instantiate the command
        # Build kwargs from data, filtered to only what the command class accepts
        kwargs = {f.name: data.get(f.name) for f in param_fields if f.name in data}
        kwargs["actor_id"] = actor_id

        cmd_instance = command_class(**kwargs)
        await on_command(cmd_instance)

        return f"Command {name} sent successfully."

    return FunctionTool(
        name=name,
        description=f"Performs the {name} action. Parameters: {', '.join(required)}",
        on_invoke_tool=execute_wrapper,
        params_json_schema={
            "type": "object",
            "properties": properties,
            "required": required
        }
    )
