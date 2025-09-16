import os
import datetime
from pathlib import Path

BASE_URL = "https://africanfootballpulse.com"
OUTPUT_FILE = Path("seo/sitemap.xml")

def generate():
    today = datetime.date.today().isoformat()

    urls = []

    # Main page
    urls.append(f"""
    <url>
      <loc>{BASE_URL}/</loc>
      <lastmod>{today}</lastmod>
    </url>
    """)

    # English episodes
    pod_dir = Path("en/pod")
    if pod_dir.exists():
        for file in pod_dir.glob("*.html"):
            if file.name == "index.html":
                urls.append(f"""
    <url>
      <loc>{BASE_URL}/en/pod/</loc>
      <lastmod>{today}</lastmod>
    </url>
                """)
            else:
                slug = file.name
                urls.append(f"""
    <url>
      <loc>{BASE_URL}/en/pod/{slug}</loc>
      <lastmod>{today}</lastmod>
    </url>
                """)

    # Arabic episodes (later)
    pod_dir_ar = Path("ar/pod")
    if pod_dir_ar.exists():
        for file in pod_dir_ar.glob("*.html"):
            if file.name == "index.html":
                urls.append(f"""
    <url>
      <loc>{BASE_URL}/ar/pod/</loc>
      <lastmod>{today}</lastmod>
    </url>
                """)
            else:
                slug = file.name
                urls.append(f"""
    <url>
      <loc>{BASE_URL}/ar/pod/{slug}</loc>
      <lastmod>{today}</lastmod>
    </url>
                """)

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join(urls)}
</urlset>
"""
    OUTPUT_FILE.write_text(sitemap.strip(), encoding="utf-8")
    print(f"[sitemap] Generated {OUTPUT_FILE}")

if __name__ == "__main__":
    generate()
