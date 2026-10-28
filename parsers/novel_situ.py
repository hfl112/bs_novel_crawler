import sys
import os
import re
from urllib.parse import urljoin

try:
    from crawl_utils import fetch_page, get_meta_info, anti_crawling_pause, save_to_file, Timer
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from crawl_utils import fetch_page, get_meta_info, anti_crawling_pause, save_to_file, Timer

SITU_SENSITIVE_WORDS = {
    '%e5%b1%81': '屁',
    '%e9%b8%a1': '鸡',
    '%e9%9b%9e': '鸡',
    '%e4%ba%b2': '亲',
    '%e8%83%b8': '胸',
    '%e7%a9%b4': '穴',
    '%e8%88%94': '舔',
    '%e5%94%87': '唇',
    '%e8%88%8c': '舌',
    '%e8%84%b1': '脱',
    '%e8%85%bf': '腿',
    '%e5%90%bb': '吻',
    '%e4%b9%b3': '乳',
    '%e8%a3%b8': '裸',
    '%e5%90%9f': '吟',
    '%e8%8c%8e': '茎',
    '%e8%82%a1': '股',
    '%e8%87%80': '臀',
    '%e6%b7%ab': '淫',
}

def extract_content(soup):
    """思兔网特有的内容提取与敏感词还原逻辑"""
    if not soup or not soup.body:
        return ""
    content_divs = soup.body.find_all('div', id='BookContent')
    if not content_divs:
        return ""
    content = ""
    for elem in content_divs[0]:
        if elem.string:
            content += '\n' + elem.string
    content = content.replace('\u3000', '\n')
    
    # 还原思兔网URL编码替换的敏感字
    for encoded, original in SITU_SENSITIVE_WORDS.items():
        content = content.replace(encoded, original)
        
    return content

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 -m parsers.novel_situ [URL]")
        return

    timer = Timer()
    url = sys.argv[1].strip()
    soup = fetch_page(url)
    if not soup:
        print(f"[错误] 无法获取首页内容: {url}")
        return

    meta = get_meta_info(soup)
    # 如果通用 meta 未识别出标题或作者，使用思兔特定规则
    if meta['title'] == '未知书籍' or meta['author'] == '未知作者':
        if soup.title and soup.title.string:
            des = soup.title.string
            author_match = des.replace('：', ':').replace('_', ':').replace('《', ':').split(':')
            if len(author_match) > 0 and meta['author'] == '未知作者':
                meta['author'] = author_match[0].strip()
            book_matches = re.findall(r'《(.*?)》', des)
            if book_matches and meta['title'] == '未知书籍':
                meta['title'] = book_matches[0].strip()

    print(f"开始抓取: {meta['title']} - {meta['author']}")

    # 提取总分页数
    n_pages = 1
    if soup.body:
        scripts = soup.body.find_all('script', src=False)
        for s in scripts:
            if s.string and "Page_select" in s.string:
                m = re.search(r'"Page_select",\d+,(?P<full_pages>\d+),(?P<current_page>\d+)', s.string)
                if m:
                    n_pages = int(m.group('full_pages'))
                    break

    page_text = {}
    for i in range(1, n_pages + 1):
        print(f"[{i}/{n_pages}] 正在抓取第 {i} 页... (已用时: {timer.format_time(timer.elapsed())})")
        if '-' in url:
            page_url = '-'.join(url.split('-')[:-1] + [f"{i}.html"])
        else:
            page_url = url
        page_soup = fetch_page(page_url)
        if page_soup:
            content = extract_content(page_soup)
            if content:
                page_text[i] = f"\n--- 第 {i} 页 ---\n" + content
        
        anti_crawling_pause()

    save_to_file(meta['title'], meta['author'], page_text, timer=timer)

if __name__ == "__main__":
    main()
