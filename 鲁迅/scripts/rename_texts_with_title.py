#!/usr/bin/env python3
import os, re, json

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
CATALOG_PATH = os.path.join(BASE_DIR, "references", "catalog.json")
TEXT_DIR = os.path.join(BASE_DIR, "references", "texts")


def safe_title(title: str) -> str:
    t = re.sub(r"[^0-9A-Za-z_\-]+", "_", title).strip("_")
    return t or "item"


def main():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    for v_idx, vol in enumerate(catalog, start=1):
        for i_idx, item in enumerate(vol.get("items", []), start=1):
            old_file = item.get("file")
            if not old_file:
                continue
            old_path = os.path.join(BASE_DIR, old_file)
            if not os.path.exists(old_path):
                continue
            title = item.get("title", "")
            new_name = f"{v_idx:02d}-{i_idx:03d}-{safe_title(title)}.txt"
            new_rel = f"references/texts/{new_name}"
            new_path = os.path.join(BASE_DIR, new_rel)
            if old_path != new_path:
                os.rename(old_path, new_path)
                item["file"] = new_rel

    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
