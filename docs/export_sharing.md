# Export & Sharing

Share your stories and campaigns with friends using the built-in export tools.

## Exporting Stories

You can export your entire chat history to a formatted HTML file.

```bash
storyteller export --story-id 1 --output my_story.html
```

The HTML file includes:
- Story Title and Summary
- All user and AI messages, color-coded
- Basic styling for readability

## Packing Lore

To share your custom world (lore), you can pack the `lore/` directory into a zip file.

```bash
storyteller pack-lore --output my_campaign_lore.zip
```

You can then send this zip file to other users. They just need to unzip it into their `lore/` directory to play in your world.
