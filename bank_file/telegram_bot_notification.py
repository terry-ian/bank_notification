#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pymysql
import time
import telegram
import pandas as pd
import datetime
from pandas import DataFrame
import telepot
from telepot.loop import MessageLoop
from bank_parameter import *
#-340019778   -364811652


# In[6]:


#while True:
#资料库 连线设定   #查詢目前數據庫中有無訊息要更新
db = pymysql.Connect(host=db_host,user=db_user,passwd=db_passwd,port=db_port,database=db_database ,charset = 'utf8')
sql_select = "select * from "+db_table2+" where status=0"
df = pd.read_sql(sql_select, con=db)
#目前有多少数据未完成传送
tasknumber=len(df)
if tasknumber == 0 :
    time.sleep(5)
elif tasknumber > 15:
    for i in range(tasknumber): 
        my_cousor = db.cursor()   
        my_cousor.execute( "UPDATE "+db_table2+" SET status = 1  WHERE id = " + str(df.iloc[i, 0]) )
        db.commit()
        my_cousor.close() #关闭游标
else :
    for i in range(tasknumber): 
        #传送至 telegram 群内
        bot = telepot.Bot(token=tele_token)
        value1=df.iloc[i, 5]
        value2=df.iloc[i, 6]
        value3=df.iloc[i, 7]
        value4=df.iloc[i, 3] #(datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')  #时间加8小时 +datetime.timedelta(hours=8)
        bot.sendMessage(chat_id=tele_chatid,text='★   最新公告   ★'  + "\n" + '[银行名称] : '+value1+ "\n" +'[标题公告] : '+ value2 + "\n" +'[重要讯息] : '+value3+ "\n"+'[讯息网址] : ' +value4)
        my_cousor = db.cursor()   
        my_cousor.execute( "UPDATE "+db_table2+" SET status = 1  WHERE id = " + str(df.iloc[i, 0]) )
        db.commit()
        my_cousor.close() #关闭游标
        if i%10 == 5 : time.sleep(20)        
db.close()    #关闭连接


# In[ ]:




