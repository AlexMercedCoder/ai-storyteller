# PyPI Installation & Usage Guide

This guide explains how to install and use `ai-storyteller-cli` directly from PyPI.

## Installation

Install the package using pip:

```bash
pip install ai-storyteller-cli
```

## Configuration

Before running the application, you need to set your API keys. You can do this by setting environment variables in your shell or by creating a `.env` file in your working directory.

### Environment Variables

- `OPENAI_API_KEY`: Required if using OpenAI (default).
- `ANTHROPIC_API_KEY`: Required if using Anthropic.
- `GEMINI_API_KEY`: Required if using Google Gemini.

Example (Linux/macOS):
```bash
export OPENAI_API_KEY="your-key-here"
```

Example (Windows PowerShell):
```powershell
$env:OPENAI_API_KEY="your-key-here"
```

## Initialization

Initialize the application to set up the database and lore directory:

```bash
storyteller init
```

This will create a `db/` folder for save files and a `lore/` folder for your world information in your current directory.

## Running the Application

Start a new story or resume an existing one:

```bash
storyteller start
```

### Options

- `--provider`: Choose the AI provider (`openai`, `anthropic`, `gemini`). Default: `openai`.
- `--model`: Specify the model (e.g., `gpt-4o`, `claude-3-5-sonnet-20240620`).
- `--tui`: Enable the rich Terminal User Interface.
- `--storybase`: Specify a custom database name (e.g., `my_campaign`).

Example:
```bash
storyteller start --provider anthropic --model claude-3-5-sonnet-20240620 --tui
```

## Updating

To update to the latest version:

```bash
pip install --upgrade ai-storyteller-cli
```
