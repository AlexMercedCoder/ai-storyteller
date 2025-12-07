# Database Guide

Storyteller uses a SQLite database to track the state of your game world. This guide explains the schema and how to leverage it for better storytelling.

## Overview

- **Location**: Databases are stored in the `db/` directory.
- **Default**: `db/default.db`
- **Custom**: You can create separate databases for different campaigns using the `--storybase` flag.

## Schema

### 1. Stories Table (`stories`)
Tracks the high-level state of a campaign.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Unique ID for the story. |
| `name` | TEXT | Name of the campaign. |
| `summary` | TEXT | A running summary of the plot so far. The AI updates this periodically. |

### 2. Characters Table (`characters`)
Stores NPCs and Player Characters.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Unique ID. |
| `story_id` | INTEGER | Links to the story. |
| `name` | TEXT | Character name. |
| `data` | JSON | Flexible field for stats, inventory, bio, etc. |

**Usage Tip**: The `data` JSON field is extremely powerful. You can store arbitrary attributes like:
```json
{
  "class": "Wizard",
  "level": 5,
  "alignment": "Chaotic Good",
  "inventory": ["Staff", "Robes"]
}
```

### 3. Events Table (`events`)
A log of everything that happens in the chat.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Unique ID. |
| `story_id` | INTEGER | Links to the story. |
| `description` | TEXT | The content of the event (User input or AI response). |
| `timestamp` | TIMESTAMP | When it happened. |

### 4. Inventory Table (`inventory`)
Tracks items in the world.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Unique ID. |
| `story_id` | INTEGER | Links to the story. |
| `owner_id` | INTEGER | Links to a character (nullable if on ground). |
| `item_name` | TEXT | Name of the item. |
| `details` | JSON | Stats, description, etc. |

## Best Practices

### Multiple Campaigns
Use `--storybase` to keep your campaigns separate.
```bash
storyteller start --storybase my_scifi_campaign
storyteller start --storybase my_fantasy_campaign
```

### Direct Database Access
Since it's just SQLite, you can use any SQLite viewer (like `sqlite3` CLI or DB Browser for SQLite) to inspect or manually edit the database. This is useful for:
- Fixing a mistake in the story summary.
- Manually adding a complex item to a character.
- Backing up your save file (just copy the `.db` file).
