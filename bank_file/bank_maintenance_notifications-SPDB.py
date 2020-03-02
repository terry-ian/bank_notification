#!/usr/bin/env python
# coding: utf-8

# In[8]:


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
#from selenium.webdriver.chrome.options import Options
from bank_mysql_function import *    #sql帳密更改
from fake_useragent import UserAgent

#反爬虫用 模拟使用者
ua = UserAgent() 


# In[9]:


def getNewsDetail(notice,domainname,item,bankname):
    result={}
    title=notice[item].find('a').text.split()[0]
    time=notice[item].find('span',{"class": "c_date"}).text.split()[0]
    urllink=notice[item].select("a")[0]["href"]
    
    if urllink.find("pdf") > 0 :
        souparticle = None
    else :
        browser.get(urllink)
        browser.implicitly_wait(20)
        souparticle = BeautifulSoup(browser.page_source, "html.parser")
    try:
        allcontent = " ".join(souparticle.find('div', {"class": "TRS_Editor"}).text.split())
        if len(allcontent)==0 :allcontent="请查询详细内文"  
    except: 
        allcontent ="请查询详细内文"

    result['bank']=bankname
    result['title']=title
    result['time']=time  #.replace("[", "").replace("]", "")
    result['urllink']=unquote(urllink,encoding="utf-8")
    result['allcontent']=allcontent

    return(result)


# In[10]:


DRIVER_PATH = '/usr/bin/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
chrome_options.add_argument('--headless')                        #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
chrome_options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"')
browser = webdriver.Chrome(executable_path=DRIVER_PATH,options=chrome_options)   #browser.set_page_load_timeout(60)
browser.get('https://www.spdb.com.cn/home/sygg/') 
browser.implicitly_wait(20)
time.sleep(2) 
soup = BeautifulSoup(browser.page_source, "html.parser")
domainname="https://www.spdb.com.cn"
notice=soup.find('div',{"class": "c_news_body common_list"}).findAll('ul')
noticelen = len(notice)

alldata=[]
for i in range(noticelen):
    datanews=getNewsDetail(notice,domainname,i,"浦发银行")
    alldata.append(datanews)
    time.sleep(2)
#关闭捞取数据
browser.close()
browser.quit() 

#存取原始数据
rowdata_db(alldata,noticelen,"浦发银行")
#存取警示数据
notification_db(alldata,noticelen,"浦发银行")


# In[ ]:




