import feedparser
from pathlib import Path
import datetime
import re
import unicodedata

RSS_URL = "https://feeds.buzzsprout.com/2538204.rss"
OUTPUT_DIR = Path("en/pod")

def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    value = re.sub(r"-{2,}", "-", value)
    return value

def fetch_and_build():
    print(f"[fetch] Reading RSS feed from {RSS_URL}")
    feed = feedparser.parse(RSS_URL)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[fetch] Found {len(feed.entries)} total entries")

    index_items = []
    new_files = []

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
        is_new = not file_path.exists()

        episode_html = TEMPLATE.format(
            title=title,
            description=description,
            audio_url=audio_url,
            date=date,
            slug=slug
        )
        file_path.write_text(episode_html, encoding="utf-8")

        index_items.append(f'<li><a href="{slug}.html">{title}</a> ({date})</li>')

        if is_new:
            new_files.append(file_path.name)

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

    # --- Summary log ---
    print(f"[fetch] {len(feed.entries)} entries processed")
    if new_files:
        print(f"[fetch] Created {len(new_files)} new episode pages:")
        for f in new_files:
            print(f"         - {f}")
    else:
        print("[fetch] No new episodes found (all already up to date)")
    print("[fetch] Updated index.html")

if __name__ == "__main__":
    TEMPLATE_PATHS = [
    Path("scripts/template.html"),
    Path("en/pod/template.html")
    ]
    for path in TEMPLATE_PATHS:
        if path.exists():
            TEMPLATE = path.read_text(encoding="utf-8")
            break
    else:
        raise FileNotFoundError("❌ Could not find template.html in expected locations")


    fetch_and_build()
