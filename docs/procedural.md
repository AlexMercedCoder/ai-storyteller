# Procedural Content Tools

Storyteller includes tools to procedurally generate content for your campaigns, helping DMs quickly create dungeons and loot.

## Dungeon Generator

Generate a random linear dungeon with rooms, encounters, and descriptions.

```bash
storyteller dm-assist dungeon --rooms 5
```

**Output Example:**
```
Dungeon of Shadows
Room 1: Entrance
  Encounter: Empty
  Description: A dark cold room.

Room 2: Hallway
  Encounter: Goblin
  Description: A dark dusty room.
...
```

## Loot Generator

Generate random loot based on weighted tables.

```bash
storyteller dm-assist loot --table-type magic
```

**Options:**
- `generic`: Common items (Gold, Rope, Torches).
- `magic`: Potions, Scrolls, Magic Items.
- `treasure`: Valuables (Gems, Crowns).
