# Novel Crawler System & Gemini Skill

这是一个高度集成、稳健且具备反爬虫能力的小说抓取系统。它已经从一组零散的脚本进化为一个统一的框架，并作为 **Gemini CLI Skill** 集成到了你的工作流中。

## 🚀 项目亮点

1.  **统一工具库 (`crawl_utils.py`)**：将网络请求、Headers 伪装、自动重试、Meta 信息提取、计时器和文件保存逻辑全部标准化。
2.  **稳健的反爬机制**：集成了随机基础休眠 (1-3s) 和概率性长暂停 (5-15s)，模拟真人阅读行为，极大地降低了被封 IP 的风险。
3.  **智能分发入口 (`main.py`)**：无需关心具体脚本名，只需输入 URL，系统自动识别域名并调用对应的提取器。
4.  **内容深度清洗**：自动剔除半夏、52书库等站点的网页噪音和广告后缀，并修复了部分站点目录倒序的问题。
5.  **Gemini Skill 集成**：已打包为 `novel-crawler` 技能，支持通过自然语言在任何路径触发抓取任务。

## 🛠 系统架构

### 核心组件
- **`main.py`**: 统一入口，负责域名识别与任务分发。
- **`crawl_utils.py`**: 核心动力源，提供 `fetch_page`, `anti_crawling_pause`, `get_meta_info` 等通用功能。
- **特定提取脚本**: `novel_banxia.py`, `novel_52.py`, `novel_256.py`, `novel_sunzhinan.py` 仅保留核心解析规则。

### 支持站点
| 网站名称 | 支持域名 | 特色功能 |
| :--- | :--- | :--- |
| **半夏小说** | xbanxia.cc | 移除固定广告后缀，自动识别汉字章节 |
| **52书库** | 52shuku.net/vip | 自动处理多域名后缀，清理 Tips 广告 |
| **256文学** | 256wx.org/net | 动态匹配 BookID，过滤目录底部的推荐书链 |
| **孙指南/醋溜儿** | sunzhinan.com | **自动校正倒序目录**，合并两页内容为一章 |

## 📖 使用指南

### 1. 命令行直接使用
在项目目录下运行：
```bash
python3 main.py [小说主页URL]
```

### 2. 作为 Gemini Skill 使用 (推荐)
你可以在 Gemini CLI 中随时输入：
> "帮我下载这部小说: https://www.xbanxia.cc/books/187646.html"

Gemini 会自动调用已安装的 `novel-crawler` 技能在后台运行。

## 📂 文件存放
- **代码位置**: `/Users/funanhe/Documents/0.MyCode/novel/`
- **Skill 位置**: `~/.gemini/skills/novel-crawler/`
- **抓取结果**: 所有 `.txt` 文件默认保存至 `~/Downloads/`。

---
*Created by Gemini CLI Assistant | April 27, 2026*
