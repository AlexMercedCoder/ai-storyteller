# Setup Guide

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install .
   ```

## Configuration

### Environment Variables

Create a `.env` file in the root directory.

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Key for OpenAI models (e.g., gpt-4o) | Yes (if using OpenAI) |
| `ANTHROPIC_API_KEY` | Key for Anthropic models (e.g., Claude 3) | Yes (if using Anthropic) |
| `GEMINI_API_KEY` | Key for Google Gemini models | Yes (if using Gemini) |

### Initialization

Run the initialization command to set up the database and lore files:

```bash
storyteller init
```

This will create a `lore/` directory for your markdown files and a `db/` directory for your story databases.

## Troubleshooting

### "Command not found: storyteller"
- Ensure you installed the package with `pip install .`.
- Check that your Python scripts directory is in your PATH.

### "API Key not found"
- Verify `.env` exists in the directory you are running the command from.
- Ensure variable names are exactly as listed above.

### "Database locked"
- Ensure you don't have multiple instances of Storyteller accessing the same `storyteller.db` simultaneously in write mode.
