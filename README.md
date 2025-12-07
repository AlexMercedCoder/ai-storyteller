# AI Storyteller

**Your AI-Powered Dungeon Master Assistant**

Storyteller is a CLI-based application that uses Large Language Models (LLMs) to run tabletop roleplaying games. It manages lore, tracks story state, and acts as an immersive Dungeon Master.

## Features

- **Multi-Provider AI**: Support for OpenAI, Anthropic, and Gemini.
- **Lore Management**: Local Markdown-based lore system with smart retrieval.
- **Persistence**: SQLite database for saving stories, characters, and events.
- **MCP Support**:
    - **Server**: Expose Storyteller tools to Claude Desktop.
    - **Client**: Connect Storyteller to external tools (Web Search, etc.).

## Documentation Index

| Topic | Description |
|-------|-------------|
| **[Setup Guide](docs/setup.md)** | Installation, API keys, and initialization. |
| **[PyPI Installation](docs/pypi_install.md)** | Installing and using from PyPI. |
| **[GitHub & Template Guide](docs/github_setup.md)** | Cloning, setup, and creating custom distributions. |
| **[Database Guide](docs/db.md)** | Understanding the schema and managing save files. |
| **[RAG & Vector Search](docs/rag.md)** | How the AI remembers lore using vector embeddings. |
| **[Procedural Tools](docs/procedural.md)** | Generating dungeons and loot. |
| **[Export & Sharing](docs/export_sharing.md)** | Exporting stories and packing lore. |
| **[Plugin System](docs/plugins.md)** | Extending Storyteller with Python scripts. |
| **[Textual TUI](docs/tui.md)** | Using the rich terminal interface. |
| **[Publishing Guide](docs/publishing.md)** | Packaging and distributing the library. |
| **[Quick Start](docs/usage.md)** | Basic usage instructions. |
| **[Chat Interface](docs/chat.md)** | Deep dive into how to play and interact. |
| **[CLI Reference](docs/cli.md)** | Complete command list (`start`, `serve`, `dm-assist`). |
| **[Lore Guide](docs/lore.md)** | How to write and organize your world's lore. |
| **[MCP Integration](docs/mcp.md)** | Configuring MCP Server and Client modes. |
| **[Best Practices](docs/bestpractices.md)** | Tips for better prompting and game management. |
| **[Architecture](docs/architecture.md)** | System design and component overview. |

## Quick Start

1.  **Install**: ```bash
pip install ai-storyteller-cli
# OR for RAG support:
pip install "ai-storyteller-cli[rag]"
```
2.  **Configure**: Create `.env` with API keys.
3.  **Init**: `storyteller init`
4.  **Play**: `storyteller start`

## License
MIT
