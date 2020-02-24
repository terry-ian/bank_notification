#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import telepot
import time
from bank_parameter import *

#執行cmd指令
def run_python_file(cmdtext,bankname,bankcode):
    ret=os.system(cmdtext)
    if ret!=0 : telebot_send_error(bankname,bankcode)
#各排程执行
def telebot_send_error(bank_name,bank_code):
    f = open("./bank_notification/bank_log/"+bank_code+".log", "r")
    bot = telepot.Bot(token=tele_warning_token)
    bot.sendMessage(chat_id=tele_warning_chatid ,text= bank_name+'-程序执行有误log档案如下\n'+ f.read())
#完成今日爬虫作业
def telebot_finish():
    timenow=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    bot = telepot.Bot(token=tele_warning_token)
    bot.sendMessage(chat_id=tele_warning_chatid ,text= timenow+' - 银行爬虫作业完成')


# In[2]:


#中国农业银行
run_python_file("python3 ./bank_notification/bank_file/bank_maintenance_notifications-ABOC.py > ./bank_notification/bank_log/ABOC.log 2>&1" ,'中国农业银行','ABOC' )

#交通银行
run_python_file("python3 ./bank_notification/bank_file/bank_maintenance_notifications-BCM.py > ./bank_notification/bank_log/BCM.log 2>&1" ,'交通银行','BCM' )

#北京银行
run_python_file("python3 ./bank_notification/bank_file/bank_maintenance_notifications-BOB.py > ./bank_notification/bank_log/BOB.log 2>&1" ,'北京银行','BOB')

#中国银行
run_python_file("python3 ./bank_notification/bank_file/bank_maintenance_notifications-BOC.py > ./bank_notification/bank_log/BOC.log 2>&1" ,'中国银行'  ,'BOC')

#内蒙古银行
run_python_file("python3 ./bank_notification/bank_file/bank_maintenance_notifications-BOIM.py > ./bank_notification/bank_log/BOIM.log 2>&1" ,'内蒙古银行','BOIM')

#中国建设银行
run_python_file("python3 ./bank_notification/bank_file/bank_maintenance_notifications-CCB.py > ./bank_notification/bank_log/CCB.log 2>&1" ,'中国建设银行','CCB' )

#中国光大银行
run_python_file("python3 ./bank_notification/bank_file/bank_maintenance_notifications-CEB.py > ./bank_notification/bank_log/CEB.log 2>&1" ,'中国光大银行','CEB' )

#中信银行
run_python_file("python3 ./bank_notification/bank_file/bank_maintenance_notifications-CITIC.py > ./bank_notification/bank_log/CITIC.log 2>&1" ,'中信银行','CITIC' )

#中国招商银行
run_python_file("python3 ./bank_notification/bank_file/bank_maintenance_notifications-CMB.py > ./bank_notification/bank_log/CMB.log 2>&1" ,'中国招商银行','CMB' )

#中国民生银行
run_python_file("python3 ./bank_notification/bank_file/bank_maintenance_notifications-CMBC.py > ./bank_notification/bank_log/CMBC.log 2>&1" ,'中国民生银行','CMBC' )

#华夏银行
run_python_file("python3 ./bank_notification/bank_file/bank_maintenance_notifications-HB.py > ./bank_notification/bank_log/HB.log 2>&1" ,'华夏银行','HB' )

#兴业银行
run_python_file("python3 ./bank_notification/bank_file/bank_maintenance_notifications-IB.py > ./bank_notification/bank_log/IB.log 2>&1" ,'兴业银行','IB' )

#中国工商银行
run_python_file("python3 ./bank_notification/bank_file/bank_maintenance_notifications-ICBC.py > ./bank_notification/bank_log/ICBC.log 2>&1" ,'中国工商银行','ICBC' )

#天津农商行
run_python_file("python3 ./bank_notification/bank_file/bank_maintenance_notifications-TRCB.py > ./bank_notification/bank_log/TRCB.log 2>&1" ,'天津农商银行','TRCB' )

#浦发银行
run_python_file("python3 ./bank_notification/bank_file/bank_maintenance_notifications-SPDB.py > ./bank_notification/bank_log/SPDB.log 2>&1" ,'浦发银行','SPDB' )

#telegram 传送警示讯息
run_python_file("python3 ./bank_notification/bank_file/telegram_bot_notification.py > ./bank_notification/bank_log/telegram_bot.log 2>&1" ,'Telegram通知','telegram_bot' )

#爬虫完成送出通知
telebot_finish()


# In[ ]:




