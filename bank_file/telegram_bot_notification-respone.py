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
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from bank_parameter import *
#-340019778   -364811652


# In[ ]:


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if chat_id in tele_chatid :
        listtext=['help']
        checkbanktext=['中国工商银行','中国银行','中国农业银行','中国建设银行','中国招商银行','中国光大银行','中国民生银行','交通银行','中信银行','华夏银行','兴业银行','浦发银行','北京银行','天津农商银行','内蒙古银行'     ] 
        totaltext=['近30天银行维修公告']
        telechannel=tele_chatid[tele_chatid.index(chat_id)]
        if any(re.findall('|'.join(listtext), msg['text'])):
            bot.sendMessage(chat_id=telechannel ,text= "银行维修公告系统：\n系统定时通知维修日期也可以查询各银行维修时间和30天内维修公告,如要查询请问安")            
        elif any(re.findall('|'.join(checkbanktext), msg['text'])):
            select_sql(msg['text'],telechannel)
        elif any(re.findall('|'.join(totaltext), msg['text'])):
            list_sql(telechannel)
        else:
            markup = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text='近30天银行维修公告')],
                [KeyboardButton(text='中国工商银行'),KeyboardButton(text='中国银行'),KeyboardButton(text='中国农业银行')],
                [KeyboardButton(text='中国建设银行'),KeyboardButton(text='中国招商银行'),KeyboardButton(text='中国光大银行')],
                [KeyboardButton(text='中国民生银行'),KeyboardButton(text='交通银行'),KeyboardButton(text='中信银行')],
                [KeyboardButton(text='华夏银行'),KeyboardButton(text='兴业银行'),KeyboardButton(text='浦发银行')],
                [KeyboardButton(text='北京银行'),KeyboardButton(text='天津农商银行'),KeyboardButton(text='内蒙古银行')]]
                )
            bot.sendMessage(chat_id=telechannel , text='请点选您要查询功能或银行', reply_markup=markup)
    
def select_sql(bank,telechannel):
    today = datetime.date.today()
    beforeday = today + datetime.timedelta(days=-5)
    db = pymysql.Connect(host=db_host,user=db_user,passwd=db_passwd,port=db_port,database=db_database ,charset = 'utf8')
    try:
        df = pd.read_sql("select * from "+db_table2+" where bank='"+bank+"' and postdate  BETWEEN STR_TO_DATE('"+str(beforeday)+"','%Y-%m-%d') AND STR_TO_DATE('"+str(today)+"','%Y-%m-%d') order by id desc limit 1", con=db)
        bot.sendMessage(chat_id=tele_chatid,text= '[银行名称] : '+df.iloc[0, 5]+ "\n" +'[标题公告] : '+ df.iloc[0, 6] + "\n" +'[重要讯息] : '+df.iloc[0, 7]+ "\n"+'[讯息网址] : ' +df.iloc[0, 3])
    except:
        bot.sendMessage(chat_id=telechannel,text="近期暂时没有维修公告")
    db.close()
    
def list_sql(telechannel):
    today = datetime.date.today()
    beforeday = today + datetime.timedelta(days=-30)
    db = pymysql.Connect(host=db_host,user=db_user,passwd=db_passwd,port=db_port,database=db_database ,charset = 'utf8')
    df = pd.read_sql("select postdate,bank,title,notes,url from "+db_table2+" where postdate  BETWEEN STR_TO_DATE('"+str(beforeday)+"','%Y-%m-%d') AND STR_TO_DATE('"+str(today)+"','%Y-%m-%d') order by postdate desc", con=db)
    if len(df)>0:
        data30=[]
        for i in range(len(df)):
            datashow=str(i+1)+". ["+df.iloc[i, 0]+"] : "+df.iloc[i, 1]+"-"+df.iloc[i, 2]+"-"+df.iloc[i, 3]+"-"+df.iloc[i, 4]+" "+"\n"+" "+"\n"
            data30.append(datashow)
        bot.sendMessage(chat_id=telechannel,text='[最近30天内发布消息]'+"\n"+"\n"+  "".join(data30))
    db.close()
    
# 给出回硬
bot = telepot.Bot(token=tele_token)
MessageLoop(bot,handle).run_as_thread()
# Keep the program running.
time.sleep(3599)


# In[ ]:




