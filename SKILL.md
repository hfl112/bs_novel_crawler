---
name: novel-crawler
description: 一个多功能小说抓取工具，支持半夏小说、52书库、256文学、孙指南/醋溜儿和思兔网。当用户请求下载、抓取小说或提供这些网站的链接时触发。
---

# Novel Crawler Skill

此 Skill 允许 Gemini CLI 自动抓取特定小说网站的内容并保存为合并的 .txt 文件。

## 支持的网站

- 半夏小说 (xbanxia.cc)
- 52书库 (52shuku.net/vip)
- 256文学 (256wx.org/net)
- 孙指南/醋溜儿 (sunzhinan.com/culiu.cc)
- 思兔网 (sto520.com/situ)

## 使用方法

1. **自动抓取**: 直接向 Gemini 提供小说主页 URL，例如：
   "帮我抓取这部小说: https://www.xbanxia.cc/books/187646.html"

2. **触发逻辑**: Gemini 会调用 `main.py [URL]`。脚本会自动识别网站并启动对应的爬虫。
