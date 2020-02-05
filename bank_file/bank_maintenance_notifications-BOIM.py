#!/usr/bin/env python
# coding: utf-8

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
from bank_mysql_function import *    #sql帳密更改

#反爬虫用 模拟使用者
send_headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
 "Connection": "keep-alive",
 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
 "Accept-Language": "zh-CN,zh;q=0.8" }
#random.choice(user_agent_list)


def getNewsDetail(notice,domainname,item,bankname):
    result={}
    title=notice[item].find('span',{"class": "fl"}).text.split()[0]
    time=notice[item].find('span',{"class": "fr"}).text.split()[0]
    urllink=domainname+notice[item].select("a")[0]["href"]

    resarticle=requests.get(urllink ,timeout = 1000  ,headers=send_headers)
    resarticle.encoding='utf-8'
    souparticle=BeautifulSoup(resarticle.text,'html.parser')
    try:
        allcontent = " ".join(souparticle.find('div', {"class": "m2rcb"}).text.split())  
        if len(allcontent)==0 :allcontent="请查询详细内文"  
    except: 
        allcontent ="请查询详细内文"

    result['bank']=bankname
    result['title']=title
    result['time']=time.replace("/", "-").replace("]", "")
    result['urllink']=unquote(urllink,encoding="utf-8")
    result['allcontent']=allcontent

    return(result)


# In[23]:


def rowdata_db(alldata,noticelen,bankname):
    #检查数据表中有无重复资料和写入原始资料库中
    lastdata=select_sql("""select url from webcrawler_bank where bank='"""+bankname+"""' order by id desc limit 1 """)
    #无data时需要写入全部资料
    if len(lastdata)==0:
        for i in reversed(range(noticelen)):
            sql_webcrawler(alldata[i]["urllink"],alldata[i]["time"],alldata[i]["bank"],alldata[i]["title"],alldata[i]["allcontent"])
    else:
        for j in range(noticelen):
            #判断有无新资料写入
            if alldata[j]['urllink'].find(lastdata.iloc[0,0])==0:
                for i in reversed(range(j)):
                    sql_webcrawler(alldata[i]["urllink"],alldata[i]["time"],alldata[i]["bank"],alldata[i]["title"],alldata[i]["allcontent"])


# In[24]:


def notification_db(alldata,noticelen,bankname):
    #文字处理
    allwarningdata=[]
    checktitletext=["维护","暂停","升级"] ; checkcontenttext=["将于","将在"] #目前限定两种
    for check in range(noticelen):
        if any(re.findall('|'.join(checktitletext), alldata[check]['title'])):
            warningdata={}
            stoptime=alldata[check]['allcontent'].find(checkcontenttext[0]) if alldata[check]['allcontent'].find(checkcontenttext[0])>alldata[check]['allcontent'].find(checkcontenttext[1]) else alldata[check]['allcontent'].find(checkcontenttext[1])
            noticetext=alldata[check]['allcontent'][stoptime:stoptime+50].split("。" )[0] if len(alldata[check]['allcontent'][stoptime:stoptime+50].split("。" )[0]) < len(alldata[check]['allcontent'][stoptime:stoptime+50].split("，" )[0]) else alldata[check]['allcontent'][stoptime:stoptime+50].split("，" )[0] 
            warningdata['bank']=bankname
            warningdata['title']=alldata[check]['title']
            warningdata['notes']=noticetext if len(noticetext) >1 else "请查询详细内文"
            warningdata['url']=alldata[check]['urllink']
            allwarningdata.append(warningdata)
    #检查数据表中有无重复资料和写入维修数据表
    lastdatawarning=select_sql("""select url from notification_bank where bank='"""+bankname+"""' order by id desc limit 1 """)
    if len(lastdatawarning)==0:
        for i in reversed(range(len(allwarningdata))):
            sql_notification(allwarningdata[i]['bank'],allwarningdata[i]['title'],allwarningdata[i]['notes'],allwarningdata[i]['url'],0)
    else:
        for j in range(len(allwarningdata)):
            if allwarningdata[j]['url'].find(lastdatawarning.iloc[0,0])==0:
                for i in reversed(range(j)):
                    sql_notification(allwarningdata[i]['bank'],allwarningdata[i]['title'],allwarningdata[i]['notes'],allwarningdata[i]['url'],0)


# In[ ]:


#数据抓取
res=requests.get("http://www.boimc.com/homepage/notice/" ,timeout = 1000  ,headers=send_headers , verify=False) 
res.encoding = "utf-8"
soup=BeautifulSoup(res.text,'html.parser')
domainname="http://www.boimc.com"
notice=soup.find('div',{"class": "auto m5list"}).findAll('li')
noticelen = len(notice)

alldata=[]
for i in range(noticelen):
    datanews=getNewsDetail(notice,domainname,i,"内蒙古银行")
    alldata.append(datanews)
    time.sleep(2)

#存取原始数据
rowdata_db(alldata,noticelen,"内蒙古银行")
#存取警示数据
notification_db(alldata,noticelen,"内蒙古银行")


# In[ ]:




