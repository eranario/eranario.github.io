# eranario.github.io

Personal academic site built with Jekyll + [Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes).

---

## Running locally

```bash
bundle install       # first time only
bundle exec jekyll serve
```

Open `http://localhost:4000`.

---

## Syncing publications from Google Scholar

Publications are pulled from [Google Scholar](https://scholar.google.com/citations?user=Zc7DhZMAAAAJ) and split into **First Author** vs **Contributed To** based on author order.

**Install dependencies (first time only):**
```bash
pip install requests beautifulsoup4
```

**Run the sync:**
```bash
python3 scripts/sync_publications.py
```

This overwrites `_pages/publications.md` with the latest papers from Scholar. Commit and push when done.

> Note: Google Scholar occasionally rate-limits scrapers. If the script errors out, wait a few minutes and try again.
