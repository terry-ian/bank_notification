#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import telepot
import time
from bank_parameter import *

#各排程执行
def telebot_send_error(bank_name):
    bot = telepot.Bot(token=tele_warning_token)
    bot.sendMessage(chat_id=tele_warning_chatid ,text= bank_name+'-程序执行有误请查看日志')
#完成今日爬虫作业
def telebot_finish():
    timenow=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    bot = telepot.Bot(token=tele_warning_token)
    bot.sendMessage(chat_id=tele_warning_chatid ,text= timenow+' - 银行爬虫作业完成')


# In[2]:


#中国农业银行
ret=os.system("python3 ./bank_proclamation/bank_file/bank_maintenance_notifications-ABOC.py > ./bank_proclamation/bank_log/ABOC.log 2>&1")
if ret!=0 : telebot_send_error('中国农业银行')


# In[3]:


#交通银行
ret=os.system("python3 ./bank_proclamation/bank_file/bank_maintenance_notifications-BCM.py > ./bank_proclamation/bank_log/BCM.log 2>&1")
if ret!=0 : telebot_send_error('交通银行')


# In[4]:


#北京银行
ret=os.system("python3 ./bank_proclamation/bank_file/bank_maintenance_notifications-BOB.py > ./bank_proclamation/bank_log/BOB.log 2>&1")
if ret!=0 : telebot_send_error('北京银行')


# In[5]:


#中国银行
ret=os.system("python3 ./bank_proclamation/bank_file/bank_maintenance_notifications-BOC.py > ./bank_proclamation/bank_log/BOC.log 2>&1")
if ret!=0 : telebot_send_error('中国银行')


# In[6]:


#内蒙古银行
ret=os.system("python3 ./bank_proclamation/bank_file/bank_maintenance_notifications-BOIM.py > ./bank_proclamation/bank_log/BOIM.log 2>&1")
if ret!=0 : telebot_send_error('内蒙古银行')


# In[7]:


#中国建设银行
ret=os.system("python3 ./bank_proclamation/bank_file/bank_maintenance_notifications-CCB.py > ./bank_proclamation/bank_log/CCB.log 2>&1")
if ret!=0 : telebot_send_error('中国建设银行')


# In[27]:


#中国光大银行
ret=os.system("python3 ./bank_proclamation/bank_file/bank_maintenance_notifications-CEB.py > ./bank_proclamation/bank_log/CEB.log 2>&1")
if ret!=0 : telebot_send_error('中国光大银行')


# In[9]:


#中信银行
ret=os.system("python3 ./bank_proclamation/bank_file/bank_maintenance_notifications-CITIC.py > ./bank_proclamation/bank_log/CITIC.log 2>&1")
if ret!=0 : telebot_send_error('中信银行')


# In[10]:


#中国招商银行
ret=os.system("python3 ./bank_proclamation/bank_file/bank_maintenance_notifications-CMB.py > ./bank_proclamation/bank_log/CMB.log 2>&1")
if ret!=0 : telebot_send_error('中国招商银行')


# In[11]:


#中国民生银行
ret=os.system("python3 ./bank_proclamation/bank_file/bank_maintenance_notifications-CMBC.py > ./bank_proclamation/bank_log/CMBC.log 2>&1")
if ret!=0 : telebot_send_error('中国民生银行')


# In[12]:


#华夏银行
ret=os.system("python3 ./bank_proclamation/bank_file/bank_maintenance_notifications-HB.py > ./bank_proclamation/bank_log/HB.log 2>&1")
if ret!=0 : telebot_send_error('华夏银行')


# In[13]:


#兴业银行
ret=os.system("python3 ./bank_proclamation/bank_file/bank_maintenance_notifications-IB.py > ./bank_proclamation/bank_log/IB.log 2>&1")
if ret!=0 : telebot_send_error('兴业银行')


# In[14]:


#中国工商银行
ret=os.system("python3 ./bank_proclamation/bank_file/bank_maintenance_notifications-ICBC.py > ./bank_proclamation/bank_log/ICBC.log 2>&1")
if ret!=0 : telebot_send_error('中国工商银行')


# In[15]:


#天津农商行
ret=os.system("python3 ./bank_proclamation/bank_file/bank_maintenance_notifications-TRCB.py > ./bank_proclamation/bank_log/TRCB.log 2>&1")
if ret!=0 : telebot_send_error('天津农商行')


# In[11]:


#浦发银行
ret=os.system("python3 ./bank_proclamation/bank_file/bank_maintenance_notifications-SPDB.py > ./bank_proclamation/bank_log/SPDB.log 2>&1")
if ret!=0 : telebot_send_error('浦发银行')


# In[8]:


#telegram 传送警示讯息
ret=os.system("python3 ./bank_proclamation/bank_file/telegram_bot_notification.py > ./bank_proclamation/bank_log/telegram_bot.log 2>&1")
if ret!=0 : telebot_send_error('Telegram警示')


# In[6]:


#爬虫完成送出通知
telebot_finish()


# In[ ]:




