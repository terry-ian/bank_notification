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
#反爬虫用 模拟使用者
send_headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
 "Connection": "keep-alive",
 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
 "Accept-Language": "zh-CN,zh;q=0.8" }


# In[2]:


def sql_webcrawler(url,postdate,bank,title,content):
    db = pymysql.Connect(host="remotemysql.com",user="giaX9JoXo3",passwd="VEm7Ky6FIB",port=3306,database="giaX9JoXo3",charset = 'utf8')
    cursor = db.cursor() # 创建一个游标对象
    # 插入语句
    sql = "INSERT INTO webcrawler_bank(url,postdate,bank,title,content) "  "VALUES ('%s','%s','%s','%s','%s')" % (url,postdate,bank,title,content)
    try:
        cursor.execute(sql)  # 执行 SQL 插入语句
    except:
        db.rollback()  # 如果发生错误则回滚
    db.commit() # 提交到数据库执行
    cursor.close() #关闭游标
    db.close() #关闭连接
    
def sql_notification(bank,title,notes,url,status):
    db = pymysql.Connect(host="remotemysql.com",user="giaX9JoXo3",passwd="VEm7Ky6FIB",port=3306,database="giaX9JoXo3",charset = 'utf8')
    cursor = db.cursor() # 创建一个游标对象
    # 插入语句
    sql = "INSERT INTO notification_bank(bank,title,notes,url,status) "  "VALUES ('%s','%s','%s','%s','%s')" % (bank,title,notes,url,status)
    try:
        cursor.execute(sql)  # 执行 SQL 插入语句
    except:
        db.rollback()  # 如果发生错误则回滚
    db.commit() # 提交到数据库执行
    cursor.close() #关闭游标
    db.close() #关闭连接

def select_sql(sqlcontent):
    db = pymysql.Connect(host="remotemysql.com",user="giaX9JoXo3",passwd="VEm7Ky6FIB",port=3306,database="giaX9JoXo3",charset = 'utf8')
    sql_select = sqlcontent
    df = pd.read_sql(sql_select, con=db)
    return(df)


# In[3]:


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
    except: 
        allcontent ="请洽内文"
 
    result['bank']=bankname
    result['title']=title
    result['time']=time  #.replace("[", "").replace("]", "")
    result['urllink']=unquote(urllink,encoding="utf-8")
    result['allcontent']=allcontent

    return(result)


# In[4]:


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


# In[5]:


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
            warningdata['notes']=noticetext if len(noticetext) != 0 else "请查询详细内文"
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


# In[6]:


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

#處理被放置頂文章
for j in range(noticelen):
    if(datetime.strptime(dt.date.today().strftime("%Y-%m-%d") , "%Y-%m-%d")-datetime.strptime(alldata[j]['time'], "%Y-%m-%d")).days < 10:
        break
if j!=0:
    del alldata[0:j]
    noticelen=noticelen-j

#存取原始数据
rowdata_db(alldata,noticelen,"中信银行")
#存取警示数据
notification_db(alldata,noticelen,"中信银行")


# In[ ]:




