import pytest
import os
from storyteller.db import DatabaseManager

@pytest.fixture
def db():
    # Use a custom storybase name for testing
    storybase = "test_db"
    db = DatabaseManager(storybase)
    yield db
    # Cleanup
    import shutil
    if db.db_dir.exists():
        shutil.rmtree(db.db_dir)

def test_create_story(db):
    story_id = db.create_story("Test Story", "Summary")
    assert story_id is not None
    story = db.get_story(story_id)
    assert story["name"] == "Test Story"

def test_update_story_summary(db):
    story_id = db.create_story("Test Story")
    db.update_story_summary(story_id, "New Summary")
    story = db.get_story(story_id)
    assert story["summary"] == "New Summary"

def test_add_character(db):
    story_id = db.create_story("Test Story")
    char_id = db.add_character(story_id, "Hero", {"class": "Warrior"})
    assert char_id is not None
    chars = db.get_characters(story_id)
    assert len(chars) == 1
    assert chars[0]["name"] == "Hero"

def test_log_event(db):
    story_id = db.create_story("Test Story")
    db.log_event(story_id, "Something happened")
    events = db.get_recent_events(story_id)
    assert len(events) == 1
    assert events[0]["description"] == "Something happened"
