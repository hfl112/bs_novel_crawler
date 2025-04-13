#!/usr/bin/env python
# coding: utf-8

# In[205]:


from bs4 import BeautifulSoup
import requests 
import numpy as np
import pandas as pd
import urllib.request
import re
import json
import lxml 
import time 
import sys
import random


# In[207]:


#add header
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')]
urllib.request.install_opener(opener)


# In[216]:


def get_page_info_banxia(page):
    content = page.body.find_all('div', id='nr1', class_=False)[0].text
    content = content.replace('\n\n\n\n\n\n\n\n本站無彈出廣告，永久域名（ xbanxia.com ）\n', '\n\n').replace('\n\r\n','\n')
    return content

def read_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        # 创建带 headers 的 Request 对象
        req = urllib.request.Request(url, headers=headers)
        webpage = urllib.request.urlopen(req).read()
        print(f"{url} - 请求成功")
        return BeautifulSoup(webpage, 'html.parser')
    except Exception as e:
        print(f"请求 {url} 失败: {e}")
        return None
def retry(page_bs):
    return read_page(page_url)


# In[172]:


#url = 'https://www.banxia.cc/books/361578.html'
url = sys.argv[1]
page = read_page(url)
main_web = 'https://www.banxia.cc/'
info = page.head
body = page.body 


# In[173]:


book_name = info.title.string.replace(',',':').split(':')[0]
author = body.find_all('a', href=re.compile(r'author'), class_=False)[0].string
print(book_name, author)


# In[220]:


def retry(page_bs):
    return read_page(page_url)


# In[221]:


page_text = {}
for i in links:    
    page_number = int(re.findall(r'第(\d+)章', i.string)[0])  
    print(page_number)
    page_url = main_web+i['href']
    page_bs = read_page(page_url)
    if page_bs is None or page_bs.body is None:
        print(f"页面 {page_number} 重试...")
        time.sleep(random.uniform(5,10))
        page_bs = retry(page_url)
        if page_bs is None or page_bs.body is None:
            print(f"页面 {page_number} 重试...")
            time.sleep(random.uniform(5,20))
            page_bs = retry(page_url)

    txt = get_page_info_banxia(page_bs)

    page_text[page_number] = txt
    time.sleep(random.uniform(1, 3))
    if page_number % 10 == 0:
        print(f"暂停...")
        time.sleep(random.uniform(3, 15))


# In[222]:


with open('~/Downloads/'+book_name+'-'+author+'.txt', "w") as f:
    for i in range(1, len(page_text.keys()) + 1):
        print(i)        
        new_text = page_text[i]
        f.write(new_text)

