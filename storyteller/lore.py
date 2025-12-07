import os
from pathlib import Path
from typing import Dict, List, Optional

try:
    import lancedb
    from sentence_transformers import SentenceTransformer
    import pandas as pd
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False

class LoreManager:
    def __init__(self, lore_dir: str = "lore", use_rag: bool = True):
        self.lore_dir = Path(lore_dir)
        self.lore_cache: Dict[str, str] = {}
        self.use_rag = use_rag
        self.vector_db = None
        self.model = None
        
        self._load_lore()
        self._load_lore()
        if self.use_rag and RAG_AVAILABLE:
            try:
                self._init_rag()
            except Exception as e:
                print(f"Warning: RAG initialization failed ({e}). Falling back to keyword search.")
                self.use_rag = False
        elif self.use_rag and not RAG_AVAILABLE:
            print("Warning: RAG dependencies not found. Falling back to keyword search.")
            self.use_rag = False

    def _init_rag(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.vector_db = lancedb.connect("db/lancedb")
        
        # Create table if not exists
        data = []
        for topic, content in self.lore_cache.items():
            # Chunking could be more sophisticated, but per-file is a start
            data.append({"text": content, "topic": topic, "vector": self.model.encode(content)})
        
        if data:
            try:
                # Ensure the table is created with the correct schema if it doesn't exist
                # Or overwrite if it does, as per the instruction's intent
                self.vector_db.create_table("lore", data=data, mode="overwrite")
            except Exception as e:
                # This catch is for cases where create_table might fail for other reasons
                # The original instruction had a bare 'except Exception', but it's better to log
                print(f"Error creating/overwriting LanceDB table: {e}")


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
        Searches lore using RAG if enabled, otherwise falls back to keyword search.
        """
        if self.use_rag and self.vector_db and self.model:
            try:
                tbl = self.vector_db.open_table("lore")
                query_vector = self.model.encode(query)
                results_df = tbl.search(query_vector).limit(3).to_pandas()
                
                if not results_df.empty:
                    output = []
                    for _, row in results_df.iterrows():
                        output.append(f"--- {row['topic'].upper()} (RAG Match) ---\n{row['text']}\n")
                    return "\n".join(output)
                else:
                    print("RAG search found no relevant results. Falling back to keyword search.")
            except Exception as e:
                print(f"RAG search failed: {e}. Falling back to keyword search.")
        
        # Fallback to keyword search
        keyword_results = []
        query_lower = query.lower()
        
        for topic, content in self.lore_cache.items():
            if query_lower in topic.lower(): # Ensure topic is also lowercased for comparison
                keyword_results.append(f"--- {topic.upper()} ---\n{content}\n")
            elif query_lower in content.lower():
                # Extract a snippet around the match
                # For simplicity, just return the whole file content for now if it matches
                # In a real app, we might want to be more selective
                keyword_results.append(f"--- {topic.upper()} (Relevant Content) ---\n{content}\n")
        
        if not keyword_results:
            return "No specific lore found for this query."
            
        return "\n".join(keyword_results)

    def refresh_lore(self):
        """Reloads lore from disk."""
        self.lore_cache = {}
        self._load_lore()
