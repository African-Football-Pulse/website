import feedparser
from pathlib import Path
import datetime
import re
import unicodedata

# Buzzsprout RSS URL för Swahili-podden
RSS_URL = "https://feeds.buzzsprout.com/2538230.rss"
OUTPUT_DIR = Path("sw/pod")

def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    value = re.sub(r"-{2,}", "-", value)
    return value

TEMPLATE = """<!DOCTYPE html>
<html lang="sw">
<head>
  <meta charset="UTF-8">
  <title>{title} | African Football Pulse</title>
  <meta name="description" content="{description}">
  <meta name="author" content="African Football Pulse">
  <meta name="keywords" content="soka la Afrika, Premier League, podcast, {title}">

  <!-- Schema.org PodcastEpisode -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "PodcastEpisode",
    "name": "{title}",
    "url": "https://africanfootballpulse.com/sw/pod/{slug}.html",
    "datePublished": "{date}",
    "description": "{description}",
    "inLanguage": "sw",
    "partOfSeries": {{
      "@type": "PodcastSeries",
      "name": "African Football Pulse",
      "url": "https://africanfootballpulse.com/sw/pod/"
    }},
    "associatedMedia": {{
      "@type": "MediaObject",
      "contentUrl": "{audio_url}",
      "encodingFormat": "audio/mpeg"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "African Football Pulse",
      "url": "https://africanfootballpulse.com"
    }}
  }}
  </script>
</head>
<body>
  <h1>{title}</h1>
  <p><em>Imechapishwa {date}</em></p>

  <audio controls>
    <source src="{audio_url}" type="audio/mpeg">
  </audio>

  <div>
    <p>{description}</p>
  </div>

  <p><a href="index.html">← Rudi kwenye Vipindi</a></p>
</body>
</html>
"""

def fetch_and_build():
    feed = feedparser.parse(RSS_URL)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    index_items = []
    for entry in feed.entries:
        title = entry.title
        guid = entry.get("guid", "")
        guid_part = guid.split("-")[-1] if guid else ""
        slug = f"{slugify(title)}-{guid_part}" if guid_part else slugify(title)

        date = datetime.datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
        description = entry.get("summary", "Kipindi cha podcast")
        audio_url = entry.enclosures[0].href if entry.enclosures else ""

        episode_html = TEMPLATE.format(
            title=title,
            description=description,
            audio_url=audio_url,
            date=date,
            slug=slug
        )
        (OUTPUT_DIR / f"{slug}.html").write_text(episode_html, encoding="utf-8")
        index_items.append(f'<li><a href="{slug}.html">{title}</a> ({date})</li>')

    # Update index.html
    index_file = OUTPUT_DIR / "index.html"
    if index_file.exists():
        index_html = index_file.read_text(encoding="utf-8")
        new_list = "<ul>\n" + "\n".join(index_items) + "\n</ul>"
        index_html = re.sub(r"<ul>.*</ul>", new_list, index_html, flags=re.DOTALL)
        index_file.write_text(index_html, encoding="utf-8")

if __name__ == "__main__":
    fetch_and_build()
