import os
from pathlib import Path
from typing import Dict, List, Optional

class LoreManager:
    def __init__(self, lore_dir: str = "lore"):
        self.lore_dir = Path(lore_dir)
        self.lore_cache: Dict[str, str] = {}
        self._load_lore()

    def _load_lore(self):
        """Loads all markdown files from the lore directory into memory."""
        if not self.lore_dir.exists():
            return

        for file_path in self.lore_dir.glob("*.md"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.lore_cache[file_path.stem] = f.read()
            except Exception as e:
                print(f"Error loading lore file {file_path}: {e}")

    def get_lore(self, topic: str) -> Optional[str]:
        """Retrieves the content of a specific lore file."""
        return self.lore_cache.get(topic.lower())

    def get_all_lore_topics(self) -> List[str]:
        """Returns a list of available lore topics."""
        return list(self.lore_cache.keys())

    def search_lore(self, query: str) -> str:
        """
        Simple keyword search across all lore files.
        Returns a concatenated string of relevant snippets.
        """
        results = []
        query = query.lower()
        
        for topic, content in self.lore_cache.items():
            if query in topic:
                results.append(f"--- {topic.upper()} ---\n{content}\n")
            elif query in content.lower():
                # Extract a snippet around the match
                # For simplicity, just return the whole file content for now if it matches
                # In a real app, we might want to be more selective
                results.append(f"--- {topic.upper()} (Relevant Content) ---\n{content}\n")
        
        if not results:
            return "No specific lore found for this query."
            
        return "\n".join(results)

    def refresh_lore(self):
        """Reloads lore from disk."""
        self.lore_cache = {}
        self._load_lore()
