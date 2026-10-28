import sys
from urllib.parse import urlparse

# 从 parsers 子包导入各站点解析器
from parsers import (
    novel_banxia,
    novel_52,
    novel_256,
    novel_sunzhinan,
    novel_situ
)

def main():
    if len(sys.argv) < 2:
        print("\n[Usage] python3 main.py [URL]")
        print("支持的网站: 半夏小说, 52书库, 256文学, 孙指南/醋溜儿, 思兔网\n")
        return

    url = sys.argv[1].strip()
    domain = urlparse(url).netloc.lower()

    print(f"正在识别网址: {url} ...")

    try:
        if 'banxia' in domain:
            print("检测到: 半夏小说 (parsers.novel_banxia)")
            novel_banxia.main()
            
        elif '52shuku' in domain:
            print("检测到: 52书库 (parsers.novel_52)")
            novel_52.main()
            
        elif '256wx' in domain:
            print("检测到: 256文学 (parsers.novel_256)")
            novel_256.main()
            
        elif 'sunzhinan' in domain or 'culiu' in domain:
            print("检测到: 孙指南/醋溜儿 (parsers.novel_sunzhinan)")
            novel_sunzhinan.main()
            
        elif 'situ' in domain or 'sto' in domain or 'stxs' in domain:
            print("检测到: 思兔网 (parsers.novel_situ)")
            novel_situ.main()
            
        else:
            print(f"抱歉，目前暂不支持该域名: {domain}")
            print("支持的站点包括: 半夏小说 (xbanxia), 52书库 (52shuku), 256文学 (256wx), 孙指南/醋溜儿 (sunzhinan/culiu), 思兔网 (situ/sto)")

    except Exception as e:
        print(f"\n[程序运行出错] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
