import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.panel import Panel
from storyteller.db import DatabaseManager
from storyteller.lore import LoreManager
from storyteller.ai import AIGateway
from storyteller.mcp_server import mcp
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

@app.command()
def start(
    provider: str = typer.Option("openai", help="AI Provider: openai, anthropic, gemini"),
    model: str = typer.Option("gpt-4o", help="Model name"),
    story_id: int = typer.Option(None, help="ID of an existing story to resume"),
    storybase: str = typer.Option("default", help="Name of the story database")
):
    """Start the chat interface."""
    # We need to run the async chat loop
    asyncio.run(chat_loop(provider, model, story_id, storybase))

async def chat_loop(provider: str, model: str, story_id: int, storybase: str):
    db = DatabaseManager(storybase)
    lore = LoreManager()
    ai = AIGateway()
    mcp_client = MCPClientManager()

    # Connect to external MCP servers
    console.print("[dim]Connecting to external MCP servers...[/dim]")
    await mcp_client.connect_all()
    
    # Fetch available tools
    tools = await mcp_client.get_all_tools()
    if tools:
        console.print(f"[green]Loaded {len(tools)} external tools.[/green]")
        for tool in tools:
            console.print(f"  - [cyan]{tool['name']}[/cyan] ({tool.get('server_name')})")

    if not story_id:
        name = Prompt.ask("Enter a name for your new story")
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
    
    try:
        while True:
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]")
            if user_input.lower() in ["exit", "quit"]:
                break

            relevant_lore = lore.search_lore(user_input)
            recent_events = db.get_recent_events(story_id, limit=5)
            events_text = "\n".join([f"- {e['description']}" for e in recent_events])
            
            # Simplified tool usage instruction
            tool_instruction = ""
            if tools:
                tool_instruction = "You have access to the following external tools. If you need to use one, output a JSON block like {\"tool\": \"tool_name\", \"args\": {...}}.\n"
                tool_instruction += "Available Tools:\n" + "\n".join([f"- {t['name']}: {t.get('description', '')}" for t in tools])

            system_instruction = f"""
            You are an AI Storyteller/Dungeon Master.
            
            Current Story Summary:
            {story_summary}
            
            Recent Events:
            {events_text}
            
            Relevant Lore:
            {relevant_lore}
            
            {tool_instruction}
            
            Your goal is to guide the player through the story.
            """

            with console.status("[bold green]Thinking...[/bold green]"):
                response = ai.generate_response(
                    prompt=user_input,
                    system_instruction=system_instruction,
                    provider=provider,
                    model=model
                )

            # Check for tool calls (Naive implementation)
            # In a real implementation, we'd use the provider's native tool calling capabilities
            # Here we just check if the response looks like a tool call JSON
            if response.strip().startswith("{") and "\"tool\"" in response:
                try:
                    tool_call = json.loads(response)
                    tool_name = tool_call.get("tool")
                    tool_args = tool_call.get("args", {})
                    
                    # Find which server has this tool
                    server_name = next((t["server_name"] for t in tools if t["name"] == tool_name), None)
                    
                    if server_name:
                        console.print(f"[dim]Calling tool {tool_name} on {server_name}...[/dim]")
                        tool_result = await mcp_client.call_tool(server_name, tool_name, tool_args)
                        
                        # Feed result back to AI
                        # For simplicity, we just print it and ask AI to continue
                        console.print(f"[dim]Tool Result: {tool_result}[/dim]")
                        
                        # Re-prompt AI with result
                        follow_up_prompt = f"Tool {tool_name} returned: {tool_result}. Please continue the story."
                        response = ai.generate_response(
                            prompt=follow_up_prompt,
                            system_instruction=system_instruction,
                            provider=provider,
                            model=model
                        )
                except json.JSONDecodeError:
                    pass # Not valid JSON, treat as text

            console.print(Markdown(response))
            
            db.log_event(story_id, f"User: {user_input}")
            db.log_event(story_id, f"AI: {response[:50]}...")

    finally:
        await mcp_client.cleanup()

if __name__ == "__main__":
    app()
