#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

# In[ ]:


#add header
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'MyApp/1.0')]
urllib.request.install_opener(opener)


# In[ ]:


def read_page(url):
    webpage = urllib.request.urlopen(url).read()
    page = BeautifulSoup(webpage, 'lxml')     #"html.parser"
    return page


# In[ ]:


url = sys.argv[1]
main_web = 'https://www.256wx.net/'
page = read_page(url)

info = page.head
body = page.body 


# In[ ]:


book_name = info.find_all('title')[0].string.split('_')[0]
author = info.find_all('title')[0].string.split('_')[1]
print(book_name, author) 


# In[ ]:


def get_page_info_256(page):
    a = page_bs.find_all('p', href = False)[:-2]
    text = ''
    for i in a:
        if i.string :
            text = text+'\n'+i.string
    return text


# In[ ]:


links = body.find_all('a', href=re.compile(r'\d+\.html'))
page_text = {}
for i in links:
    if '第' in i.string:

        page_number = int(i.string[1:-1])

        page_url = i['href']
        page_bs = read_page(main_web + page_url)
        txt = get_page_info_256(page_bs)

        page_text[page_number] = txt


# In[ ]:


with open('~/Downloads/'+book_name+'-'+author+'.txt', "w") as f:
    for i in range(1, len(page_text.keys()) + 1):
        print(i)
        new_text = page_text[i]
        f.write(new_text)

