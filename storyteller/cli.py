import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.panel import Panel
from storyteller.db import DatabaseManager
from storyteller.lore import LoreManager
from storyteller.ai import AIGateway
from storyteller.mcp_server import mcp, get_lore, search_lore, get_story_summary, update_story_summary, roll_dice, list_characters, set_world_state, get_world_state
from storyteller.mcp_client import MCPClientManager
import asyncio
import json
import os
import sys

app = typer.Typer()
console = Console()
dm_app = typer.Typer(help="DM Assistance Tools")
app.add_typer(dm_app, name="dm-assist")

@app.command()
def init(storybase: str = typer.Option("default", help="Name of the story database")):
    """Initialize the storyteller application."""
    console.print("[green]Initializing Storyteller...[/green]")
    db = DatabaseManager(storybase)
    lore = LoreManager()
    console.print(f"[green]Initialization complete. Using database: {storybase}[/green]")

@app.command()
def serve(
    port: int = 8000,
    storybase: str = typer.Option("default", help="Name of the story database")
):
    """Start the MCP server."""
    console.print(f"[green]Starting MCP Server on port {port} using database '{storybase}'...[/green]")
    os.environ["STORYTELLER_DB_PATH"] = storybase
    mcp.run()

@app.command()
def config():
    """Print MCP configuration for external clients."""
    # Get the absolute path to the current python executable and the script
    # This is a best-effort guess for the configuration
    python_path = sys.executable
    script_path = os.path.abspath(sys.argv[0])
    
    # If installed as a package, we might want to use 'uv' or 'pip' based invocation
    # But here we'll provide a generic configuration
    
    config = {
      "mcpServers": {
        "storyteller": {
          "command": "uv", # Assuming uv is available, or use python_path
          "args": [
            "run",
            "storyteller",
            "serve"
          ]
        }
      }
    }
    
    console.print(Panel(json.dumps(config, indent=2), title="Claude Desktop Config (Example)", expand=False))
    console.print("\n[dim]Add this to your claude_desktop_config.json[/dim]")

@dm_app.command("npc")
def generate_npc(
    provider: str = typer.Option("openai", help="AI Provider"),
    model: str = typer.Option("gpt-4o", help="Model name"),
    archetype: str = typer.Option("villager", help="NPC Archetype"),
    storybase: str = typer.Option("default", help="Name of the story database")
):
    """Generate a random NPC."""
    # Note: DM assist currently doesn't persist, but if we wanted to log it, we'd use storybase
    ai = AIGateway()
    prompt = f"Generate a detailed NPC description for a fantasy RPG. Archetype: {archetype}. Include name, appearance, personality, and a secret."
    
    with console.status("[bold green]Generating NPC...[/bold green]"):
        response = ai.generate_response(prompt, provider=provider, model=model)
    
    console.print(Markdown(response))

@dm_app.command("quest")
def generate_quest(
    provider: str = typer.Option("openai", help="AI Provider"),
    model: str = typer.Option("gpt-4o", help="Model name"),
    level: int = typer.Option(1, help="Party Level"),
    storybase: str = typer.Option("default", help="Name of the story database")
):
    """Generate a quest hook."""
    ai = AIGateway()
    prompt = f"Generate a quest hook for a party of level {level}. Include title, hook, twist, and reward."
    
    with console.status("[bold green]Generating Quest...[/bold green]"):
        response = ai.generate_response(prompt, provider=provider, model=model)
    
    console.print(Markdown(response))

@dm_app.command("dungeon")
def generate_dungeon(
    rooms: int = typer.Option(5, help="Number of rooms")
):
    """Generate a random dungeon."""
    from storyteller.procedural import DungeonGenerator
    gen = DungeonGenerator(num_rooms=rooms)
    dungeon = gen.generate()
    
    console.print(f"[bold red]{dungeon['name']}[/bold red]")
    for room in dungeon["rooms"]:
        console.print(f"[bold]Room {room['id']}: {room['type']}[/bold]")
        console.print(f"  Encounter: {room['encounter']}")
        console.print(f"  Description: {room['description']}")
        console.print("")

@dm_app.command("loot")
def generate_loot(
    table_type: str = typer.Option("generic", help="Loot table type: generic, magic, treasure")
):
    """Generate random loot."""
    from storyteller.procedural import LootTable
    
    tables = {
        "generic": {"Gold Coin": 50, "Torch": 20, "Rope": 15, "Potion": 10, "Gem": 5},
        "magic": {"Potion of Healing": 40, "Scroll of Fireball": 30, "+1 Sword": 10, "Ring of Protection": 10, "Wand": 10},
        "treasure": {"Gold Pouch": 40, "Silver Bar": 30, "Ruby": 15, "Diamond": 10, "Crown": 5}
    }
    
    items = tables.get(table_type, tables["generic"])
    loot = LootTable(items).roll()
    console.print(f"[bold yellow]You found: {loot}[/bold yellow]")

