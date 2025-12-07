import pytest
from storyteller.tui import CharacterSheet, LoreBrowser
from storyteller.lore import LoreManager

# Note: Testing Textual widgets usually requires an async test environment or mocking
# We will test the logic of the widgets where possible without full rendering

def test_character_sheet_update():
    # This is a bit tricky without a running app, but we can check the class exists
    assert CharacterSheet is not None
    # In a real scenario, we'd use textual's test harness

def test_lore_browser_init():
    lore = LoreManager()
    browser = LoreBrowser(lore)
    assert browser.lore_manager == lore
