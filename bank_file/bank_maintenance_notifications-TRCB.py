#!/usr/bin/env python
# coding: utf-8

# In[17]:


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

# 增加重连次数
requests.adapters.DEFAULT_RETRIES = 5  
#反爬虫用 模拟使用者
send_headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
 "Connection": "close" 
}
#random.choice(user_agent_list)


# In[18]:


def get_html(url,retry=5):
    try:
        resarticle = requests.get(url=url,headers=send_headers,timeout=1000)
    except Exception as e:
        if retry > 0:
            get_html(url,retry-1)
    else:
        resarticle.encoding = 'gbk'
        page_text = resarticle.text
        return page_text


# In[19]:


def getNewsDetail(notice,domainname,item,bankname):
    result={}
    title=notice[item].find('a').text.split()[0]
    time=notice[item].find('font').text.split()[0]
    urllink=notice[item].select("a")[0]["href"]
    
    resarticletext=get_html(urllink)
    souparticle=BeautifulSoup(resarticletext,'html.parser')
    try:
        allcontent = " ".join(souparticle.find('div', {"class": "newscontent"}).text.split())  
        if len(allcontent)==0 :allcontent="请查询详细内文"  
    except: 
        allcontent ="请查询详细内文"

    result['bank']=bankname
    result['title']=title
    result['time']=time.replace("/", "-").replace("]", "")
    result['urllink']=unquote(urllink,encoding="utf-8")
    result['allcontent']=allcontent

    return(result)


# In[16]:


#数据抓取
res=requests.get("http://www.trcbank.com.cn/class/cpxw/index.htm" ,timeout = 1000  ,headers=send_headers , verify=False) 
res.encoding = "gbk"
soup=BeautifulSoup(res.content,'html.parser')
domainname="http://www.trcbank.com.cn/Class/cpxw/"
notice=soup.findAll('td',{"colspan": "2"}) 
noticelen = len(notice)

alldata=[]
for i in range(noticelen):
    datanews=getNewsDetail(notice,domainname,i,"天津农商银行")
    alldata.append(datanews)
    time.sleep(2)

#存取原始数据
rowdata_db(alldata,noticelen,"天津农商银行")
#存取警示数据
notification_db(alldata,noticelen,"天津农商银行")


# In[ ]:




