#!/usr/bin/env python3
import os, re, json, html
from urllib.parse import urljoin
import requests
import chardet

BASE = "https://www.marxists.org/chinese/reference-books/luxun/"
INDEX = urljoin(BASE, "index.htm")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "references", "texts")
CATALOG_PATH = os.path.join(os.path.dirname(__file__), "..", "references", "catalog.json")


def fetch(url: str) -> str:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    raw = r.content
    enc = chardet.detect(raw).get("encoding") or "utf-8"
    text = raw.decode(enc, errors="ignore")
    return text


def extract_links(html_text: str):
    # returns list of (href, text)
    links = re.findall(r'<a\s+[^>]*href\s*=\s*"([^"]+)"[^>]*>(.*?)</a>', html_text, flags=re.I|re.S)
    out = []
    for href, text in links:
        t = re.sub(r"<[^>]+>", "", text)
        t = html.unescape(t).strip()
        out.append((href.strip(), t))
    return out


def clean_text(html_text: str) -> str:
    # remove script/style
    html_text = re.sub(r"<script[\s\S]*?</script>", "", html_text, flags=re.I)
    html_text = re.sub(r"<style[\s\S]*?</style>", "", html_text, flags=re.I)
    # convert <br> and <p> to newlines
    html_text = re.sub(r"<br\s*/?>", "\n", html_text, flags=re.I)
    html_text = re.sub(r"</p>", "\n", html_text, flags=re.I)
    # strip tags
    text = re.sub(r"<[^>]+>", "", html_text)
    text = html.unescape(text)
    # normalize spaces
    lines = [line.strip().replace("\u3000", "") for line in text.split("\n")]
    # drop empty leading/trailing
    cleaned = "\n".join([l for l in lines if l != ""])
    return cleaned.strip() + "\n"


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    index_html = fetch(INDEX)
    # find volume links (01/000.htm, 02/000.htm, 31/index.htm, etc.)
    vol_links = []
    for href, title in extract_links(index_html):
        if re.match(r"\d{2}/(000|index)\.htm", href):
            vol_links.append((href, title))
    # de-dup by href
    seen = set()
    vols = []
    for href, title in vol_links:
        if href in seen:
            continue
        seen.add(href)
        vols.append((href, title or href))

    catalog = []
    for v_idx, (href, v_title) in enumerate(vols, start=1):
        vol_url = urljoin(BASE, href)
        vol_html = fetch(vol_url)
        items = []
        for item_href, item_title in extract_links(vol_html):
            # content pages are like 001.htm, 002.htm ...
            if re.match(r"\d{3}\.htm", item_href):
                item_url = urljoin(vol_url, item_href)
                item_html = fetch(item_url)
                text = clean_text(item_html)
                safe_title = re.sub(r"[^0-9A-Za-z_\-]+", "_", item_title).strip("_") or f"item{len(items)+1}"
                out_name = f"{v_idx:02d}-{safe_title}.txt"
                out_path = os.path.join(OUT_DIR, out_name)
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(text)
                items.append({
                    "title": item_title,
                    "url": item_url,
                    "file": f"references/texts/{out_name}",
                })
        if items:
            catalog.append({
                "volume": v_title,
                "url": vol_url,
                "items": items,
            })

    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