@app.command()
def export(
    story_id: int = typer.Option(..., help="ID of the story to export"),
    output: str = typer.Option("story_export.html", help="Output filename"),
    storybase: str = typer.Option("default", help="Name of the story database")
):
    """Export a story to HTML."""
    from storyteller.export import StoryExporter
    exporter = StoryExporter(storybase)
    exporter.export_html(story_id, output)
    console.print(f"[green]Story exported to {output}[/green]")

@app.command()
def pack_lore(
    output: str = typer.Option("lore_pack.zip", help="Output filename")
):
    """Pack the lore directory into a zip file."""
    from storyteller.export import LorePacker
    packer = LorePacker()
    packer.pack(output)
    console.print(f"[green]Lore packed to {output}[/green]")

@app.command()
def validate():
    """Validate lore files."""
    lore_dir = Path("lore")
    if not lore_dir.exists():
        console.print("[red]Lore directory not found.[/red]")
        return

    errors = []
    for file_path in lore_dir.glob("*.md"):
        if file_path.stat().st_size == 0:
            errors.append(f"{file_path.name}: Empty file")
        # Add more checks here (e.g., header format)

    if errors:
        console.print("[red]Validation failed:[/red]")
        for error in errors:
            console.print(f"- {error}")
    else:
        console.print("[green]All lore files are valid.[/green]")

@app.command()
def start(
    provider: str = typer.Option("openai", help="AI Provider: openai, anthropic, gemini"),
    model: str = typer.Option("gpt-4o", help="Model name"),
    story_id: int = typer.Option(None, help="ID of an existing story to resume"),
    storybase: str = typer.Option("default", help="Name of the story database"),
    campaign_id: int = typer.Option(None, help="ID of a campaign template to start from"),
    tui: bool = typer.Option(False, help="Use Textual TUI")
):
    """Start the chat interface."""
    if tui:
        from storyteller.tui import StorytellerApp
        # We need to ensure story_id exists before starting TUI
        db = DatabaseManager(storybase)
        if not story_id:
            name = Prompt.ask("Enter a name for your new story")
            story_id = db.create_story(name)
        
        app = StorytellerApp(provider, model, story_id, storybase)
        app.run()
    else:
        # We need to run the async chat loop
        asyncio.run(chat_loop(provider, model, story_id, storybase, campaign_id))

