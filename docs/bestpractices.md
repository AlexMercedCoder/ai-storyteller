# Best Practices

To get the most out of Storyteller, follow these guidelines for lore management, prompting, and configuration.

## Lore Management

The quality of the AI's narration depends heavily on the quality of your lore files.

### 1. Keep it Modular
Don't put everything in one huge file. Break it down:
- `factions.md`
- `history.md`
- `magic_system.md`

### 2. Use Keywords
The system searches for keywords in your input to find relevant lore. Ensure your lore files contain the specific terms you are likely to use in chat.
- *Bad*: "The big bad guy lives in the north."
- *Good*: "The **Lich King** resides in the **Frozen Citadel**."

### 3. Concise Descriptions
LLMs have context limits (though they are large now). Concise, punchy descriptions are better than rambling prose. Bullet points work great for lists of items or NPCs.

## Effective Prompting

### 1. Be Descriptive
The more detail you give the AI about your actions, the better it can narrate the result.
- *Weak*: "I hit him."
- *Strong*: "I feint to the left and thrust my spear towards the orc's exposed flank."

### 2. Set the Tone
If you want a horror vibe, use horror language in your inputs. The AI will pick up on your style and mirror it.

### 3. Use OOC for Correction
If the AI makes a mistake (e.g., forgets an NPC is dead), gently correct it using OOC (Out of Character) markers.
> (OOC: Remember, the innkeeper died in the fire yesterday.)

## External Tools (MCP)

### 1. Use Specialized Servers
Connect Storyteller to specialized MCP servers for better results:
- **Web Search**: For looking up real-world mythology or rules.
- **Code Execution**: For complex dice probability calculations or generating random tables programmatically.

### 2. Security
Only connect to MCP servers you trust. Storyteller gives them access to the conversation context, and they can execute code on your machine if designed to do so.

## Database
- **Backups**: Your `storyteller.db` contains all your campaigns. Back it up regularly!
- **Resuming**: Always note down your `story_id` if you plan to run multiple parallel campaigns.
