#!/usr/bin/env python3
"""
Download 100 .ini files from GitHub using the Code Search API.

Requirements:
  pip install requests

Optional:
  export GITHUB_TOKEN="ghp_xxx"   # increases rate‑limit from 10 → 30 req/min
"""

import os
import time
import requests
from pathlib import Path

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
SAVE_DIR          = Path("ini_data")          # target folder
TOTAL_FILES       = 100                       # how many .ini files to pull
REQUEST_TIMEOUT   = 10                        # seconds
PAUSE_BETWEEN_REQ = 0.7                       # be gentle to GitHub
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "BulkIniFetcher/1.0",
}

# Insert PAT if available (prevents 403 / low quota)
if token := os.getenv("GITHUB_TOKEN"):
    HEADERS["Authorization"] = f"Bearer {token}"

SEARCH_URL = (
    "https://api.github.com/search/code"
    "?q=extension:ini+size:<10000"     # skip huge binaries
    f"&per_page={TOTAL_FILES}&page=1"
)

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def get_json(url: str) -> dict | None:
    """GET JSON with basic error handling."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            return r.json()
        print(f"[{r.status_code}] {url}")
    except Exception as exc:
        print(f"[Error] {url} – {exc}")
    return None


def download_file(raw_url: str, dest: Path) -> bool:
    """Download raw text and save; return success flag."""
    try:
        r = requests.get(raw_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            dest.write_bytes(r.content)
            return True
        print(f"[{r.status_code}] {raw_url}")
    except Exception as exc:
        print(f"[Error] {raw_url} – {exc}")
    return False


# --------------------------------------------------------------------------- #
# Main logic
# --------------------------------------------------------------------------- #
def main() -> None:
    SAVE_DIR.mkdir(exist_ok=True)
    print("[*] Searching GitHub code…")
    search_data = get_json(SEARCH_URL)
    if not search_data or "items" not in search_data:
        raise SystemExit("Search failed or returned zero items.")

    items = search_data["items"][:TOTAL_FILES]
    print(f"[*] Found {len(items)} .ini candidates. Start downloading…")

    for idx, item in enumerate(items, 1):
        # Step 1: query file‑details API to get download_url
        file_api_url = item["url"]          # e.g., https://api.github.com/repos/.../contents/.../foo.ini
        file_info    = get_json(file_api_url)
        if not file_info or "download_url" not in file_info:
            print(f"[!] Skip: unable to read metadata for {file_api_url}")
            continue

        raw_url  = file_info["download_url"]
        filename = SAVE_DIR / f"{idx:03d}_{item['name']}"
        ok = download_file(raw_url, filename)
        if ok:
            print(f"[✓] {filename.name}")
        else:
            print(f"[✗] Failed to save {filename.name}")

        time.sleep(PAUSE_BETWEEN_REQ)       # stay under rate‑limit

    print("[✓] Done.")

if __name__ == "__main__":
    main()