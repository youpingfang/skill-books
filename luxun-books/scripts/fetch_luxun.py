#!/usr/bin/env python3
import os, json, re
from urllib.parse import urljoin
import requests
import chardet

BASE = "http://xwww.xys.org"

BOOKS = {
    "呐喊": {
        "base": "/xys/classics/Lu-Xun/Nahan/",
        "items": [
            ("呐喊·序", "preface.txt"),
            ("狂人日记", "kuangren.txt"),
            ("孔乙己", "kongyiji.txt"),
            ("药", "yao.txt"),
            ("明天", "mingtian.txt"),
            ("一件小事", "xiaoshi.txt"),
            ("头发的故事", "toufa.txt"),
            ("风波", "fengbo.txt"),
            ("故乡", "guxiang.txt"),
            ("阿Q正传", "aq.txt"),
            ("端午节", "duanwu.txt"),
            ("白光", "baiguang.txt"),
            ("兔和猫", "tumao.txt"),
            ("鸭的喜剧", "ya.txt"),
            ("社戏", "shexi.txt"),
        ],
    },
    "彷徨": {
        "base": "/xys/classics/Lu-Xun/Panghuang/",
        "items": [
            ("祝福", "zhufu.txt"),
            ("酒楼", "jiulou.txt"),
            ("幸福的家庭", "xingfu.txt"),
            ("肥皂", "feizao.txt"),
            ("长明灯", "changming.txt"),
            ("示众", "shizhong.txt"),
            ("高老夫子", "gao.txt"),
            ("孤独者", "guduzhe.txt"),
            ("伤逝", "shangshi.txt"),
            ("兄弟", "xiongdi.txt"),
        ],
    },
    "朝花夕拾": {
        "base": "/xys/classics/Lu-Xun/Zhaohua/",
        "items": [
            ("小引", "preface.txt"),
            ("狗·猫·鼠", "goumao.txt"),
            ("阿长与《山海经》", "achang.txt"),
            ("二十四孝图", "24xiao.txt"),
            ("五猖会", "5chang.txt"),
            ("无常", "wuchang.txt"),
            ("从百草园到三味书屋", "baicao.txt"),
            ("父亲的病", "fuqin.txt"),
            ("琐记", "suoji.txt"),
            ("藤野先生", "tengye.txt"),
            ("范爱农", "fan.txt"),
            ("后记", "houji.txt"),
        ],
    },
}

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "references", "texts")


def fetch_text(url: str) -> str:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    raw = r.content
    det = chardet.detect(raw)
    enc = det.get("encoding") or "utf-8"
    try:
        text = raw.decode(enc, errors="ignore")
    except Exception:
        text = raw.decode("utf-8", errors="ignore")
    # normalize
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.strip()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    catalog = {}
    for book, info in BOOKS.items():
        base = info["base"]
        catalog[book] = []
        for idx, (title, fname) in enumerate(info["items"], start=1):
            url = urljoin(BASE, base + fname)
            text = fetch_text(url)
            safe = re.sub(r"[^0-9A-Za-z_\-]+", "_", title).strip("_") or f"item{idx}"
            out_name = f"{book}-{idx:02d}-{safe}.txt"
            out_path = os.path.join(OUT_DIR, out_name)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text + "\n")
            catalog[book].append({
                "title": title,
                "url": url,
                "file": f"references/texts/{out_name}",
            })
    with open(os.path.join(os.path.dirname(__file__), "..", "references", "catalog.json"), "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
