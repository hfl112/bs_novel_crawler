import sys
from urllib.parse import urlparse

def main():
    if len(sys.argv) < 2:
        print("\n[Usage] python3 main.py [URL]")
        print("支持的网站: 半夏小说, 52书库, 256文学, 孙指南/醋溜儿\n")
        return

    url = sys.argv[1].strip()
    domain = urlparse(url).netloc.lower()

    print(f"正在识别网址: {url} ...")

    try:
        if 'banxia' in domain:
            print("检测到: 半夏小说 (novel_banxia.py)")
            import novel_banxia
            novel_banxia.main()
            
        elif '52shuku' in domain:
            print("检测到: 52书库 (novel_52.py)")
            import novel_52
            novel_52.main()
            
        elif '256wx' in domain:
            print("检测到: 256文学 (novel_256.py)")
            import novel_256
            novel_256.main()
            
        elif 'sunzhinan' in domain or 'culiu' in domain:
            print("检测到: 孙指南/醋溜儿 (novel_sunzhinan.py)")
            import novel_sunzhinan
            novel_sunzhinan.main()
            
        else:
            print(f"抱歉，目前暂不支持该域名: {domain}")
            print("你可以尝试直接运行对应的脚本，或者告诉我增加支持。")

    except Exception as e:
        print(f"\n[程序运行出错] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
