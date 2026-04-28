import sys
import re
from urllib.parse import urljoin
from crawl_utils import fetch_page, get_meta_info, anti_crawling_pause, save_to_file, Timer

def extract_content(soup):
    """256文学特有的内容提取逻辑"""
    if not soup: return ""
    paragraphs = soup.find_all('p', href=False)[:-2]
    text = '\n'.join([p.string for p in paragraphs if p.string])
    return text

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 novel_256.py [URL]")
        return

    url = sys.argv[1]
    # 提取书籍 ID，例如 https://www.256wx.org/read/182834/ -> 182834
    book_id_match = re.search(r'/read/(\d+)/', url)
    if not book_id_match:
        print("无法识别书籍 ID")
        return
    book_id = book_id_match.group(1)

    timer = Timer()
    soup = fetch_page(url)
    meta = get_meta_info(soup)
    print(f"开始抓取: {meta['title']} - {meta['author']}")

    # 仅匹配当前 book_id 下的章节链接，过滤推荐书籍
    links = soup.find_all('a', href=re.compile(f'/read/{book_id}/\\d+\\.html'))
    
    page_text = {}
    total = len(links)
    for idx, link in enumerate(links):
        chapter_title = link.string or f"第{idx+1}章"
        print(f"[{idx+1}/{total}] 正在抓取: {chapter_title} (已用时: {timer.format_time(timer.elapsed())})")
        
        chapter_url = urljoin(url, link['href'])
        chapter_soup = fetch_page(chapter_url)
        if chapter_soup:
            page_text[idx] = f"\n{chapter_title}\n" + extract_content(chapter_soup)
        
        anti_crawling_pause()

    save_to_file(meta['title'], meta['author'], page_text, timer=timer)

if __name__ == "__main__":
    main()
