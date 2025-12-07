# Plugin System

Extend Storyteller with custom Python scripts.

## How to Create a Plugin

1.  Create a `plugins/` directory in your project root.
2.  Add a Python file (e.g., `my_plugin.py`).
3.  Define a `register_tools()` function that returns a list of tool definitions.

### Example Plugin

```python
# plugins/math_plugin.py

def add(a: int, b: int) -> int:
    return a + b

def register_tools():
    return [
        {
            "name": "add_numbers",
            "description": "Adds two numbers.",
            "function": add,
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }
        }
    ]
```

## Loading Plugins

Plugins are automatically loaded when you start `storyteller start` or `storyteller serve`. The AI will be aware of your new tools and use them when appropriate.
