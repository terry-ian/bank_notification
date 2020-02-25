#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import re
import datetime as dt
from datetime import datetime
import pymysql
from urllib.parse import unquote
import pandas as pd
import time
import random
from bank_mysql_function import *
#反爬虫用 模拟使用者
send_headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
 "Connection": "close",
 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
 "Accept-Language": "zh-CN,zh;q=0.8" }
#random.choice(user_agent_list)


# In[2]:


def getNewsDetail(notice,domainname,item,bankname):
    result={}
    title=notice[item].find('span',{"class": "li_left"}).text.split()[0]
    time=notice[item].find('span',{"class": "li_right"}).text.split()[0]
    urllink=domainname+notice[item].select("a")[0]["href"]
    
    resarticle=request_retry(urllink ,send_headers)
    resarticle.encoding='utf-8'
    souparticle=BeautifulSoup(resarticle.text,'html.parser')
    try:
        allcontent = " ".join(souparticle.find('div', {"id": "con"}).text.split())  
        if len(allcontent)==0 :allcontent="请查询详细内文"  
    except: 
        allcontent ="请查询详细内文"

    result['bank']=bankname
    result['title']=title
    result['time']=time.replace("/", "-").replace("]", "")
    result['urllink']=unquote(urllink,encoding="utf-8")
    result['allcontent']=allcontent

    return(result)


# In[3]:


#数据抓取
res=request_retry("http://www.bankofbeijing.com.cn/about/gonggao.html" ,send_headers) 
res.encoding='utf-8'
soup=BeautifulSoup(res.text,'html.parser')
domainname="http://www.bankofbeijing.com.cn"
notice=soup.find('ul',{"class": "sub_news"}).findAll('li')
noticelen = len(notice)

alldata=[]
for i in range(noticelen):
    datanews=getNewsDetail(notice,domainname,i,"北京银行")
    alldata.append(datanews)
    time.sleep(2)

#存取原始数据
rowdata_db(alldata,noticelen,"北京银行")
#存取警示数据
notification_db(alldata,noticelen,"北京银行")


# In[ ]:




