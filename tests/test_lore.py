import pytest
import os
from pathlib import Path
from storyteller.lore import LoreManager

@pytest.fixture
def lore_dir():
    path = Path("test_lore")
    path.mkdir(exist_ok=True)
    (path / "dragons.md").write_text("Dragons breathe fire.")
    yield str(path)
    import shutil
    shutil.rmtree(path)

def test_get_lore(lore_dir):
    lore = LoreManager(lore_dir)
    content = lore.get_lore("dragons")
    assert "fire" in content

def test_search_lore(lore_dir):
    lore = LoreManager(lore_dir)
    results = lore.search_lore("fire")
    assert "DRAGONS" in results
