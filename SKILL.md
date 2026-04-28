---
name: novel-crawler
description: 一个多功能小说抓取工具，支持半夏小说、52书库、256文学和孙指南/醋溜儿。当用户请求下载、抓取小说或提供这些网站的链接时触发。
---

# Novel Crawler Skill

此 Skill 允许 Gemini CLI 自动抓取特定小说网站的内容并保存为合并的 .txt 文件。

## 支持的网站

- 半夏小说 (xbanxia.cc)
- 52书库 (52shuku.net/vip)
- 256文学 (256wx.org/net)
- 孙指南/醋溜儿 (sunzhinan.com/culiu.cc)

## 使用方法

1. **自动抓取**: 直接向 Gemini 提供小说主页 URL，例如：
   "帮我抓取这部小说: https://www.xbanxia.cc/books/187646.html"

2. **触发逻辑**: Gemini 会调用 `scripts/main.py` 并传入 URL。脚本会自动识别网站并启动对应的爬虫。

## 核心流程

- 调用 `python3 scripts/main.py [URL]`（注意：在 Skill 内部调用时需使用相对于 Skill 根目录的路径）。
- 所有内容会自动保存到用户的 `~/Downloads` 目录下。
- 抓取过程包含随机休眠以防止被封禁。

## 资源

- `scripts/main.py`: 统一入口
- `scripts/crawl_utils.py`: 通用工具（请求、保存、统计）
- `scripts/novel_*.py`: 各站专用提取逻辑
