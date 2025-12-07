# Architecture Overview

Storyteller is a modular, AI-powered RPG application designed for extensibility and immersion. It combines a local Python CLI/TUI with powerful LLMs (OpenAI, Anthropic, Gemini) to act as a dynamic Dungeon Master.

## Core Components

### 1. Interface Layer
- **CLI (`storyteller/cli.py`)**: The main entry point using `typer`. Handles commands, configuration, and the standard chat loop.
- **TUI (`storyteller/tui.py`)**: A rich terminal user interface built with `textual`. Provides a dashboard with chat, character sheets, and lore browsing.

### 2. Logic Layer
- **AI Gateway (`storyteller/ai.py`)**: A unified interface for multiple AI providers. Handles prompt construction and tool calling.
- **Lore Manager (`storyteller/lore.py`)**: Manages static Markdown lore files.
    - **RAG**: Uses `lancedb` and `sentence-transformers` for vector-based retrieval.
    - **Fallback**: Uses keyword search if RAG dependencies are missing.
- **Database Manager (`storyteller/db.py`)**: Handles SQLite operations for persisting stories, characters, events, and world state.
- **Plugin Manager (`storyteller/plugins.py`)**: Dynamically loads external Python scripts to extend functionality.

### 3. Tooling Layer (MCP)
Storyteller implements the **Model Context Protocol (MCP)** to standardize tool usage.
- **Internal Server (`storyteller/mcp_server.py`)**: Exposes core functions (dice rolling, lore lookup, state management) as MCP tools.
- **Client Manager (`storyteller/mcp_client.py`)**: Connects to external MCP servers (e.g., Brave Search, filesystem) to give the AI more capabilities.

### 4. Content Generation
- **Procedural Tools (`storyteller/procedural.py`)**: Algorithms for generating dungeons and loot tables.
- **Export Tools (`storyteller/export.py`)**: Utilities for exporting stories to HTML and packing lore for sharing.

## Data Flow

1.  **User Input**: User types an action in CLI or TUI.
2.  **Context Assembly**:
    - `LoreManager` retrieves relevant lore (Vector/Keyword).
    - `DatabaseManager` retrieves recent chat history and world state.
3.  **AI Processing**:
    - `AIGateway` sends the prompt + context + tool definitions to the LLM.
4.  **Tool Execution**:
    - If the LLM calls a tool, `MCPClientManager` or the internal handler executes it.
    - Results are fed back to the LLM.
5.  **Response**: The LLM generates a narrative response.
6.  **Persistence**: The interaction is logged to SQLite.

## Directory Structure

```
storyteller/
├── db/                 # SQLite databases and LanceDB vectors
├── lore/               # Markdown lore files
├── plugins/            # User-created plugin scripts
├── storyteller/        # Source code
│   ├── cli.py          # CLI entry point
│   ├── tui.py          # Textual TUI
│   ├── ai.py           # AI integration
│   ├── db.py           # Database logic
│   ├── lore.py         # RAG and Lore logic
│   ├── mcp_server.py   # Internal MCP server
│   ├── mcp_client.py   # External MCP client
│   ├── procedural.py   # Generators
│   └── export.py       # Export utilities
├── tests/              # Pytest suite
└── docs/               # Documentation
```
