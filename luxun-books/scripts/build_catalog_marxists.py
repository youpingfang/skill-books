#!/usr/bin/env python3
import os, re, json, html
from urllib.parse import urljoin
import requests
import chardet

BASE = "https://www.marxists.org/chinese/reference-books/luxun/"
INDEX = urljoin(BASE, "index.htm")
CATALOG_PATH = os.path.join(os.path.dirname(__file__), "..", "references", "catalog.json")


def fetch(url: str) -> str:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    raw = r.content
    enc = chardet.detect(raw).get("encoding") or "utf-8"
    return raw.decode(enc, errors="ignore")


def extract_links(html_text: str):
    links = re.findall(r'<a\s+[^>]*href\s*=\s*"([^"]+)"[^>]*>(.*?)</a>', html_text, flags=re.I|re.S)
    out = []
    for href, text in links:
        t = re.sub(r"<[^>]+>", "", text)
        t = html.unescape(t).strip()
        out.append((href.strip(), t))
    return out


def main():
    index_html = fetch(INDEX)
    vol_links = []
    for href, title in extract_links(index_html):
        if re.match(r"\d{2}/(000|index)\.htm", href):
            vol_links.append((href, title))
    seen = set()
    vols = []
    for href, title in vol_links:
        if href in seen:
            continue
        seen.add(href)
        vols.append((href, title or href))

    catalog = []
    for href, v_title in vols:
        vol_url = urljoin(BASE, href)
        vol_html = fetch(vol_url)
        items = []
        for item_href, item_title in extract_links(vol_html):
            if re.match(r"\d{3}\.htm", item_href):
                item_url = urljoin(vol_url, item_href)
                items.append({
                    "title": item_title,
                    "url": item_url,
                    "file": ""  # to be filled after download
                })
        if items:
            catalog.append({
                "volume": v_title,
                "url": vol_url,
                "items": items
            })

    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
