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
        data=json.load(f)

    for fname in os.listdir(TEXT_DIR):
        if not fname.endswith('.txt'):
            continue
        m=re.match(r"(\d{2})-(\d{3})-.*\.txt", fname)
        if not m:
            continue
        v_idx=int(m.group(1))
        i_idx=int(m.group(2))
        if v_idx<=0 or v_idx>len(data):
            continue
        items=data[v_idx-1].get('items',[])
        if i_idx<=0 or i_idx>len(items):
            continue
        item=items[i_idx-1]
        title=item.get('title','').strip()
        if title in ('上一篇','下一篇','回主页'):
            continue
        vol_name=data[v_idx-1].get('volume','').replace('・','').strip()
        vol_name=re.sub(r"（.*?）","",vol_name).strip() or '未命名'
        vol_dir=os.path.join(TEXT_DIR, vol_name)
        os.makedirs(vol_dir, exist_ok=True)
        new_name=f"{safe(title)}.txt"
        new_path=os.path.join(vol_dir, new_name)
        old_path=os.path.join(TEXT_DIR, fname)
        if os.path.abspath(old_path)!=os.path.abspath(new_path):
            if os.path.exists(new_path):
                k=2
                while True:
                    new_name=f"{safe(title)}_{k}.txt"
                    new_path=os.path.join(vol_dir, new_name)
                    if not os.path.exists(new_path):
                        break
                    k+=1
            os.rename(old_path, new_path)
        item['file']=f"references/texts/{vol_name}/{new_name}".replace('\\','/')

    with open(CATALOG, "w", encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

if __name__=='__main__':
    main()
