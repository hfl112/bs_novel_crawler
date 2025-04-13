#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


#add header
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'MyApp/1.0')]
urllib.request.install_opener(opener)


# In[3]:


def read_page(url):
    webpage = urllib.request.urlopen(url).read()
    page = BeautifulSoup(webpage, 'lxml')     #"html.parser"
    return page


# In[4]:


def get_page_info_st(page):
    for table in page.find_all("a"):
        table.extract()
    for table in page.find_all("span"):
        table.extract()
    page_txt = page.find_all('p')[:-1]
    text = ''
    for i in page_txt:
        if i.string :
            text = text+i.string
    text = text.replace('\u3000','\n').replace('\u200c','')
    return text


# In[7]:


#url = 'https://www.52shuku.vip/gl/hyxV.html'
url = sys.argv[1]
page = read_page(url)

info = page.head
body = page.body 


# In[8]:


book_name = info.title.string.replace('【',':').replace('_',':').split(':')[0]
author = info.title.string.replace('【',':').replace('_',':').split(':')[1]
print(book_name, author)


# In[ ]:


links = body.find_all('a', href=re.compile(r'.*_\d+.html'), class_=False)
page_text = {}
for i in links:
    page_number = int(i.string[1:-1])
    
    page_url = i['href']
    page_bs = read_page(page_url)
    txt = get_page_info_st(page_bs)
    
    page_text[page_number] = txt


# In[ ]:


replace_character = {'Tips:看好看的小说，就来52书库呀~www.52shuku.vip':''}
with open('/Users/funanhe/Downloads/'+book_name+'-'+author+'.txt', "w") as f:
    for i in range(1, len(page_text.keys()) + 1):
        print(i)
        
        new_text = page_text[i]
        for key in replace_character.keys():
            new_text = new_text.replace(key, replace_character[key])
        f.write(new_text)


# In[ ]:




