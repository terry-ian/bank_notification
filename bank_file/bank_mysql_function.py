#!/usr/bin/env python
# coding: utf-8
import pymysql
import pandas as pd
import re
from bank_parameter import *

#sql写入rowdata表格中语句
def sql_webcrawler(url,postdate,bank,title,content):
    db = pymysql.Connect(host=db_host,user=db_user,passwd=db_passwd,port=db_port,database=db_database,charset = 'utf8')
    cursor = db.cursor() # 创建一个游标对象
    # 插入语句
    sql = "INSERT INTO bank_webcrawler(url,postdate,bank,title,content) "  "VALUES ('%s','%s','%s','%s','%s')" % (url,postdate,bank,title,content)
    try:
        cursor.execute(sql)  # 执行 SQL 插入语句
    except:
        db.rollback()  # 如果发生错误则回滚
    db.commit() # 提交到数据库执行
    cursor.close() #关闭游标
    db.close() #关闭连接

#sql写入警示表格中语句	
def sql_notification(bank,title,notes,url,status):
    db = pymysql.Connect(host=db_host,user=db_user,passwd=db_passwd,port=db_port,database=db_database,charset = 'utf8')
    cursor = db.cursor() # 创建一个游标对象
    # 插入语句
    sql = "INSERT INTO bank_notification(bank,title,notes,url,status) "  "VALUES ('%s','%s','%s','%s','%s')" % (bank,title,notes,url,status)
    try:
        cursor.execute(sql)  # 执行 SQL 插入语句
    except:
        db.rollback()  # 如果发生错误则回滚
    db.commit() # 提交到数据库执行
    cursor.close() #关闭游标
    db.close() #关闭连接

#sql查询语句	
def sql_select(sqlcontent):
    db = pymysql.Connect(host=db_host,user=db_user,passwd=db_passwd,port=db_port,database=db_database,charset = 'utf8')
    sql_text = sqlcontent
    df = pd.read_sql(sql_text, con=db)   
    return(df)
	
#检查有无重复资料写入rowdata表
def rowdata_db(alldata,noticelen,bankname):
    #检查数据表中有无重复资料和写入原始资料库中
    for i in reversed(range(noticelen)):
        lastdata=sql_select("""select url from bank_webcrawler where bank='"""+bankname+"""'  and url ='"""+alldata[i]["urllink"]+"""' """)
        if len(lastdata) ==0:
            sql_webcrawler(alldata[i]["urllink"],alldata[i]["time"],alldata[i]["bank"],alldata[i]["title"],alldata[i]["allcontent"])

#检查有无重复资料写入警示表
def notification_db(alldata,noticelen,bankname):
    #文字处理
    allwarningdata=[]
    checktitletext=["维护","暂停","升级"] ; checkcontenttext=["将于","约于","定于","计划于","将在","具体时间为","拟于"] #title 关键字 ,content 关键字
    for check in range(noticelen):
        if any(re.findall('|'.join(checktitletext), alldata[check]['title'])):
            warningdata={}
            if len(re.findall('|'.join(checkcontenttext), alldata[check]['allcontent'])) == 0:
                noticetext="请查询详细内文"
            else:
                stoptime=alldata[check]['allcontent'].find( re.findall('|'.join(checkcontenttext), alldata[check]['allcontent'])[0] )
                noticetext=alldata[check]['allcontent'][stoptime:stoptime+50].split("。" )[0] if len(alldata[check]['allcontent'][stoptime:stoptime+50].split("。" )[0]) < len(alldata[check]['allcontent'][stoptime:stoptime+50].split("，" )[0]) else alldata[check]['allcontent'][stoptime:stoptime+50].split("，" )[0] 
            warningdata['bank']=bankname
            warningdata['title']=alldata[check]['title']
            warningdata['notes']=noticetext
            warningdata['url']=alldata[check]['urllink']
            allwarningdata.append(warningdata)
    
    allwarningdatalen=len(allwarningdata)
    #检查数据表中有无重复资料和写入原始资料库中
    for i in reversed(range(allwarningdatalen)):
        lastdatawarning=sql_select("""select url from bank_notification where bank='"""+bankname+"""' and url ='"""+allwarningdata[i]["url"]+"""' """)
        if len(lastdatawarning) ==0:
            sql_notification(allwarningdata[i]['bank'],allwarningdata[i]['title'],allwarningdata[i]['notes'],allwarningdata[i]['url'],0)

