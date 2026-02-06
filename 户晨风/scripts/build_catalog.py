#!/usr/bin/env python3
import os, json

BASE = os.path.join(os.path.dirname(__file__), "..", "references", "source")
OUT = os.path.join(os.path.dirname(__file__), "..", "references", "catalog.json")


def first_line(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if s:
                    return s[:120]
    except Exception:
        return None
    return None


def main():
    items = []
    for root, _, files in os.walk(BASE):
        for name in files:
            if not name.endswith(".md"):
                continue
            full = os.path.join(root, name)
            rel = os.path.relpath(full, os.path.join(os.path.dirname(__file__), ".."))
            title = first_line(full) or name.replace(".md", "")
            items.append({
                "title": title,
                "file": rel.replace("\\", "/"),
            })
    items.sort(key=lambda x: x["file"])
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
