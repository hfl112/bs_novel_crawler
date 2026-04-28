import sys
import re
from urllib.parse import urljoin
from crawl_utils import fetch_page, get_meta_info, anti_crawling_pause, save_to_file, Timer

def extract_content(soup):
    """52书库特有的内容提取逻辑"""
    if not soup: return ""
    for tag in soup.find_all(["a", "span"]):
        tag.extract()
    paragraphs = soup.find_all('p')[:-1]
    text = '\n'.join([p.string for p in paragraphs if p.string])
    text = text.replace('\u3000','\n').replace('\u200c','')
    
    # 清理各种版本的 52书库 广告语
    noise_list = [
        'Tips:看好看的小说，就来52书库呀~www.52shuku.vip',
        '小贴士:找看好看得小说，就来52书库呀~www.52shuku.net',
        '小贴士:找看好看得小说，就来52书库呀~www.52shuku.vip'
    ]
    for noise in noise_list:
        text = text.replace(noise, '')
    
    return text

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 novel_52.py [URL]")
        return

    timer = Timer()
    url = sys.argv[1]
    soup = fetch_page(url)
    meta = get_meta_info(soup)
    print(f"开始抓取: {meta['title']} - {meta['author']}")

    links = soup.find_all('a', href=re.compile(r'.*_\d+.html'), class_=False)
    page_text = {}
    total = len(links)
    for idx, link in enumerate(links):
        try:
            page_num = int(link.string[1:-1])
        except:
            page_num = idx + 1
            
        print(f"[{idx+1}/{total}] 正在抓取第 {page_num} 页... (已用时: {timer.format_time(timer.elapsed())})")
        page_url = urljoin(url, link['href'])
        page_soup = fetch_page(page_url)
        if page_soup:
            page_text[page_num] = extract_content(page_soup)
        
        anti_crawling_pause()

    save_to_file(meta['title'], meta['author'], page_text, timer=timer)

if __name__ == "__main__":
    main()
