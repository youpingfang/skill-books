#!/usr/bin/env python3
import os, re, json

BASE = os.path.join(os.path.dirname(__file__), "..")
CATALOG = os.path.join(BASE, "references", "catalog.json")
TEXT_DIR = os.path.join(BASE, "references", "texts")


def safe(name):
    name=name.replace('/','-').strip()
    name=re.sub(r"[\\:*?\"<>|]","_",name)
    return name or '未命名'


def main():
    with open(CATALOG, "r", encoding="utf-8") as f:
        catalog=json.load(f)

    # build volume map
    vol_map = {}
    for v in catalog:
        vol_name = re.sub(r"（.*?）","", v.get('volume','').replace('・','').strip())
        if not vol_name:
            continue
        items=[it for it in v.get('items',[]) if it.get('title') not in ('上一篇','下一篇','回主页')]
        vol_map[vol_name]=items

    for vol_name, items in vol_map.items():
        vol_dir = os.path.join(TEXT_DIR, vol_name)
        if not os.path.isdir(vol_dir):
            continue
        # rename itemN.txt
        for idx, it in enumerate(items, start=1):
            old = os.path.join(vol_dir, f'item{idx}.txt')
            if not os.path.exists(old):
                continue
            new_name = f"{safe(it.get('title',''))}.txt"
            new = os.path.join(vol_dir, new_name)
            if os.path.exists(new):
                k=2
                while True:
                    new_name=f"{safe(it.get('title',''))}_{k}.txt"
                    new=os.path.join(vol_dir,new_name)
                    if not os.path.exists(new):
                        break
                    k+=1
            os.rename(old, new)
            it['file']=f"references/texts/{vol_name}/{new_name}".replace('\\','/')

    with open(CATALOG, "w", encoding="utf-8") as f:
        json.dump(catalog,f,ensure_ascii=False,indent=2)

if __name__=='__main__':
    main()
