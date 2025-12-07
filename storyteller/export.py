import shutil
from pathlib import Path
from typing import List, Dict, Any
from storyteller.db import DatabaseManager

class StoryExporter:
    def __init__(self, storybase: str):
        self.db = DatabaseManager(storybase)

    def export_html(self, story_id: int, output_file: str):
        """Exports story events to an HTML file."""
        story = self.db.get_story(story_id)
        events = self.db.get_recent_events(story_id, limit=1000) # Get all events
        
        html = f"""
        <html>
        <head>
            <title>{story['name']}</title>
            <style>
                body {{ font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                .event {{ margin-bottom: 15px; padding: 10px; border-radius: 5px; }}
                .user {{ background-color: #e3f2fd; text-align: right; }}
                .ai {{ background-color: #f5f5f5; }}
                h1 {{ color: #333; }}
            </style>
        </head>
        <body>
            <h1>{story['name']}</h1>
            <p><em>{story.get('summary', '')}</em></p>
            <hr>
        """
        
        for event in reversed(events):
            css_class = "user" if event['description'].startswith("User:") else "ai"
            content = event['description'].replace("User: ", "").replace("AI: ", "")
            # Simple markdown-ish to HTML conversion (very basic)
            content = content.replace("\n", "<br>")
            html += f'<div class="event {css_class}">{content}</div>\n'
            
        html += "</body></html>"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

class LorePacker:
    def __init__(self, lore_dir: str = "lore"):
        self.lore_dir = Path(lore_dir)

    def pack(self, output_filename: str):
        """Zips the lore directory."""
        shutil.make_archive(output_filename.replace(".zip", ""), 'zip', self.lore_dir)
