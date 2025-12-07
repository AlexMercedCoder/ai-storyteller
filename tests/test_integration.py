import pytest
import os
from storyteller.ai import AIGateway
from storyteller.db import DatabaseManager
from storyteller.lore import LoreManager

# Skip if no API key present
@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No OpenAI API key found")
def test_ai_gateway_openai():
    ai = AIGateway()
    response = ai.generate_response("Say hello", provider="openai", model="gpt-4o")
    assert len(response) > 0
    print(f"OpenAI Response: {response}")

def test_full_flow():
    # Setup
    db = DatabaseManager("test_integration")
    lore = LoreManager() # Uses default lore
    ai = AIGateway()
    
    story_id = db.create_story("Integration Test Story")
    
    # Simulate user input
    user_input = "I look around the tavern."
    
    # Context
    relevant_lore = lore.search_lore("tavern") # Might be empty if no tavern lore
    recent_events = db.get_recent_events(story_id)
    
    system_instruction = f"You are a DM. User says: {user_input}. Lore: {relevant_lore}"
    
    # Generate
    if os.getenv("OPENAI_API_KEY"):
        response = ai.generate_response(user_input, system_instruction, provider="openai")
        assert len(response) > 0
        
        # Log
        db.log_event(story_id, f"User: {user_input}")
        db.log_event(story_id, f"AI: {response}")
        
        events = db.get_recent_events(story_id)
        assert len(events) == 2
    
    # Cleanup
    import shutil
    if db.db_dir.exists():
        shutil.rmtree(db.db_dir)
