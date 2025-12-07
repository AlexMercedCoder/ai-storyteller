import random
from typing import List, Dict, Any, Optional

class LootTable:
    def __init__(self, items: Dict[str, float]):
        """
        Initialize with a dictionary of item names and their weights.
        Example: {"Gold Coin": 50.0, "Potion": 20.0, "Sword": 5.0}
        """
        self.items = items

    def roll(self) -> str:
        """Selects an item based on weights."""
        choices = list(self.items.keys())
        weights = list(self.items.values())
        return random.choices(choices, weights=weights, k=1)[0]

class DungeonGenerator:
    def __init__(self, num_rooms: int = 5):
        self.num_rooms = num_rooms

    def generate(self) -> Dict[str, Any]:
        """Generates a simple linear dungeon."""
        dungeon = {
            "name": f"Dungeon of {random.choice(['Doom', 'Shadows', 'Echoes', 'Despair'])}",
            "rooms": []
        }
        
        room_types = ["Entrance", "Hallway", "Chamber", "Armory", "Library", "Crypt"]
        encounters = ["Goblin", "Skeleton", "Trap", "Puzzle", "Treasure Chest", "Empty"]
        
        for i in range(self.num_rooms):
            room = {
                "id": i + 1,
                "type": "Boss Room" if i == self.num_rooms - 1 else random.choice(room_types),
                "encounter": "Boss" if i == self.num_rooms - 1 else random.choice(encounters),
                "description": f"A dark {random.choice(['damp', 'dusty', 'cold'])} room."
            }
            dungeon["rooms"].append(room)
            
        return dungeon
