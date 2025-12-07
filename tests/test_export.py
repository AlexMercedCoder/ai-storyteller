import pytest
import os
from storyteller.export import StoryExporter, LorePacker
from storyteller.db import DatabaseManager

def test_export_html(tmp_path):
    # Setup DB
    db_path = tmp_path / "test.db"
    # We need to mock DatabaseManager to use this path or patch it
    # For simplicity, we'll use the actual class but point it to a temp file if possible
    # But DatabaseManager takes a name and puts it in db/
    # So we'll just use a test name
    
    exporter = StoryExporter("test_export")
    db = exporter.db
    story_id = db.create_story("Test Story")
    db.log_event(story_id, "User: Hello")
    db.log_event(story_id, "AI: Hi there")
    
    output_file = tmp_path / "export.html"
    exporter.export_html(story_id, str(output_file))
    
    assert output_file.exists()
    content = output_file.read_text()
    assert "Test Story" in content
    assert "Hello" in content
    assert "Hi there" in content
    
    # Cleanup
    os.remove(f"db/test_export.db")

def test_lore_packer(tmp_path):
    # Create dummy lore
    lore_dir = tmp_path / "lore"
    lore_dir.mkdir()
    (lore_dir / "test.md").write_text("# Test Lore")
    
    packer = LorePacker(str(lore_dir))
    output_zip = tmp_path / "lore_pack"
    packer.pack(str(output_zip))
    
    assert (tmp_path / "lore_pack.zip").exists()
