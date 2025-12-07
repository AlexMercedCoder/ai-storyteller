# Architecture

## Components

- **CLI**: Entry point for user interaction.
- **AIGateway**: Unified interface for LLM providers.
- **LoreManager**: Handles reading and indexing of Markdown lore files.
- **DatabaseManager**: Manages SQLite databases in the `db/` directory for state persistence.
- **MCPServer**: Exposes application functionality via Model Context Protocol.

## Data Flow

1. User inputs text via CLI.
2. CLI queries `LoreManager` for relevant context.
3. CLI queries `DatabaseManager` for story state and recent events.
4. CLI sends prompt + context to `AIGateway`.
5. `AIGateway` calls external API (OpenAI/Anthropic/Gemini).
6. Response is displayed and logged to `DatabaseManager`.
