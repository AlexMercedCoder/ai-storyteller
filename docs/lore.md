# Lore Management

Lore is the heart of your Storyteller experience. It provides the AI with the knowledge it needs to build a consistent world.

## Directory Structure

Lore is stored in the `lore/` directory. You can organize files however you like, but flat lists of markdown files work best for simple keyword matching.

```
lore/
  ├── ruleset.md
  ├── setting.md
  ├── factions.md
  └── characters/
       ├── king_alric.md
       └── lady_elara.md
```

## Writing Effective Lore

### Format
Use standard Markdown headers (`#`, `##`) to structure your documents.

### Example: `factions.md`

```markdown
# Factions of Aethelgard

## The Silver Hand
A knightly order dedicated to purging the undead.
- **Leader**: Grandmaster Thorne
- **Base**: Silver Keep
- **Motto**: "Light in the Darkness"

## The Red Cabal
A secret society of blood mages.
- **Goal**: To resurrect the Dark Lord.
```

## How Retrieval Works

When you type a message, Storyteller scans your input for keywords that match:
1.  **Filenames**: `king_alric` matches `lore/characters/king_alric.md`.
2.  **Content**: If you mention "Silver Hand", the system finds it in `factions.md`.

*Tip: Unique names work best for retrieval.*
