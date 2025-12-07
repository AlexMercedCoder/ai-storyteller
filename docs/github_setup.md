# GitHub Setup & Template Guide

This guide covers how to clone and set up the **AI Storyteller** repository, and how to use it as a template to distribute your own custom RPG worlds.

## Cloning and Setup

Follow these steps to get a local copy of Storyteller running on your machine.

### 1. Clone the Repository
Open your terminal and run:

```bash
git clone https://github.com/AlexMercedCoder/ai-storyteller.git
cd ai-storyteller
```

### 2. Create a Virtual Environment (Recommended)
It's best practice to use a virtual environment to manage dependencies.

```bash
# Create the virtual environment
python -m venv venv

# Activate it (Linux/macOS)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies
Install the package in editable mode:

```bash
pip install -e .
```

### 4. Configure API Keys
Create a `.env` file in the root directory. You can copy the example:

```bash
cp example.env .env
```

Edit `.env` and add your API keys:
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
```

### 5. Initialize
Run the initialization command to create the necessary directories (`db/` and `lore/`):

```bash
storyteller init
```

You are now ready to play! Run `storyteller start` to begin.

---

## Using as a Template

This repository is designed to be a **Template Repository**. This means you can use it as a starting point to create your own pre-packaged RPG worlds (e.g., "Cyberpunk 2099", "High Fantasy Realm").

### 1. Create a New Repo from Template
1.  Go to the [AI Storyteller GitHub page](https://github.com/AlexMercedCoder/ai-storyteller).
2.  Click the **"Use this template"** button.
3.  Select **"Create a new repository"**.
4.  Name your new repository (e.g., `my-rpg-world`).

### 2. Customize Your World
Once you have your own repository, you can customize the lore to fit your setting.

1.  **Clear Default Lore**: Delete the files in `lore/`.
2.  **Add Your Lore**: Create new markdown files in `lore/` describing your world.
    *   `lore/history.md`
    *   `lore/factions.md`
    *   `lore/magic.md`
3.  **Update README**: Update the `README.md` to describe your specific setting.

### 3. Distribute
Now, when users clone *your* repository and run `storyteller init`, they will have your custom lore pre-loaded and ready to play!

This is perfect for:
- **Game Designers**: Distributing a starter kit for your TTRPG.
- **Dungeon Masters**: Sharing your campaign setting with players.
- **Writers**: Letting readers explore your fictional world interactively.
