import pytest
from storyteller.lore import LoreManager, RAG_AVAILABLE
import shutil
from pathlib import Path

def test_rag_availability():
    """Verify that RAG dependencies are installed and detected."""
    assert RAG_AVAILABLE is True, "RAG dependencies (lancedb, sentence-transformers) are not installed or detected."

def test_rag_initialization_and_search():
    """Verify that LoreManager initializes RAG and performs vector search."""
    # Clean up any existing db/lancedb to ensure fresh start
    db_path = Path("db/lancedb")
    if db_path.exists():
        shutil.rmtree(db_path)

    # Initialize LoreManager with RAG
    lore = LoreManager(use_rag=True)
    
    # Check if vector_db is initialized
    assert lore.vector_db is not None, "Vector DB was not initialized."
    assert lore.model is not None, "Embedding model was not initialized."
    
    # Perform a search that should yield a result
    # Assuming standard lore files exist (e.g., about 'Elves' or 'Magic')
    # We'll use a query that should match the 'setting.md' or similar
    result = lore.search_lore("kingdom")
    
    # Verify we got a RAG match
    assert "(RAG Match)" in result, f"Expected RAG match, got: {result}"
    
    # Clean up
    if db_path.exists():
        shutil.rmtree(db_path)
