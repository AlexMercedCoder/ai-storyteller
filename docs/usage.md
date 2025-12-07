# Usage Guide

## Starting a Chat

To start a new story or resume an existing one:

```bash
storyteller start --provider openai --model gpt-4o
```

You will be prompted to enter a story name if starting a new one.

## Command Options

- `--provider`: Choose between `openai`, `anthropic`, or `gemini`.
- `--model`: Specify the model to use (e.g., `gpt-4o`, `claude-3-opus`, `gemini-1.5-pro`).
- `--story-id`: Resume a specific story by ID.

## MCP Server

To start the MCP server:

```bash
storyteller serve --port 8000
```
