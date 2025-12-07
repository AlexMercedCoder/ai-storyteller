import importlib.util
import os
from pathlib import Path
from typing import List, Dict, Any, Callable

class PluginManager:
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugins: List[Dict[str, Any]] = []

    def load_plugins(self) -> List[Dict[str, Any]]:
        """Loads plugins from the plugins directory."""
        if not self.plugin_dir.exists():
            return []

        for file_path in self.plugin_dir.glob("*.py"):
            if file_path.name == "__init__.py":
                continue
            
            try:
                spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Look for a 'register_tools' function
                    if hasattr(module, "register_tools"):
                        tools = module.register_tools()
                        for tool in tools:
                            # Add metadata to identify as plugin tool
                            tool["server_name"] = "plugin" 
                            self.plugins.append(tool)
                            print(f"Loaded plugin tool: {tool['name']} from {file_path.name}")
            except Exception as e:
                print(f"Error loading plugin {file_path}: {e}")
        
        return self.plugins
