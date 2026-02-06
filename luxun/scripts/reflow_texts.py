#!/usr/bin/env python3
import os, re

BASE = os.path.join(os.path.dirname(__file__), "..", "references", "texts")


def reflow(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    paras = []
    buf = []
    for line in lines:
        line = line.replace("\u3000", " ").strip()
        if line == "":
            if buf:
                paras.append("".join(buf))
                buf = []
            else:
                if paras and paras[-1] != "":
                    paras.append("")
            continue
        # collapse internal multiple spaces
        line = re.sub(r"[ \t]{2,}", " ", line)
        buf.append(line)
    if buf:
        paras.append("".join(buf))
    # remove duplicate blank paras
    out = []
    blank = False
    for p in paras:
        if p == "":
            if not blank:
                out.append("")
            blank = True
        else:
            out.append(p)
            blank = False
    return "\n".join(out).strip() + "\n"


def main():
    for name in os.listdir(BASE):
        if not name.endswith(".txt"):
            continue
        path = os.path.join(BASE, name)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        out = reflow(text)
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)

if __name__ == "__main__":
    main()
