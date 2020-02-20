#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymysql
import time
import telegram
import pandas as pd
import datetime
from pandas import DataFrame
import re
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup
from telepot.delegate import pave_event_space, per_chat_id, create_open
from bank_parameter import *
#-340019778   -364811652


# In[ ]:


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if str(chat_id) == tele_chatid :
        listtext=['目录','银行总类','查询','建行','工行','招行']
        checkbanktext=['中国工商银行','中国银行','中国农业银行','中国建设银行','中国招商银行','中国光大银行','中国民生银行','交通银行','中信银行','华夏银行','兴业银行','浦发银行','北京银行','天津农商银行','内蒙古银行'     ] 
        totaltext=['清单','近日','数据']
        
        if any(re.findall('|'.join(listtext), msg['text'])):
            bot.sendMessage(chat_id=tele_chatid ,text= "[可查询银行] : '中国工商银行','中国银行','中国农业银行','中国建设银行','中国招商银行','中国光大银行','中国民生银行','交通银行','中信银行','华夏银行','兴业银行','浦发银行','北京银行','天津农商银行','内蒙古银行' " )            
        elif any(re.findall('|'.join(checkbanktext), msg['text'])):
            select_sql(msg['text'])
        elif any(re.findall('|'.join(totaltext), msg['text'])):
            list_sql()
        else:
            bot.sendMessage(chat_id=tele_chatid,text="听不太懂您说的请看功能\n\n银行公告系统会通知维修日期也可以查询各银行维修时间和30天内维修公告\n\n可查询清单：关键字-目录\n可查询银行：关键字-银行名称\n可查询近况：关键字-清单")

def select_sql(bank):
    db = pymysql.Connect(host=db_host,user=db_user,passwd=db_passwd,port=db_port,database=db_database ,charset = 'utf8')
    df = pd.read_sql("select * from "+db_table2+" where bank='"+bank+"' order by id desc limit 1", con=db)
    value1=df.iloc[0, 5]
    value2=df.iloc[0, 6]
    value3=df.iloc[0, 7]
    value4=df.iloc[0, 3]     #(datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')  #时间加8小时 +datetime.timedelta(hours=8)
    bot.sendMessage(chat_id=tele_chatid,text= '[银行名称] : '+value1+ "\n" +'[标题公告] : '+ value2 + "\n" +'[重要讯息] : '+value3+ "\n"+'[讯息网址] : ' +value4)

def list_sql():
    today = datetime.date.today()
    beforeday = today + datetime.timedelta(days=-30)
    db = pymysql.Connect(host=db_host,user=db_user,passwd=db_passwd,port=db_port,database=db_database ,charset = 'utf8')
    df = pd.read_sql("select postdate,bank,title,notes,url from "+db_table2+" where postdate  BETWEEN STR_TO_DATE('"+str(beforeday)+"','%Y-%m-%d') AND STR_TO_DATE('"+str(today)+"','%Y-%m-%d')", con=db)
    if len(df)>0:
        data30=[]
        for i in range(len(df)):
            datashow=df.iloc[i, 0]+": "+df.iloc[i, 1]+"-"+df.iloc[i, 2]+"-"+df.iloc[i, 3]+"-"+df.iloc[i, 4]+" "+"\n"+" "+"\n"
            data30.append(datashow)
        bot.sendMessage(chat_id=tele_chatid,text='[最近30天内发布消息]'+"\n"+"\n"+  "".join(data30))
    
# 给出回硬
bot = telepot.Bot(token=tele_token)
MessageLoop(bot,handle).run_as_thread()
# Keep the program running.
time.sleep(3600)


# In[ ]:




