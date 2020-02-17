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
 "Connection": "close"
}


# In[2]:


def remove_scripts(soup):
    [s.extract() for s in soup('script')]

def getNewsDetail(notice,domainname,item,bankname):
    result={}
    title=notice[item].select("a")[0].text.split()[0]
    time=notice[item].find("span").text
    urllink=domainname+notice[item].select("a")[0]["href"].replace("./", "")
    
    resarticle=requests.get(urllink ,timeout = 1000  ,headers=send_headers)
    resarticle.encoding='utf-8'
    souparticle=BeautifulSoup(resarticle.text,'html.parser')
    try:
        remove_scripts(souparticle)
        allcontent = " ".join(souparticle.find('div', {"class": "main_content"}).text.split())
        if len(allcontent)==0 :allcontent="请查询详细内文" 
    except: 
        allcontent ="请洽内文"
 
    result['bank']=bankname
    result['title']=title
    result['time']=time  #.replace("[", "").replace("]", "")
    result['urllink']=unquote(urllink,encoding="utf-8")
    result['allcontent']=allcontent

    return(result)


# In[ ]:


#数据抓取
res=requests.get("http://www.citicbank.com/common/servicenotice/" ,timeout = 1000  ,headers=send_headers) 
res.encoding='utf-8'
soup=BeautifulSoup(res.text,'html.parser')
domainname="http://www.citicbank.com/common/servicenotice/"
notice=soup.find('ul',{"class": "dhy_b"}).findAll("li")
noticelen = len(notice)

alldata=[]
for i in range(noticelen):
    datanews=getNewsDetail(notice,domainname,i,"中信银行")
    alldata.append(datanews)
    time.sleep(2)

#存取原始数据
rowdata_db(alldata,noticelen,"中信银行")
#存取警示数据
notification_db(alldata,noticelen,"中信银行")


# In[ ]:




