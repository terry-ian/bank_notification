#手动设置参数文件

#mysql_parameter
db_host='remotemysql.com'
db_user='giaX9JoXo3'
db_passwd='VEm7Ky6FIB'
db_port=3306
db_database='giaX9JoXo3'
db_table1='bank_webcrawler'
db_table2='bank_notification'

#telegram_parameter group
tele_chatid='-364811652'
tele_token='1020859504:AAEb-tLbaBjJvJqBsLCzCsStrgTlZNqXRR8'

#warning message 
tele_warning_chatid='-364811652'
tele_warning_token='1020859504:AAEb-tLbaBjJvJqBsLCzCsStrgTlZNqXRR8'

#反爬虫用 模拟使用者
send_headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
 "Connection": "keep-alive",
 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
 "Accept-Language": "zh-CN,zh;q=0.8" }