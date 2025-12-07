# MCP Integration

The Storyteller application acts as both an MCP Client (consuming lore and tools) and an MCP Server (exposing tools to other clients).

## 1. Storyteller as an MCP Server

You can use Storyteller as a server in other MCP clients like Claude Desktop. This allows Claude to access your lore and roll dice for you.

### Configuration
Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "storyteller": {
      "command": "uv",
      "args": ["--directory", "/abs/path/to/storyteller", "run", "storyteller", "serve"]
    }
  }
}
```

### Exposed Tools
- `get_lore(topic)`: Retrieve lore content.
- `search_lore(query)`: Search across all lore.
- `get_story_summary(story_id)`: Get current story state.
- `roll_dice(sides, count)`: Roll dice.

## 2. Storyteller as an MCP Client

Storyteller can connect to *other* MCP servers to gain new powers (e.g., web search, file system access).

### Configuration
Create `mcp_servers.json` in your project root:

```json
{
  "mcpServers": {
    "web-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"]
    }
  }
}
```

### Security Warning
> [!WARNING]
> **Granting Access**: When you add an MCP server, you are giving the AI the ability to use that server's tools. If you add a "filesystem" server, the AI can read/write your files. Only add servers you trust.

### Troubleshooting Connections
- **"Connection Refused"**: Ensure the command in `mcp_servers.json` is executable and in your PATH.
- **"Tool Error"**: Check the logs of the external server if possible.
