# AI Storyteller

## Purpose

To be a tool to either act as a dungeon master or assist a dungeon master in running a roleplaying game.

## How it works

This is an AI agent using a Chat interface that can act as an MCP client or an MCP server that can be plugged into other MCP clients.

- It will use a local "lore" folder to look through markdown for game rules, lore and other information to help with storytelling.

- It will instantiate a local SQLite database to pursure things like characters, events, inventory, etc. (probably use a JSON field in a charachter to have flexible tracking of charachters with different rulesets)

- In the sql lite database it should also track the story state with a "storyname" and "storysummary" which is a summary of the story so far that is updated as the story progresses so the story can be resumed at a later time.

- Please populate the lore folder with a unique and simple:

    - ruleset.md
    - setting.md
    - races.md
    - classes.md
    - locations.md
    - enemies.md
    - items.md

This way people can try this out of the box

- For the AI Agent, it should be able to use OpenAI, Gemini and Anthropic, the API keys should be stored in a .env file or exist in the environment and the provider and model should be passed in as arguments and all should be exaustively detailed in a docmentation folder that has a dedicated markdown for each feature that is indexed in the readme.md

- make sure this using python or javascript, whatever you choose, make sure it is using the latest version of the language and has a dedicated documentation folder that has a dedicated markdown for each feature that is indexed in the readme.md