#!/usr/bin/env python3
import os, re

BASE = os.path.join(os.path.dirname(__file__), "..", "references", "texts")


def normalize(text: str) -> str:
    # normalize newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    out = []
    blank = 0
    for line in lines:
        # trim leading/trailing spaces (including full-width)
        line = line.strip().replace("\u3000", "")
        if line == "":
            blank += 1
            if blank <= 1:
                out.append("")
            continue
        blank = 0
        # collapse multiple spaces inside line
        line = re.sub(r"[ \t]{2,}", " ", line)
        out.append(line)
    return "\n".join(out).strip() + "\n"


def main():
    for name in os.listdir(BASE):
        if not name.endswith(".txt"):
            continue
        path = os.path.join(BASE, name)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        norm = normalize(text)
        with open(path, "w", encoding="utf-8") as f:
            f.write(norm)

if __name__ == "__main__":
    main()
