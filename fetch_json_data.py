#!/usr/bin/env python3
"""
Generic GitHub Code Search downloader
-------------------------------------

Key additions in v1.2
---------------------
• Duplicates handling: if the would-be final filename already exists
  in --out OR was downloaded earlier in the same session, the script
  skips it and continues searching.

• All previous features retained:
  - extension / keyword / size filters
  - GitHub PAT authentication
  - optional --validator <exe>  (keep file only if exit code == 0)
"""

import argparse
import os
import subprocess
import sys
import time
from math import ceil
from pathlib import Path
from typing import Optional, Sequence

import requests


# --------------------------------------------------------------------------- #
# Utilities
# --------------------------------------------------------------------------- #
def build_headers(token: str | None) -> dict[str, str]:
    hdr = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "GenericBulkFetcher/1.2",
    }
    if token:
        hdr["Authorization"] = f"Bearer {token}"
    return hdr


def get_json(url: str, headers: dict, timeout: int) -> Optional[dict]:
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        if r.status_code == 200:
            return r.json()
        print(f"[{r.status_code}] {url}", file=sys.stderr)
    except Exception as exc:
        print(f"[Error] {url} – {exc}", file=sys.stderr)
    return None


def download(url: str, dest: Path, headers: dict, timeout: int) -> bool:
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        if r.status_code == 200:
            dest.write_bytes(r.content)
            return True
        print(f"[{r.status_code}] {url}", file=sys.stderr)
    except Exception as exc:
        print(f"[Error] {url} – {exc}", file=sys.stderr)
    return False


def validate_file(exe: str, file_path: Path, timeout: int = 10) -> bool:
    try:
        completed = subprocess.run(
            [exe, str(file_path)],
            timeout=timeout,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return completed.returncode == 0
    except Exception as exc:
        print(f"[ValidatorError] {file_path} – {exc}", file=sys.stderr)
        return False


# --------------------------------------------------------------------------- #
# Main logic
# --------------------------------------------------------------------------- #
def main(argv: Sequence[str] | None = None):
    ap = argparse.ArgumentParser(
        description="Bulk download files from GitHub with optional validation"
    )
    ap.add_argument("-e", "--ext", help="file extension filter, e.g., ini / cfg / md")
    ap.add_argument("-q", "--query", default="", help="keyword query (optional)")
    ap.add_argument("-n", "--total", type=int, required=True, help="total files to fetch")
    ap.add_argument("--size", default="<10000", help='size filter, e.g., "<5000"')
    ap.add_argument("--out", default="data", help="output directory")
    ap.add_argument("--pause", type=float, default=0.7, help="pause between requests (s)")
    ap.add_argument("--timeout", type=int, default=10, help="HTTP timeout (s)")
    ap.add_argument("--token", help="GitHub PAT; else read $GITHUB_TOKEN")
    ap.add_argument("--validator", help="path to program that validates each file")

    args = ap.parse_args(argv)
    token = args.token or os.getenv("GITHUB_TOKEN")
    if not token:
        ap.error("GitHub token missing: set GITHUB_TOKEN or use --token")

    headers = build_headers(token)
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Track duplicates both on disk (previous runs) and within this run
    existing_files = {p.name for p in out_dir.iterdir()}
    seen_names_this_run: set[str] = set()

    # Compose GitHub search query
    parts = []
    if args.ext:
        parts.append(f"extension:{args.ext}")
    if args.query:
        parts.append(args.query)
    if args.size:
        parts.append(f"size:{args.size}")
    query = "+".join(parts)

    print(f"[*] Search query: {query}")
    per_page = 100
    pages_needed = ceil(args.total / per_page)
    saved = 0

    for page in range(1, pages_needed + 1):
        url = f"https://api.github.com/search/code?q={query}&per_page={per_page}&page={page}"
        data = get_json(url, headers, args.timeout)
        if not data or "items" not in data:
            print("[!] Empty or error response – stopping.")
            break

        for item in data["items"]:
            if saved >= args.total:
                break

            # Build final filename
            final_name = f"{saved+1:03d}_{item['name']}"
            if final_name in existing_files or final_name in seen_names_this_run:
                print(f"[↷] Duplicate skipped: {final_name}")
                continue

            meta = get_json(item["url"], headers, args.timeout)
            if not meta or "download_url" not in meta:
                continue

            tmp_path = out_dir / f"tmp_{saved+1:03d}"
            final_path = out_dir / final_name

            if not download(meta["download_url"], tmp_path, headers, args.timeout):
                continue

            if args.validator and not validate_file(args.validator, tmp_path):
                print(f"[✗] Validation failed: {final_name}")
                tmp_path.unlink(missing_ok=True)
                time.sleep(args.pause)
                continue

            tmp_path.rename(final_path)
            print(f"[✓] {final_name}")
            existing_files.add(final_name)
            seen_names_this_run.add(final_name)
            saved += 1
            time.sleep(args.pause)

        if saved >= args.total:
            break
        time.sleep(args.pause)

    print(f"[✓] Downloaded {saved} unique file(s) → {out_dir}")


if __name__ == "__main__":
    main()