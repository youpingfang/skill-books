# skill-books

本仓库用于存放 **OpenClaw** 的书籍/素材类技能数据（如鲁迅全集、户晨风内容库）。

## 用途（请务必阅读）
- **仅用于 OpenClaw 技能的本地检索与内容引用**
- 不包含应用程序代码、运行服务或前端
- 作为技能的数据源/资料库被 OpenClaw 加载

## 快速安装（示例：luxun-books）
### 方法 A：直接拷贝到 OpenClaw skills 目录
```bash
git clone https://github.com/youpingfang/skill-books.git
cp -r skill-books/luxun-books /root/.openclaw/workspace/skills/
```

### 方法 B：打包为 .skill
```bash
python3 /usr/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py \
  /path/to/skill-books/luxun-books \
  /path/to/output
```
生成的包为：`/path/to/output/luxun-books.skill`

## 目录说明
- `luxun-books/`：鲁迅全集阅读与检索技能数据

## 备注
- 数据来源与具体说明见各技能目录内的 `README.md` 与 `SKILL.md`
