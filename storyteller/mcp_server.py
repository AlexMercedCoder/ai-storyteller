from mcp.server.fastmcp import FastMCP
from storyteller.db import DatabaseManager
from storyteller.lore import LoreManager
import random
import os

# Initialize managers
lore = LoreManager()

def get_db():
    storybase = os.environ.get("STORYTELLER_DB_PATH", "default")
    return DatabaseManager(storybase)

# Create MCP Server
mcp = FastMCP("Storyteller")

@mcp.tool()
def get_lore(topic: str) -> str:
    """Retrieves lore about a specific topic."""
    content = lore.get_lore(topic)
    if content:
        return content
    return f"No lore found for topic: {topic}"

@mcp.tool()
def search_lore(query: str) -> str:
    """Searches all lore files for a query."""
    return lore.search_lore(query)

@mcp.tool()
def get_story_summary(story_id: int) -> str:
    """Retrieves the summary of a story."""
    db = get_db()
    story = db.get_story(story_id)
    if story:
        return story.get("summary", "")
    return "Story not found."

@mcp.tool()
def update_story_summary(story_id: int, summary: str) -> str:
    """Updates the summary of a story."""
    db = get_db()
    db.update_story_summary(story_id, summary)
    return "Story summary updated."

@mcp.tool()
def roll_dice(sides: int = 20, count: int = 1) -> str:
    """Rolls a number of dice with a given number of sides."""
    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls)
    return f"Rolled {count}d{sides}: {rolls} (Total: {total})"

@mcp.tool()
def list_characters(story_id: int) -> str:
    """Lists all characters in a story."""
    db = get_db()
    chars = db.get_characters(story_id)
    if not chars:
        return "No characters found."
    return "\n".join([f"{c['id']}: {c['name']}" for c in chars])

@mcp.tool()
def set_world_state(story_id: int, key: str, value: str) -> str:
    """Sets a key-value pair in the world state."""
    db = get_db()
    db.set_world_state(story_id, key, value)
    return f"Set {key} to {value}."

@mcp.tool()
def get_world_state(story_id: int) -> str:
    """Gets the world state."""
    db = get_db()
    state = db.get_world_state(story_id)
    return str(state)

if __name__ == "__main__":
    mcp.run()
