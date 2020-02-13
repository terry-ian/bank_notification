#!/usr/bin/env python
# coding: utf-8

# In[69]:


import requests
from bs4 import BeautifulSoup
import re
import datetime as dt
from datetime import datetime
import pymysql
import pandas as pd
import time
from urllib.parse import unquote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bank_mysql_function import *    #sql帳密更改
#代理
#from fake_useragent import UserAgent
#ua = UserAgent()
#ua.random

#反爬虫用 模拟使用者
send_headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
 "Connection": "keep-alive",
 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
 "Accept-Language": "zh-CN,zh;q=0.8" }


# In[70]:


def getNewsDetail(notice,domainname,item,bankname):
    result={}
    title=notice[item].find('a').text.split()[0]
    time=notice[item].find('span',{"class": "c_date"}).text.split()[0]
    urllink=notice[item].select("a")[0]["href"]
    
    browser.get(urllink)
    browser.implicitly_wait(100)
    souparticle = BeautifulSoup(browser.page_source, "html.parser")
    try:
        allcontent = " ".join(souparticle.find('div', {"class": "TRS_Editor"}).text.split())
    except: 
        allcontent ="请洽内文"

    result['bank']=bankname
    result['title']=title
    result['time']=time  #.replace("[", "").replace("]", "")
    result['urllink']=unquote(urllink,encoding="utf-8")
    result['allcontent']=allcontent

    return(result)


# In[71]:

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.set_page_load_timeout(60)
browser.get('https://www.spdb.com.cn/home/sygg/')  #browser.implicitly_wait(10)
time.sleep(5) 
soup = BeautifulSoup(browser.page_source, "html.parser")
domainname="https://www.spdb.com.cn"
notice=soup.find('div',{"class": "c_news_body common_list"}).findAll('ul')
noticelen = len(notice)

alldata=[]
for i in range(noticelen):
    datanews=getNewsDetail(notice,domainname,i,"浦发银行")
    alldata.append(datanews)
    time.sleep(1)
#关闭捞取数据
#browser.close()
browser.quit() 

#存取原始数据
rowdata_db(alldata,noticelen,"浦发银行")
#存取警示数据
notification_db(alldata,noticelen,"浦发银行")


# In[ ]:




