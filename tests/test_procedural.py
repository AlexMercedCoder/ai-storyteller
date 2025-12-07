import pytest
from storyteller.procedural import DungeonGenerator, LootTable

def test_loot_table():
    items = {"A": 100, "B": 0}
    table = LootTable(items)
    assert table.roll() == "A"
    
    items = {"A": 0, "B": 100}
    table = LootTable(items)
    assert table.roll() == "B"

def test_dungeon_generator():
    gen = DungeonGenerator(num_rooms=3)
    dungeon = gen.generate()
    
    assert "name" in dungeon
    assert len(dungeon["rooms"]) == 3
    assert dungeon["rooms"][-1]["type"] == "Boss Room"
    assert dungeon["rooms"][-1]["encounter"] == "Boss"
