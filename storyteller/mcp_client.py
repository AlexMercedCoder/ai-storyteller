import json
import os
import asyncio
from typing import Dict, List, Any, Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClientManager:
    def __init__(self, config_path: str = "mcp_servers.json"):
        self.config_path = config_path
        self.servers: Dict[str, Any] = {}
        self.sessions: Dict[str, ClientSession] = {}
        self.exit_stack = AsyncExitStack()
        self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    data = json.load(f)
                    self.servers = data.get("mcpServers", {})
            except Exception as e:
                print(f"Error loading MCP config: {e}")

    async def connect_all(self):
        """Connects to all configured MCP servers."""
        for name, config in self.servers.items():
            try:
                command = config.get("command")
                args = config.get("args", [])
                env = config.get("env", None)
                
                if not command:
                    continue

                server_params = StdioServerParameters(
                    command=command,
                    args=args,
                    env={**os.environ, **(env or {})}
                )
                
                # Create the client connection
                # We need to keep the transport and session alive
                # Using AsyncExitStack to manage context managers
                
                stdio_transport = await self.exit_stack.enter_async_context(
                    stdio_client(server_params)
                )
                read, write = stdio_transport
                
                session = await self.exit_stack.enter_async_context(
                    ClientSession(read, write)
                )
                
                await session.initialize()
                self.sessions[name] = session
                print(f"Connected to MCP server: {name}")
                
            except Exception as e:
                print(f"Failed to connect to MCP server {name}: {e}")

    async def get_all_tools(self) -> List[Dict[str, Any]]:
        """Retrieves tools from all connected servers."""
        all_tools = []
        for name, session in self.sessions.items():
            try:
                result = await session.list_tools()
                for tool in result.tools:
                    # Add server name to tool to disambiguate if needed, 
                    # or just pass through. For now, we'll just return the tool definition
                    # and handle execution routing later.
                    tool_dict = tool.model_dump()
                    tool_dict["server_name"] = name
                    all_tools.append(tool_dict)
            except Exception as e:
                print(f"Error listing tools for {name}: {e}")
        return all_tools

    async def call_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Calls a tool on a specific server."""
        session = self.sessions.get(server_name)
        if not session:
            return f"Error: Server {server_name} not connected."
        
        try:
            result = await session.call_tool(tool_name, arguments)
            return result
        except Exception as e:
            return f"Error calling tool {tool_name} on {server_name}: {e}"

    async def cleanup(self):
        """Closes all connections."""
        await self.exit_stack.aclose()
