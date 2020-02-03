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
#-340019778   -364811652


# In[2]:


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    checkbanktext=['中国工商银行','中国银行','中国农业银行','中国建设银行','中国招商银行','中国光大银行','中国民生银行','交通银行','中信银行','华夏银行','兴业银行','北京银行','天津农商行','内蒙古银行','浦发银行'  ]             
    if any(re.findall('|'.join(checkbanktext), msg['text'])):
        select_sql(msg['text'])
def select_sql(bank):
    db = pymysql.Connect(host="remotemysql.com",user="giaX9JoXo3",passwd="VEm7Ky6FIB",port=3306,database="giaX9JoXo3",charset = 'utf8')
    df = pd.read_sql("select * from notification_bank where bank='"+bank+"' order by id desc limit 1", con=db)
    value1=df.iloc[0, 3]
    value2=df.iloc[0, 4]
    value3=df.iloc[0, 5]
    value4=df.iloc[0, 6]     #(datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')  #时间加8小时 +datetime.timedelta(hours=8)
    bot.sendMessage(chat_id='-364811652',text= '银行名称 : '+value1+ "\n" +'公告 : '+ value2 + "\n" +'重要讯息 : '+value3+ "\n"+'讯息网址 : ' +value4)

# 给出回硬
bot = telepot.Bot(token='1020859504:AAEb-tLbaBjJvJqBsLCzCsStrgTlZNqXRR8')
MessageLoop(bot,handle).run_as_thread()
print ('Listening ...')
# Keep the program running.
while 1:
    time.sleep(10)


# In[ ]:


#mark_up = ReplyKeyboardMarkup(keyboard=[['1则消息'],['2则消息'],['3则消息']], one_time_keyboard=True)
#bot.sendMessage(chat_id='-364811652',text= '请问要选择几则讯息', reply_markup=mark_up)

