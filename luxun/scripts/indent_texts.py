#!/usr/bin/env python3
import os

TEXT_DIR = os.path.join(os.path.dirname(__file__), "..", "references", "texts")


def indent_paragraphs(text: str) -> str:
    lines = text.split("\n")
    out = []
    for line in lines:
        if line.strip() == "":
            out.append("")
        else:
            # add two full-width spaces for paragraph indent
            out.append("\u3000\u3000" + line.lstrip())
    return "\n".join(out).rstrip() + "\n"


def main():
    for root, _, files in os.walk(TEXT_DIR):
        for name in files:
            if not name.endswith(".txt"):
                continue
            path = os.path.join(root, name)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            with open(path, "w", encoding="utf-8") as f:
                f.write(indent_paragraphs(text))

if __name__ == "__main__":
    main()
