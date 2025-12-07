from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static, ListView, ListItem, Label, TabbedContent, TabPane, Markdown as TextualMarkdown
from textual.containers import Container, Horizontal, Vertical
from textual.message import Message
import asyncio
from storyteller.db import DatabaseManager
from storyteller.lore import LoreManager
from storyteller.ai import AIGateway
from storyteller.mcp_client import MCPClientManager
from storyteller.mcp_server import get_lore, search_lore, get_story_summary, update_story_summary, roll_dice, list_characters, set_world_state, get_world_state
import json

class ChatMessage(Static):
    """A widget to display a chat message."""
    pass

class CharacterSheet(Static):
    """Displays character stats."""
    def compose(self) -> ComposeResult:
        yield Label("Character Stats", classes="header")
        yield Label("HP: 20/20", id="hp-label")
        yield Label("Gold: 50", id="gold-label")
        yield Label("Inventory:", classes="header")
        yield ListView(id="inventory-list")

    def update_stats(self, hp: int, gold: int, inventory: list):
        self.query_one("#hp-label").update(f"HP: {hp}/20")
        self.query_one("#gold-label").update(f"Gold: {gold}")
        # Update inventory list (simplified)

class LoreBrowser(Static):
    """Browses lore files."""
    def __init__(self, lore_manager: LoreManager):
        super().__init__()
        self.lore_manager = lore_manager

    def compose(self) -> ComposeResult:
        topics = self.lore_manager.get_all_lore_topics()
        yield Label("Lore Topics", classes="header")
        yield ListView(*[ListItem(Label(topic), name=topic) for topic in topics], id="lore-list")
        yield Container(id="lore-content")

    def on_list_view_selected(self, message: ListView.Selected):
        topic = message.item.name
        content = self.lore_manager.get_lore(topic)
        self.query_one("#lore-content").mount(TextualMarkdown(content))

class StorytellerApp(App):
    """A Textual app for Storyteller."""

    CSS = """
    Screen {
        layout: grid;
        grid-size: 3 1;
        grid-columns: 1fr 3fr 1fr;
    }

    .sidebar {
        background: $panel;
        border-right: vkey $accent;
        height: 100%;
        padding: 1;
    }

    .header {
        text-align: center;
        text-style: bold;
        background: $primary;
        color: $text;
        margin-bottom: 1;
    }

    .main-content {
        height: 100%;
        border-right: vkey $accent;
    }

    #chat-history {
        height: 1fr;
        overflow-y: scroll;
        padding: 1;
    }

    #user-input {
        dock: bottom;
    }

    ChatMessage {
        padding: 1;
        margin-bottom: 1;
        background: $surface;
        color: $text;
    }

    .user-message {
        text-align: right;
        background: $primary-darken-2;
    }

    .ai-message {
        text-align: left;
        background: $secondary-darken-2;
    }
    """

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def __init__(self, provider: str, model: str, story_id: int, storybase: str):
        super().__init__()
        self.provider = provider
        self.model = model
        self.story_id = story_id
        self.storybase = storybase
        self.db = DatabaseManager(storybase)
        self.lore = LoreManager()
        self.ai = AIGateway()
        self.mcp_client = MCPClientManager()
        self.internal_tools = [
            {"name": "get_lore", "function": get_lore, "server_name": "internal"},
            {"name": "search_lore", "function": search_lore, "server_name": "internal"},
            {"name": "get_story_summary", "function": get_story_summary, "server_name": "internal"},
            {"name": "update_story_summary", "function": update_story_summary, "server_name": "internal"},
            {"name": "roll_dice", "function": roll_dice, "server_name": "internal"},
            {"name": "list_characters", "function": list_characters, "server_name": "internal"},
            {"name": "set_world_state", "function": set_world_state, "server_name": "internal"},
            {"name": "get_world_state", "function": get_world_state, "server_name": "internal"}
        ]
        self.tools = []

    async def on_mount(self) -> None:
        """Called when app starts."""
        await self.mcp_client.connect_all()
        external_tools = await self.mcp_client.get_all_tools()
        self.tools = self.internal_tools + (external_tools if external_tools else [])
        
        # Load initial history
        recent_events = self.db.get_recent_events(self.story_id, limit=10)
        chat_history = self.query_one("#chat-history")
        for event in reversed(recent_events): # Display oldest first
            msg_class = "user-message" if event['description'].startswith("User:") else "ai-message"
            content = event['description'].replace("User: ", "").replace("AI: ", "")
            chat_history.mount(ChatMessage(content, classes=msg_class))

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        
        with Vertical(classes="sidebar"):
            yield CharacterSheet()

        with Vertical(classes="main-content"):
            with TabbedContent():
                with TabPane("Chat"):
                    yield Container(id="chat-history")
                    yield Input(placeholder="What do you want to do?", id="user-input")
                with TabPane("Lore"):
                    yield LoreBrowser(self.lore)

        with Vertical(classes="sidebar"):
            yield Label("World State")
            # Placeholder for world state
            yield Static("Location: Village\nTime: Night")

        yield Footer()

    async def on_input_submitted(self, message: Input.Submitted) -> None:
        """Handle user input."""
        user_input = message.value
        if not user_input:
            return

        chat_history = self.query_one("#chat-history")
        chat_history.mount(ChatMessage(user_input, classes="user-message"))
        self.query_one("#user-input").value = ""
        
        # Process turn
        await self.process_turn(user_input)

    async def process_turn(self, user_input: str):
        chat_history = self.query_one("#chat-history")
        
        # Logic similar to cli.py chat_loop
        relevant_lore = self.lore.search_lore(user_input)
        recent_events = self.db.get_recent_events(self.story_id, limit=5)
        events_text = "\n".join([f"- {e['description']}" for e in recent_events])
        story_summary = self.db.get_story(self.story_id).get("summary", "")

        system_instruction = f"""
        You are an AI Storyteller/Dungeon Master.
        Current Story Summary: {story_summary}
        Recent Events: {events_text}
        Relevant Lore: {relevant_lore}
        Your goal is to guide the player through the story.
        """

        # Call AI (blocking for TUI, ideally should be threaded/async properly)
        # Textual supports async handlers, so we can await
        response = self.ai.generate_response(
            prompt=user_input,
            system_instruction=system_instruction,
            provider=self.provider,
            model=self.model,
            tools=self.tools
        )

        # Handle tools (Simplified for TUI demo)
        if isinstance(response, list):
             # ... (Tool handling logic same as CLI) ...
             # For brevity, assuming text response for now or simple tool handling
             pass
        
        if isinstance(response, str):
            chat_history.mount(ChatMessage(response, classes="ai-message"))
            self.db.log_event(self.story_id, f"User: {user_input}")
            self.db.log_event(self.story_id, f"AI: {response[:50]}...")

    async def on_shutdown(self):
        await self.mcp_client.cleanup()

if __name__ == "__main__":
    # For testing
    app = StorytellerApp("openai", "gpt-4o", 1, "default")
    app.run()
