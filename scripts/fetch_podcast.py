import feedparser
from pathlib import Path
import datetime

# Buzzsprout RSS URL (byt ut mot din feed)
RSS_URL = "https://feeds.buzzsprout.com/2538204.rss"
OUTPUT_DIR = Path("en/pod")

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
        slug = title.lower().replace(" ", "-")
        date = datetime.datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
        description = entry.summary if hasattr(entry, "summary") else "Podcast episode"
        audio_url = entry.enclosures[0].href if entry.enclosures else ""

        # Build episode HTML
        episode_html = TEMPLATE.format(
            title=title,
            description=description,
            audio_url=audio_url,
            date=date,
            slug=slug
        )
        file_path = OUTPUT_DIR / f"{slug}.html"
        file_path.write_text(episode_html, encoding="utf-8")

        # Add link to index
        index_items.append(f'<li><a href="{slug}.html">{title}</a> ({date})</li>')

    # Update index.html with new list
    index_file = OUTPUT_DIR / "index.html"
    if index_file.exists():
        index_html = index_file.read_text(encoding="utf-8")
        new_list = "<ul>\n" + "\n".join(index_items) + "\n</ul>"
        index_html = index_html.replace(
            "<ul>\n    <!-- Script kommer fylla på med länkar -->\n  </ul>",
            new_list
        )
        index_file.write_text(index_html, encoding="utf-8")
    else:
        # Create fallback index if missing
        fallback = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>African Football Pulse | Episodes</title>
  <meta name="description" content="Podcast episodes about African football and the Premier League.">
</head>
<body>
  <h1>Podcast Episodes</h1>
  <ul>
    {"".join(index_items)}
  </ul>
</body>
</html>
"""
        index_file.write_text(fallback, encoding="utf-8")

if __name__ == "__main__":
    fetch_and_build()
