import asyncio
from player.agentic_player.tools.CommandAdapter import command_to_tool
from phases.voting.commands import CastVoteCommand
from phases.discussion.commands import SendChatMessageCommand
from phases.hunting.commands import NominateHuntCommand

async def dummy_on_command(cmd):
    pass

def verify():
    print("--- Verifying Command Docstrings ---")

    # Test CastVoteCommand
    vote_tool = command_to_tool(CastVoteCommand, "p1", dummy_on_command)
    print(f"Tool: {vote_tool.name}")
    print(f"Description:\n{vote_tool.description}")
    assert "Formally casts a vote" in vote_tool.description
    assert "Strategic Note" in vote_tool.description

    # Test SendChatMessageCommand
    chat_tool = command_to_tool(SendChatMessageCommand, "p1", dummy_on_command)
    print(f"\nTool: {chat_tool.name}")
    print(f"Description:\n{chat_tool.description}")
    assert "Broadcasts a message" in chat_tool.description

    # Test NominateHuntCommand
    hunt_tool = command_to_tool(NominateHuntCommand, "p1", dummy_on_command)
    print(f"\nTool: {hunt_tool.name}")
    print(f"Description:\n{hunt_tool.description}")
    assert "Nominate a target" in hunt_tool.description

    print("\n--- Verification SUCCESS ---")

if __name__ == "__main__":
    verify()
