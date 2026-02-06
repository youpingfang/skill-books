#!/usr/bin/env python3
import os, re

TEXT_DIR = os.path.join(os.path.dirname(__file__), "..", "references", "texts")


def clean(text: str) -> str:
    lines = [l.strip() for l in text.split("\n")]
    out = []
    for l in lines:
        if l in ("中文马克思主义文库 -> 参考图书・左翼文化 -> 鲁迅全集", "上一篇", "下一篇", "回主页"):
            continue
        if re.match(r"^〔\d+〕", l):
            # drop footnotes entirely
            continue
        if re.match(r"^\d+$", l):
            # drop section numbers
            continue
        if l in ("※ ※ ※", "完"):
            continue
        if l == "无题" and out and out[-1] == "无题":
            continue
        if l == "":
            if out and out[-1] != "":
                out.append("")
            continue
        out.append(l)
    return "\n".join(out).strip() + "\n"


def main():
    for name in os.listdir(TEXT_DIR):
        if not name.endswith(".txt"):
            continue
        path = os.path.join(TEXT_DIR, name)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        cleaned = clean(text)
        with open(path, "w", encoding="utf-8") as f:
            f.write(cleaned)

if __name__ == "__main__":
    main()
