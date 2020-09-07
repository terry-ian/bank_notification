#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import re
import datetime
import datetime as dt
from datetime import datetime
import pymysql
from urllib.parse import unquote
import pandas as pd
import time
from bank_mysql_function import *
#反爬虫用 模拟使用者
send_headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
 "Connection": "keep-alive",
 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
 "Accept-Language": "zh-CN,zh;q=0.8" }


# In[2]:


def getNewsDetail(notice,domainname,item,bankname):
    result={}
    title=notice[item].select("a")[0].text.split()[0]
    time=notice[item].find("span").text
    urllink=domainname+notice[item].select("a")[0]["href"]
    
    resarticle=request_retry(urllink ,send_headers)
    resarticle.encoding='utf-8'
    souparticle=BeautifulSoup(resarticle.text,'html.parser')
    try:
        allcontent = " ".join(souparticle.find('div', {"class": "show_main c_content"}).text.split())
    except: 
        allcontent ="请查询详细内文"

    result['bank']=bankname
    result['title']=title
    result['time']=time.replace("[", "").replace("]", "")
    result['urllink']=unquote(urllink,encoding="utf-8")
    result['allcontent']=allcontent

    return(result)


# In[3]:


#数据抓取
res=request_retry("http://www.bankcomm.com/BankCommSite/shtml/jyjr/cn/7158/7825/list_1.shtml?channelId=7158" ,send_headers) 
res.encoding='utf-8'
soup=BeautifulSoup(res.text,'html.parser')
domainname="http://www.bankcomm.com"
notice=soup.find('ul',{"class": "tzzgx-conter ty-list"}).findAll("li")
noticelen = len(notice)

alldata=[]
for i in range(noticelen):
    try:
        datanews=getNewsDetail(notice,domainname,i,"交通银行")
    except: 
        continue
    alldata.append(datanews)
    time.sleep(2)

noticelen=len(alldata)
    
#存取原始数据
rowdata_db(alldata,noticelen,"交通银行")
#存取警示数据
notification_db(alldata,noticelen,"交通银行")


# In[ ]:




