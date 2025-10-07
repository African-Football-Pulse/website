import feedparser
from pathlib import Path
import datetime
import re
import unicodedata
import os
import sys

# -----------------------------------------------------
# Configuration
# -----------------------------------------------------
RSS_URL = "https://feeds.buzzsprout.com/2538204.rss"
OUTPUT_DIR = Path("en/pod")
FORCE_REBUILD = os.getenv("FORCE_REBUILD", "false").lower() == "true"

# -----------------------------------------------------
# Helpers
# -----------------------------------------------------
def slugify(value: str) -> str:
    """Convert a string to an SEO-friendly slug."""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    value = re.sub(r"-{2,}", "-", value)
    return value

def load_template() -> str:
    """Try to load template.html from known locations."""
    template_paths = [
        Path("scripts/template.html"),
        Path("en/pod/template.html"),
    ]
    for path in template_paths:
        if path.exists():
            print(f"[fetch] Using template: {path}")
            return path.read_text(encoding="utf-8")
    print("❌ Could not find template.html in expected locations")
    sys.exit(1)

def safe_format(template: str, **kwargs) -> str:
    """Safely format template by escaping stray braces."""
    # Escape all single braces not used as format placeholders
    safe = template.replace("{", "{{").replace("}", "}}")
    # Restore the placeholders we actually want to substitute
    for key in kwargs.keys():
        safe = safe.replace("{{" + key + "}}", "{" + key + "}")
    return safe.format(**kwargs)

# -----------------------------------------------------
# Main
# -----------------------------------------------------
def fetch_and_build():
    print(f"[fetch] Reading RSS feed from {RSS_URL}")
    feed = feedparser.parse(RSS_URL)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[fetch] Found {len(feed.entries)} total entries")

    template = load_template()
    index_items = []
    created, updated = [], []

    for entry in feed.entries:
        title = entry.title
        guid = entry.get("guid", "")
        guid_part = guid.split("-")[-1] if guid else ""
        base_slug = slugify(title)
        slug = f"{base_slug}-{guid_part}" if guid_part else base_slug

        date = datetime.datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
        description = entry.get("summary", "Podcast episode")
        audio_url = entry.enclosures[0].href if entry.enclosures else ""

        file_path = OUTPUT_DIR / f"{slug}.html"
        exists = file_path.exists()

        # Build episode HTML safely
        episode_html = safe_format(
            template,
            title=title,
            description=description,
            audio_url=audio_url,
            date=date,
            slug=slug,
        )

        if not exists or FORCE_REBUILD:
            file_path.write_text(episode_html, encoding="utf-8")
            if exists and FORCE_REBUILD:
                updated.append(file_path.name)
            else:
                created.append(file_path.name)

        index_items.append(f'<li><a href="{slug}.html">{title}</a> ({date})</li>')

    # Build index.html
    index_file = OUTPUT_DIR / "index.html"
    new_list = "<ul>\n" + "\n".join(index_items) + "\n</ul>"

    if index_file.exists():
        index_html = index_file.read_text(encoding="utf-8")
        if "<ul>" in index_html:
            index_html = re.sub(r"<ul>.*</ul>", new_list, index_html, flags=re.DOTALL)
        else:
            index_html += "\n" + new_list
    else:
        index_html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Podcast Episodes</title></head>
<body><h1>Podcast Episodes</h1>{new_list}</body></html>"""
    index_file.write_text(index_html, encoding="utf-8")

    # Summary log
    print(f"[fetch] {len(feed.entries)} entries processed")
    if created:
        print(f"[fetch] Created {len(created)} new episode page(s):")
        for f in created:
            print(f"         + {f}")
    if updated:
        print(f"[fetch] Rebuilt {len(updated)} existing page(s):")
        for f in updated:
            print(f"         * {f}")
    if not created and not updated:
        print("[fetch] No new or rebuilt episodes")
    print("[fetch] Updated index.html")

# -----------------------------------------------------
if __name__ == "__main__":
    fetch_and_build()
