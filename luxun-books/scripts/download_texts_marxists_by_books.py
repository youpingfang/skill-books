#!/usr/bin/env python3
import os, re, json, time
import requests
import chardet

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
CATALOG_PATH = os.path.join(BASE_DIR, "references", "catalog.json")
OUT_DIR = os.path.join(BASE_DIR, "references", "texts")
STATE_PATH = os.path.join(BASE_DIR, "references", "download_state_by_books.json")

TARGET_BOOKS = [
    "三闲集","二心集","南腔北调集","伪自由书","准风月谈","花边文学",
    "且介亭杂文","且介亭杂文二集","且介亭杂文末编","且介亭杂文附集"
]

def fetch(url: str) -> str:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    raw = r.content
    enc = chardet.detect(raw).get("encoding") or "utf-8"
    return raw.decode(enc, errors="ignore")


def clean_text(html_text: str) -> str:
    html_text = re.sub(r"<script[\s\S]*?</script>", "", html_text, flags=re.I)
    html_text = re.sub(r"<style[\s\S]*?</style>", "", html_text, flags=re.I)
    html_text = re.sub(r"<br\s*/?>", "\n", html_text, flags=re.I)
    html_text = re.sub(r"</p>", "\n", html_text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", html_text)
    text = re.sub(r"^〔\d+〕.*$", "", text, flags=re.M)
    text = text.replace("上一篇", "").replace("下一篇", "").replace("回主页", "")
    lines = [line.strip().replace("\u3000", "") for line in text.split("\n")]
    cleaned = "\n".join([l for l in lines if l != ""])
    return cleaned.strip() + "\n"


def safe(name: str) -> str:
    name=name.replace('/','-').strip()
    name=re.sub(r"[\\:*?\"<>|]","_",name)
    return name or "未命名"


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"index": 0}


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def main(limit=100, sleep_s=0.3):
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    flat = []
    for v in catalog:
        vol_name = v.get("volume", "").replace("・", "").strip()
        vol_name = re.sub(r"（.*?）", "", vol_name).strip()
        if vol_name not in TARGET_BOOKS:
            continue
        for item in v.get("items", []):
            if item.get("title") in ("上一篇","下一篇","回主页"):
                continue
            flat.append((vol_name, item))

    state = load_state()
    start = state.get("index", 0)
    end = min(start + limit, len(flat))

    for idx in range(start, end):
        vol_name, item = flat[idx]
        url = item["url"]
        html_text = fetch(url)
        text = clean_text(html_text)
        # add two full-width spaces indent per line
        text = "\n".join([("\u3000\u3000" + l) if l.strip() else "" for l in text.split("\n")])
        vol_dir = os.path.join(OUT_DIR, vol_name)
        os.makedirs(vol_dir, exist_ok=True)
        title = safe(item.get("title",""))
        out_name = f"{title}.txt"
        out_path = os.path.join(vol_dir, out_name)
        if os.path.exists(out_path):
            k=2
            while True:
                out_name = f"{title}_{k}.txt"
                out_path = os.path.join(vol_dir, out_name)
                if not os.path.exists(out_path):
                    break
                k+=1
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        item["file"] = f"references/texts/{vol_name}/{out_name}".replace('\\','/')
        time.sleep(sleep_s)

    state["index"] = end
    save_state(state)
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    print(f"Downloaded {end-start} items ({end}/{len(flat)})")

if __name__ == "__main__":
    main()
