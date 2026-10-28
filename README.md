# 网络小说爬虫 Skill (Novel Crawler)

这是一个高度集成、稳健且具备反爬虫能力的网络小说抓取系统，支持统一入口分发，并支持作为 Gemini CLI Skill 集成。

## 🌐 支持的书库

- **半夏小说** (`xbanxia.cc`)
- **52书库** (`52shuku.net/vip`)
- **256文学** (`256wx.org/net`)
- **孙指南 / 醋溜儿** (`sunzhinan.com` / `culiu.cc`)
- **思兔网** (`sto520.com` / `situ`)

---

## 🛠 系统架构

- **`main.py`**: 统一调度入口，根据传入的 URL 域名自动识别并分发给对应站点解析器。
- **`crawl_utils.py`**: 核心动力底座，提供标准化的网页请求、自动重试、反爬随机休眠、元数据提取、计时与文本保存。
- **`parsers/`**: 独立站点解析器子包。
  - `novel_banxia.py`: 半夏小说专有解析
  - `novel_52.py`: 52书库专有解析
  - `novel_256.py`: 256文学专有解析
  - `novel_sunzhinan.py`: 孙指南 / 醋溜儿专有解析（含自动倒序纠偏）
  - `novel_situ.py`: 思兔网专有解析（含敏感词字典还原）

---

## 📖 使用指南

### 1. 命令行直接运行
```bash
python3 main.py [小说主页URL]
```

### 2. 作为 Gemini Skill 使用 (推荐)
你可以在命令行或对话中直接输入：
> "帮我下载这部小说: https://www.xbanxia.cc/books/342243.html"

所有结果默认自动合并保存为 `.txt` 文件输出至 `~/Downloads/` 目录下。

---

## 📦 依赖安装

```bash
pip install -r requirements.txt
```
