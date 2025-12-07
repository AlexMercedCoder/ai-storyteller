# Chat Interface Guide

The Chat Interface is the core of the Storyteller application, acting as your portal to the game world. This guide details how the chat works, how context is managed, and how to interact effectively with the AI Dungeon Master.

## How it Works

When you send a message in the chat, several things happen in the background before you get a response:

1.  **Lore Retrieval**: The system scans your input for keywords matching your local lore files (in the `lore/` directory). If matches are found, that content is pulled into the context.
2.  **State Check**: The system retrieves the current "Story Summary" and the last few events from the database to understand what just happened.
3.  **Tool Discovery**: If you have external MCP servers configured, the system checks if any tools are available and presents them to the AI.
4.  **AI Processing**: All this information (User Input + Lore + Story State + Recent Events + Tools) is sent to the AI provider (OpenAI, Anthropic, or Gemini).
5.  **Response & Logging**: The AI generates a response, which is displayed to you and logged in the database as an event.

## Context Window

The "Context Window" is the amount of information the AI can "remember" at once. Storyteller manages this by:

- **Summarization**: As the story progresses, the AI updates a running "Story Summary". This ensures that even if specific details of early events drop out of the immediate logs, the core narrative remains.
- **Selective Lore**: Only lore relevant to your *current* input is injected. This keeps the context focused and prevents the AI from being overwhelmed by irrelevant world-building details.

## Interaction Patterns

### Roleplay
You can speak directly as your character.
> **You**: I draw my sword and shout, "For the King!" then charge at the goblin.

### Out of Character (OOC)
You can ask the DM questions or clarify rules.
> **You**: (OOC) How much health do I have left? And does this goblin look injured?

### Directing the Story
You can give high-level direction to the narrative.
> **You**: I want to skip the travel and arrive at the city gates by nightfall.

## Event Logging

Every interaction is saved to the SQLite database.
- **User Actions**: What you typed.
- **AI Responses**: What the DM said.
- **System Events**: Significant state changes (like finding an item) can be logged programmatically if tools are used.

This persistence allows you to close the application and resume exactly where you left off using the `--story-id` flag.
