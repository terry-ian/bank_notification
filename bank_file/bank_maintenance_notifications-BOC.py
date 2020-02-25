#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import re
import datetime
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
    title=notice[item].select("a")[0].text
    time=notice[item].select("span")[0].text.replace("[ ", "").replace(" ]", "")
    urllink=domainname+notice[item].select("a")[0]["href"].replace("../../", "").replace("./", "custserv/bi2/")
    
    resarticle=request_retry(urllink ,send_headers)
    resarticle.encoding='utf-8'
    souparticle=BeautifulSoup(resarticle.text,'html.parser')
    allcontent = " ".join(souparticle.find('div', {"class": "TRS_Editor"}).text.split()) if souparticle.find('div', {"class": "TRS_Editor"}) != None else  " ".join(souparticle.find('div', {"class": "sub_con"}).text.split())
    
    result['bank']=bankname
    result['title']=title
    result['time']=time.replace("年", "-").replace("月", "-").replace("日", "")
    result['urllink']=unquote(urllink,encoding="utf-8")
    result['allcontent']=allcontent

    return(result)


# In[4]:


#数据抓取
res=request_retry("https://www.boc.cn/custserv/bi2/" ,send_headers) 
res.encoding='utf-8'
soup=BeautifulSoup(res.text,'html.parser')
domainname="https://www.boc.cn/"
notice=soup.find('div',{"class": "news"}).findAll("li")
noticelen = len(notice)

alldata=[]
for i in range(noticelen):
    datanews=getNewsDetail(notice,domainname,i,"中国银行")
    alldata.append(datanews)
    time.sleep(2)

#存取原始数据
rowdata_db(alldata,noticelen,"中国银行")
#存取警示数据
notification_db(alldata,noticelen,"中国银行")


# In[ ]:




