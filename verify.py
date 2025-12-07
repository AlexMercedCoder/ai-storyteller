import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from storyteller.db import DatabaseManager
from storyteller.lore import LoreManager

def test_database():
    print("Testing DatabaseManager...")
    db = DatabaseManager("test_storyteller.db")
    
    # Create story
    story_id = db.create_story("Test Story", "A test summary")
    assert story_id is not None
    print(f"  Created story with ID: {story_id}")
    
    # Get story
    story = db.get_story(story_id)
    assert story["name"] == "Test Story"
    assert story["summary"] == "A test summary"
    print("  Retrieved story successfully")
    
    # Update summary
    db.update_story_summary(story_id, "Updated summary")
    story = db.get_story(story_id)
    assert story["summary"] == "Updated summary"
    print("  Updated story summary successfully")
    
    # Clean up
    os.remove("test_storyteller.db")
    print("Database tests passed!")

def test_lore():
    print("\nTesting LoreManager...")
    # Create a dummy lore file
    Path("lore").mkdir(exist_ok=True)
    with open("lore/test_topic.md", "w") as f:
        f.write("This is a test lore file about dragons.")
        
    lore = LoreManager()
    
    # Get lore
    content = lore.get_lore("test_topic")
    assert "dragons" in content
    print("  Retrieved lore successfully")
    
    # Search lore
    results = lore.search_lore("dragons")
    assert "TEST_TOPIC" in results
    print("  Searched lore successfully")
    
    # Clean up
    os.remove("lore/test_topic.md")
    print("Lore tests passed!")

if __name__ == "__main__":
    try:
        test_database()
        test_lore()
        print("\nAll verification tests passed!")
    except Exception as e:
        print(f"\nVerification failed: {e}")
        sys.exit(1)
