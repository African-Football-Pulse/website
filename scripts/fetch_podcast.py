import feedparser
from pathlib import Path
import datetime
import re
import unicodedata

# Buzzsprout RSS URL
RSS_URL = "https://feeds.buzzsprout.com/2538204.rss"
OUTPUT_DIR = Path("en/pod")

def slugify(value: str) -> str:
    """Convert string to SEO-friendly slug."""
    # Normalisera unicode (é -> e)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    # Lowercase
    value = value.lower()
    # Byt ut allt som inte är a-z0-9 mot -
    value = re.sub(r"[^a-z0-9]+", "-", value)
    # Trimma bindestreck
    value = value.strip("-")
    # Byt ut flera - i rad mot ett
    value = re.sub(r"-{2,}", "-", value)
    return value

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title} | African Football Pulse</title>

  <!-- Basic SEO -->
  <meta name="description" content="{description}">
  <meta name="keywords" content="African football, Premier League, podcast, {title}">
  <meta name="author" content="African Football Pulse">

  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title} | African Football Pulse">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="https://africanfootballpulse.com/en/pod/{slug}.html">
  <meta property="og:site_name" content="African Football Pulse">
  <meta property="og:image" content="https://africanfootballpulse.com/assets/cover.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title} | African Football Pulse">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="https://africanfootballpulse.com/assets/cover.jpg">

  <!-- Schema.org PodcastEpisode -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "PodcastEpisode",
    "name": "{title}",
    "url": "https://africanfootballpulse.com/en/pod/{slug}.html",
    "datePublished": "{date}",
    "description": "{description}",
    "partOfSeries": {{
      "@type": "PodcastSeries",
      "name": "African Football Pulse",
      "url": "https://africanfootballpulse.com/en/pod/"
    }},
    "associatedMedia": {{
      "@type": "MediaObject",
      "contentUrl": "{audio_url}",
      "encodingFormat": "audio/mpeg"
    }},
    "inLanguage": "en",
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
        guid = entry.get("guid", "")
        guid_part = guid.split("-")[-1] if guid else ""
        base_slug = slugify(title)

        # Bygg slug: title + GUID (om finns)
        slug = f"{base_slug}-{guid_part}" if guid_part else base_slug

        date = datetime.datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
        description = entry.get("summary", "Podcast episode")
        audio_url = entry.enclosures[0].href if entry.enclosures else ""

        # Skapa episod HTML
        episode_html = TEMPLATE.format(
            title=title,
            description=description,
            audio_url=audio_url,
            date=date,
            slug=slug
        )
        file_path = OUTPUT_DIR / f"{slug}.html"
        file_path.write_text(episode_html, encoding="utf-8")

        # Lägg till i index
        index_items.append(f'<li><a href="{slug}.html">{title}</a> ({date})</li>')

    # Uppdatera index.html
    index_file = OUTPUT_DIR / "index.html"
    new_list = "<ul>\n" + "\n".join(index_items) + "\n</ul>"

    if index_file.exists():
        index_html = index_file.read_text(encoding="utf-8")
        if "<ul>" in index_html:
            # Byt ut befintlig lista
            index_html = re.sub(r"<ul>.*</ul>", new_list, index_html, flags=re.DOTALL)
        else:
            # Lägg till längst ner
            index_html += "\n" + new_list
        index_file.write_text(index_html, encoding="utf-8")
    else:
        # Skapa fallback index
        fallback = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>African Football Pulse | Episodes</title>
  <meta name="description" content="Podcast episodes about African football and the Premier League.">
</head>
<body>
  <h1>Podcast Episodes</h1>
  {new_list}
</body>
</html>
"""
        index_file.write_text(fallback, encoding="utf-8")

if __name__ == "__main__":
    fetch_and_build()