async def chat_loop(provider: str, model: str, story_id: int, storybase: str, campaign_id: int = None):
    db = DatabaseManager(storybase)
    lore = LoreManager()
    ai = AIGateway()
    mcp_client = MCPClientManager()

    # Define Internal Tools
    internal_tools = [
        {
            "name": "get_lore",
            "description": "Retrieves lore about a specific topic.",
            "function": get_lore,
            "server_name": "internal"
        },
        {
            "name": "search_lore",
            "description": "Searches all lore files for a query.",
            "function": search_lore,
            "server_name": "internal"
        },
        {
            "name": "get_story_summary",
            "description": "Retrieves the summary of a story.",
            "function": get_story_summary,
            "server_name": "internal"
        },
        {
            "name": "update_story_summary",
            "description": "Updates the summary of a story.",
            "function": update_story_summary,
            "server_name": "internal"
        },
        {
            "name": "roll_dice",
            "description": "Rolls a number of dice with a given number of sides.",
            "function": roll_dice,
            "server_name": "internal"
        },
        {
            "name": "list_characters",
            "description": "Lists all characters in a story.",
            "function": list_characters,
            "server_name": "internal"
        },
        {
            "name": "set_world_state",
            "description": "Sets a key-value pair in the world state.",
            "function": set_world_state,
            "server_name": "internal"
        },
        {
            "name": "get_world_state",
            "description": "Gets the world state.",
            "function": get_world_state,
            "server_name": "internal"
        }
    ]

    # Load Plugins
    from storyteller.plugins import PluginManager
    plugin_manager = PluginManager()
    plugin_tools = plugin_manager.load_plugins()
    internal_tools.extend(plugin_tools)

    # Connect to external MCP servers
    console.print("[dim]Connecting to external MCP servers...[/dim]")
    await mcp_client.connect_all()
    
    # Fetch available tools
    external_tools = await mcp_client.get_all_tools()
    tools = internal_tools + (external_tools if external_tools else [])
    
    if tools:
        console.print(f"[green]Loaded {len(tools)} tools ({len(internal_tools)} internal, {len(external_tools) if external_tools else 0} external).[/green]")
        for tool in tools:
            console.print(f"  - [cyan]{tool['name']}[/cyan] ({tool.get('server_name')})")

    if not story_id:
        name = Prompt.ask("Enter a name for your new story")
        # If campaign_id is provided, we could potentially seed the story with campaign-specific details
        # For now, we just create a blank story
        story_id = db.create_story(name)
        console.print(f"[green]Created new story: {name} (ID: {story_id})[/green]")
    else:
        story = db.get_story(story_id)
        if not story:
            console.print(f"[red]Story ID {story_id} not found.[/red]")
            await mcp_client.cleanup()
            return
        console.print(f"[green]Resuming story: {story['name']}[/green]")

    console.print("[bold yellow]Welcome to Storyteller! Type 'exit' to quit.[/bold yellow]")
    
    story_summary = db.get_story(story_id).get("summary", "")
    turn_count = 0
    
    try:
        while True:
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]")
            if user_input.lower() in ["exit", "quit"]:
                break

            relevant_lore = lore.search_lore(user_input)
            recent_events = db.get_recent_events(story_id, limit=5)
            events_text = "\n".join([f"- {e['description']}" for e in recent_events])
            
            # Auto-Summarization Logic
            turn_count += 1
            if turn_count % 10 == 0:
                console.print("[dim]Auto-summarizing story...[/dim]")
                summary_prompt = f"Summarize the following recent events into the existing story summary. Keep it concise.\n\nExisting Summary:\n{story_summary}\n\nRecent Events:\n{events_text}"
                new_summary = ai.generate_response(summary_prompt, model=model, provider=provider)
                db.update_story_summary(story_id, new_summary)
                story_summary = new_summary

            system_instruction = f"""
            You are an AI Storyteller/Dungeon Master.
            
            Current Story Summary:
            {story_summary}
            
            Recent Events:
            {events_text}
            
            Relevant Lore:
            {relevant_lore}
            
            Note: Lore files starting with 'campaign_' represent specific campaign settings. Prioritize them if relevant.
            
            Your goal is to guide the player through the story.
            """

            with console.status("[bold green]Thinking...[/bold green]"):
                # Pass tools to generate_response for native tool calling
                response = ai.generate_response(
                    prompt=user_input,
                    system_instruction=system_instruction,
                    provider=provider,
                    model=model,
                    tools=tools
                )

            # Handle Native Tool Calls (OpenAI/Anthropic return list of tool calls)
            if isinstance(response, list):
                for tool_call in response:
                    # Extract tool details based on provider format
                    # OpenAI: tool_call.function.name, tool_call.function.arguments (str)
                    # Anthropic: tool_call["function"]["name"], tool_call["function"]["arguments"] (str)
                    
                    tool_name = ""
                    tool_args_str = "{}"
                    tool_call_id = None
                    
                    if hasattr(tool_call, 'function'): # OpenAI object
                        tool_name = tool_call.function.name
                        tool_args_str = tool_call.function.arguments
                        tool_call_id = tool_call.id
                    elif isinstance(tool_call, dict) and "function" in tool_call: # Anthropic dict
                         tool_name = tool_call["function"]["name"]
                         tool_args_str = tool_call["function"]["arguments"]
                         tool_call_id = tool_call.get("id")

                    try:
                        tool_args = json.loads(tool_args_str)
                    except json.JSONDecodeError:
                        tool_args = {}

                    # Find server
                    server_name = next((t["server_name"] for t in tools if t["name"] == tool_name), None)
                    
                    if server_name:
                        console.print(f"[dim]Calling tool {tool_name} on {server_name}...[/dim]")
                        
                        if server_name == "internal":
                            tool_func = next((t["function"] for t in internal_tools if t["name"] == tool_name), None)
                            if tool_func:
                                import inspect
                                sig = inspect.signature(tool_func)
                                if "story_id" in sig.parameters and "story_id" not in tool_args:
                                    tool_args["story_id"] = story_id
                                try:
                                    tool_result = tool_func(**tool_args)
                                except Exception as e:
                                    tool_result = f"Error: {e}"
                            else:
                                tool_result = "Error: Tool not found"
                        else:
                            tool_result = await mcp_client.call_tool(server_name, tool_name, tool_args)
                        
                        console.print(f"[dim]Result: {tool_result}[/dim]")
                        
                        # Feed back to AI
                        follow_up_prompt = f"Tool {tool_name} returned: {tool_result}. Continue."
                        # Note: For proper chat history, we should append messages, but here we just follow up
                        # A full chat history management is better for native tool use
                        response = ai.generate_response(
                            prompt=follow_up_prompt,
                            system_instruction=system_instruction,
                            provider=provider,
                            model=model
                        )
            
            # If response is still a list (e.g. multiple tool calls), we might need a loop or handle it better
            # For now, assume the final response is text
            if isinstance(response, str):
                console.print(Markdown(response))
                db.log_event(story_id, f"User: {user_input}")
                db.log_event(story_id, f"AI: {response[:50]}...")

    finally:
        await mcp_client.cleanup()

if __name__ == "__main__":
    app()
