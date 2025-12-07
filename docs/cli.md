# CLI Command Reference

Storyteller provides a robust Command Line Interface (CLI) for managing your stories, configuring the server, and accessing DM tools.

## Global Options

These options apply to most commands or the application entry point.

- `--help`: Show help message and exit.
- `--storybase [TEXT]`: Name of the database file to use (default: `default`). Stored in `db/`.

## Commands

### `init`
Initializes the project structure in the current directory.
- **Usage**: `storyteller init`
- **Effect**: Creates `storyteller.db` (if missing) and populates the `lore/` directory with default markdown files.

### `start`
Starts the interactive chat session.
- **Usage**: `storyteller start [OPTIONS]`
- **Options**:
    - `--provider [openai|anthropic|gemini]`: Select the AI provider (default: `openai`).
    - `--model [TEXT]`: Specify the model name (e.g., `gpt-4o`, `claude-3-sonnet`).
    - `--story-id [INTEGER]`: Resume a specific story by its ID. If omitted, prompts to create a new story.

### `serve`
Starts the Storyteller MCP Server, exposing its tools to other clients.
- **Usage**: `storyteller serve [OPTIONS]`
- **Options**:
    - `--port [INTEGER]`: Port to run the server on (default: `8000`).

### `config`
Prints the configuration JSON needed to add Storyteller as an MCP server to other applications (like Claude Desktop).
- **Usage**: `storyteller config`
- **Output**: JSON block to copy-paste into `claude_desktop_config.json`.

### `dm-assist`
A collection of helper commands for Dungeon Masters to generate content quickly without entering a full chat session.

#### `dm-assist npc`
Generates a detailed NPC description.
- **Usage**: `storyteller dm-assist npc [OPTIONS]`
- **Options**:
    - `--archetype [TEXT]`: The type of NPC (e.g., "merchant", "guard", "wizard").
    - `--provider`, `--model`: AI configuration.

#### `dm-assist quest`
Generates a quest hook.
- **Usage**: `storyteller dm-assist quest [OPTIONS]`
- **Options**:
    - `--level [INTEGER]`: The target party level.
    - `--provider`, `--model`: AI configuration.

## Examples

**Start a new story with Claude 3:**
```bash
storyteller start --provider anthropic --model claude-3-opus-20240229
```

**Resume story #5:**
```bash
storyteller start --story-id 5
```

**Generate a high-level boss encounter:**
```bash
storyteller dm-assist npc --archetype "ancient lich" --model gpt-4o
```
