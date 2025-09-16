import feedparser
from pathlib import Path
import datetime

# Buzzsprout RSS URL (byt ut mot din)
RSS_URL = "https://feeds.buzzsprout.com/XXXX.rss"
OUTPUT_DIR = Path("en/pod")

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <meta name="description" content="{description}">
</head>
<body>
  <h1>{title}</h1>
  <p><em>Published {date}</em></p>
  <audio controls>
    <source src="{audio_url}" type="audio/mpeg">
  </audio>
  <div>
    <p>{description}</p>
  </div>
  <p><a href="../index.html">← Back to Episodes</a></p>
</body>
</html>
"""

def fetch_and_build():
    feed = feedparser.parse(RSS_URL)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    index_items = []

    for entry in feed.entries:
        title = entry.title
        slug = title.lower().replace(" ", "-")
        date = datetime.datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
        description = entry.summary
        audio_url = entry.enclosures[0].href if entry.enclosures else ""

        # Create episode HTML
        episode_html = TEMPLATE.format(
            title=title,
            description=description,
            audio_url=audio_url,
            date=date
        )
        file_path = OUTPUT_DIR / f"{slug}.html"
        file_path.write_text(episode_html, encoding="utf-8")

        # Add to index
        index_items.append(f'<li><a href="{slug}.html">{title}</a> ({date})</li>')

    # Update index.html
    index_html = (OUTPUT_DIR / "index.html").read_text(encoding="utf-8")
    new_list = "<ul>\n" + "\n".join(index_items) + "\n</ul>"
    index_html = index_html.replace("<ul>\n    <!-- Script kommer fylla på med länkar -->\n  </ul>", new_list)
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

if __name__ == "__main__":
    fetch_and_build()
