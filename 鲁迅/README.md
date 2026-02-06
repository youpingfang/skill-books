# luxun-books

鲁迅全集阅读与检索技能。支持按卷目录浏览、关键词全文检索，并可返回指定文章全文或片段。

## 功能
- 按目录浏览（书名 → 文章列表）
- 关键词全文检索（返回命中片段 + 文章定位）
- 输出原文，不改写

## 数据来源
- marxists.org《鲁迅全集》
- 目录索引：`references/catalog.json`
- 正文：`references/texts/*.txt`

## 使用示例
- “打开《朝花夕拾》目录”
- “查‘革命’在哪些文章出现？”
- “给我《呐喊·药》全文”

## 安装
### 方式 A：放到 OpenClaw 的 skills 目录（推荐）
```bash
# 复制本目录到你的 OpenClaw skills 目录
cp -r luxun-books /root/.openclaw/workspace/skills/
```

### 方式 B：打包为 .skill
```bash
python3 /usr/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py \
  /path/to/luxun-books \
  /path/to/output
```
生成的包为：`/path/to/output/luxun-books.skill`

## 维护/更新
1. 生成目录
```bash
python3 scripts/build_catalog_marxists.py
```
2. 分批下载/更新正文
```bash
python3 scripts/download_texts_marxists.py
```

> 如需继续补采未收录卷，可扩展脚本源列表并重复执行。

## 许可与声明
- 本技能仅用于学习与研究；原文版权归原作者及相关权利方所有。
