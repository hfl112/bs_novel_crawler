import sys
import os
import re
import time
import random
from urllib.parse import urljoin

try:
    from crawl_utils import fetch_page, get_meta_info, anti_crawling_pause, save_to_file, Timer
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from crawl_utils import fetch_page, get_meta_info, anti_crawling_pause, save_to_file, Timer

def extract_content(soup):
    """孙指南特有的内容提取逻辑"""
    if not soup: return ""
    paragraphs = [str(i.string) for i in soup.find_all('p', class_=False) if i.string]
    return ''.join(paragraphs).replace('www.sunzhinan.com', '')

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 -m parsers.novel_sunzhinan [URL]")
        return

    url = sys.argv[1]
    book_id_match = re.search(r'/books/(\d+)/', url)
    book_id = book_id_match.group(1) if book_id_match else ""

    timer = Timer()
    soup = fetch_page(url)
    meta = get_meta_info(soup)
    print(f"开始抓取: {meta['title']} - {meta['author']}")

    all_links = soup.find_all('a', href=re.compile(f'/read/{book_id}/\\d+\\.html'), title=True)
    
    unique_chapters = {}
    for link in all_links:
        m = re.search(r'/(\d+)\.html', link['href'])
        if m:
            chapter_id = int(m.group(1))
            if chapter_id not in unique_chapters:
                unique_chapters[chapter_id] = link

    sorted_chapter_ids = sorted(unique_chapters.keys())
    page_text = {}
    total = len(sorted_chapter_ids)
    
    for idx, cid in enumerate(sorted_chapter_ids):
        link = unique_chapters[cid]
        chapter_title = link.string or f"第{idx+1}章"
        print(f"[{idx+1}/{total}] 正在抓取: {chapter_title} (ID: {cid}, 已用时: {timer.format_time(timer.elapsed())})")
        
        url1 = urljoin(url, link['href'])
        soup1 = fetch_page(url1)
        content1 = extract_content(soup1)
        
        time.sleep(random.uniform(0.3, 0.7))
        
        url2 = url1.replace('.html', '_2.html')
        soup2 = fetch_page(url2)
        content2 = extract_content(soup2)
        
        page_text[cid] = f"\n{chapter_title}\n" + content1 + content2
        anti_crawling_pause()

    save_to_file(meta['title'], meta['author'], page_text, timer=timer)

if __name__ == "__main__":
    main()
