#!/usr/bin/env python3
"""
Fetches publications from Google Scholar and regenerates _pages/publications.md.
Splits into First Author vs Contributed To based on author order.

Usage:
    pip install requests beautifulsoup4
    python3 scripts/sync_publications.py
"""

import time
import sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup

SCHOLAR_USER = "Zc7DhZMAAAAJ"
AUTHOR_NAME = "Earl Ranario"
BASE_URL = "https://scholar.google.com"
OUTPUT_FILE = Path(__file__).parent.parent / "_pages" / "publications.md"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def fetch_profile():
    url = f"{BASE_URL}/citations?user={SCHOLAR_USER}&hl=en&sortby=pubdate&pagesize=100"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.text


def parse_papers(html):
    soup = BeautifulSoup(html, "html.parser")
    papers = []
    for row in soup.select("tr.gsc_a_tr"):
        title_el = row.select_one("a.gsc_a_at")
        if not title_el:
            continue
        title = title_el.get_text(strip=True)
        href = title_el.get("href", "")
        url = (BASE_URL + href) if href.startswith("/") else href
        papers.append({"title": title, "url": url})
    return papers


def get_first_author(citation_url):
    time.sleep(1.5)  # stay polite to Scholar
    try:
        resp = requests.get(citation_url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  Warning: could not fetch {citation_url}: {e}", file=sys.stderr)
        return None

    soup = BeautifulSoup(resp.text, "html.parser")
    for row in soup.select("div.gs_scl"):
        field = row.select_one("div.gsc_oci_field")
        value = row.select_one("div.gsc_oci_value")
        if field and value and "Authors" in field.get_text():
            authors_raw = value.get_text(strip=True)
            first = authors_raw.split(",")[0].strip().lower()
            return first
    return None


def is_first_author(first_author_str):
    if first_author_str is None:
        return False
    name_parts = AUTHOR_NAME.lower().split()
    return all(part in first_author_str for part in name_parts)


def build_markdown(first_author_papers, contributed_papers):
    lines = [
        "---",
        'title: "Publications"',
        "permalink: /publications/",
        "layout: single",
        "author_profile: true",
        "---",
        "",
        "## First Author",
        "",
    ]
    for p in first_author_papers:
        lines.append(f"- [{p['title']}]({p['url']})")
        lines.append("")

    lines += ["---", "", "## Contributed To", ""]
    for p in contributed_papers:
        lines.append(f"- [{p['title']}]({p['url']})")
        lines.append("")

    return "\n".join(lines)


def main():
    print("Fetching Scholar profile...")
    try:
        html = fetch_profile()
    except requests.RequestException as e:
        print(f"Error fetching Scholar profile: {e}", file=sys.stderr)
        sys.exit(1)

    papers = parse_papers(html)
    if not papers:
        print("No papers found — Scholar may have blocked the request.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(papers)} papers. Checking author order...")

    first_author, contributed = [], []
    for i, paper in enumerate(papers, 1):
        print(f"  [{i}/{len(papers)}] {paper['title'][:70]}...")
        first = get_first_author(paper["url"])
        if is_first_author(first):
            first_author.append(paper)
        else:
            contributed.append(paper)

    print(f"\nFirst author: {len(first_author)} | Contributed: {len(contributed)}")

    md = build_markdown(first_author, contributed)
    OUTPUT_FILE.write_text(md)
    print(f"Written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
