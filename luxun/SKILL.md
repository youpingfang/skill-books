---
name: luxun
description: 鲁迅全集作品阅读与检索。用于提供目录选择与关键词搜索，按用户选择返回对应文章全文或片段。
---

# 鲁迅全集（marxists.org）

## 资料来源
- 参考目录与全文来自 marxists.org 的《鲁迅全集》页面（用户指定来源）。
- 目录索引：`references/catalog.json`
- 文章全文：`references/texts/*.txt`

## 使用方式

### 1) 目录选择
- 先读取 `references/catalog.json`，展示书名 → 文章标题列表。
- 用户选择后，打开对应 `file` 并返回全文（或用户指定的段落）。

### 2) 关键词搜索
- 在 `references/texts/*.txt` 中做全文关键词匹配。
- 输出：匹配文章列表（书名 + 标题），并给出命中片段（前后各 1-2 句）。
- 让用户选择要展开的全文。

## 注意
- 保持原文，不改写。
- 若用户要“摘要/解读/翻译”，再按需求处理。

## 维护
- 先运行 `scripts/build_catalog_marxists.py` 生成目录。
- 再运行 `scripts/download_texts_marxists.py` 分批下载正文（可多次运行继续）。
