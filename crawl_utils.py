import time
import random
import urllib.request
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import os

# 默认 Headers
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def anti_crawling_pause(base_range=(1, 3), long_pause_chance=0.3, long_pause_range=(5, 15)):
    """通用反爬虫休眠逻辑 - 已恢复安全速度"""
    sleep_time = random.uniform(*base_range)
    time.sleep(sleep_time)
    if random.random() < long_pause_chance:
        long_sleep = random.uniform(*long_pause_range)
        print(f"  [Anti-Bot] 触发随机长暂停: 预计休眠 {long_sleep:.2f} 秒...")
        time.sleep(long_sleep)

def fetch_page(url, retries=2):
    """通用的页面请求函数"""
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
            with urllib.request.urlopen(req, timeout=15) as response:
                html = response.read()
                return BeautifulSoup(html, 'lxml')
        except Exception as e:
            if i < retries:
                time.sleep((i + 1) * 3)
            else:
                print(f"  [Fatal] 无法获取页面 {url}: {e}")
    return None

def get_meta_info(soup):
    """通用 Meta 信息提取 - 增强版"""
    info = {'title': '未知书籍', 'author': '未知作者'}
    if not soup: return info

    # 1. 尝试从 OpenGraph Meta 标签提取
    og_title = soup.find('meta', property='og:novel:book_name') or soup.find('meta', property='og:title')
    og_author = soup.find('meta', property='og:novel:author') or soup.find('meta', property='author')
    
    if og_title: info['title'] = og_title.get('content', '').strip()
    if og_author: info['author'] = og_author.get('content', '').strip()

    # 2. 针对半夏等特定结构的备选方案
    if info['author'] == '未知作者':
        # 尝试查找包含 'author' 链接的文本
        a_author = soup.find('a', href=re.compile(r'author'))
        if a_author: info['author'] = a_author.string.strip()

    # 3. 备选方案：解析 <title> 标签
    if info['title'] == '未知书籍' or info['author'] == '未知作者':
        title_str = soup.title.string if soup.title else ""
        if title_str:
            for sep in ['_', '：', ':', ' ', ',']:
                if sep in title_str:
                    parts = title_str.split(sep)
                    if info['title'] == '未知书籍': info['title'] = parts[0].strip()
                    if info['author'] == '未知作者' and len(parts) > 1: info['author'] = parts[1].strip()
                    break

    # 4. 深度清理
    for noise in ['最新章节', '在线阅读', '全文阅读', '小说', '免费', '全文', 'txt', '下载']:
        info['title'] = info['title'].split(noise)[0].strip()
        info['author'] = info['author'].split(noise)[0].strip()
    
    info['title'] = info['title'].strip('《》, ')
    info['author'] = info['author'].strip('《》, ')
    
    return info

class Timer:
    def __init__(self):
        self.start_time = time.time()
    
    def elapsed(self):
        return time.time() - self.start_time
    
    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{int(mins)}分{int(secs)}秒"

def save_to_file(book_name, author, page_text_dict, timer=None, save_path=None):
    """通用的保存逻辑"""
    if not save_path:
        clean_name = re.sub(r'[\\/:*?"<>|]', '_', f"{book_name}-{author}")
        save_path = os.path.expanduser(f"~/Downloads/{clean_name}.txt")
    
    count = len(page_text_dict)
    print(f"\n--- 抓取完成统计 ---")
    print(f"书籍名称: {book_name}")
    print(f"作者: {author}")
    print(f"总计章节: {count} 章/页")
    
    if timer:
        total_time = timer.elapsed()
        print(f"总计耗时: {timer.format_time(total_time)}")
    
    print(f"正在保存到: {save_path}")
    with open(save_path, "w", encoding='utf-8') as f:
        for i in sorted(page_text_dict.keys()):
            f.write(page_text_dict[i])
            if not page_text_dict[i].endswith('\n'):
                f.write('\n')
    print("文件保存成功！\n")
