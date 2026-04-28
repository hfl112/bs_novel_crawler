import sys
import re
from urllib.parse import urljoin
from crawl_utils import fetch_page, get_meta_info, anti_crawling_pause, save_to_file, Timer

def extract_content(soup):
    """半夏小说特有的内容提取逻辑"""
    if not soup or not soup.body: return ""
    content_div = soup.body.find('div', id='nr1')
    if not content_div: return ""
    content = content_div.text
    content = content.replace('\n\n\n\n\n\n\n\n本站無彈出廣告，永久域名（ xbanxia.com ）\n', '\n\n')
    content = content.replace('\n\r\n','\n').replace('本站無彈出廣告', '').replace('半夏小說，快樂很多', '')
    return content

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 novel_banxia.py [URL]")
        return

    timer = Timer()
    url = sys.argv[1]
    soup = fetch_page(url)
    meta = get_meta_info(soup)
    print(f"开始抓取: {meta['title']} - {meta['author']}")

    links = soup.find_all('li')
    chapter_links = []
    for li in links:
        a = li.find('a', href=re.compile(r'/books/\d+/\d+\.html'))
        if a: chapter_links.append(a)

    page_text = {}
    total = len(chapter_links)
    for idx, link in enumerate(chapter_links):
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
