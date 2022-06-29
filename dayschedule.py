# -*- coding: utf-8 -*-
"""
每天固定時間撈取一次資料存到資料庫
@author: benhuang
"""

import json
import ssl
import urllib.request
from datetime import datetime
import pymysql as maria
    
def API_To_DB():
    print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    url = 'https://data.epa.gov.tw/api/v1/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&format=json'    
    context = ssl._create_unverified_context()   
    # print(context)    
    with urllib.request.urlopen(url, context=context) as jsondata:
         #將JSON進行UTF-8的BOM解碼，並把解碼後的資料載入JSON陣列中
         data = json.loads(jsondata.read().decode('utf-8-sig'))        
    # print(data)  

    conn = maria.connect(host="127.0.0.1", user="root", passwd="1234", 
                          db="mylab", port=3307, charset="utf8")
    cusr = conn.cursor()  
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    # strSQL=""
    values = []
    for localDic in data['records']:
        SiteName=localDic['SiteName']
        AQI=localDic['AQI']
        Date=current_time      
        # print(SiteName,'\t',AQI,'\t',Date)            
        # strSQL="insert into airquality (SiteName,AQI,Date) values ('"+SiteName+"',"+AQI+", '"+Date+"')"
        # strSQL+="insert into airquality (SiteName,AQI,Date) values ('"+SiteName+"',"+AQI+", '"+Date+"');"
        values.append([SiteName,AQI,Date])
        
    # print('strSQL=',strSQL)
    # cusr.execute(strSQL)             
    cusr.executemany("insert into airquality(SiteName,AQI,Date) values (%s, %s, %s)", values)
    conn.commit() 
      
    cusr.close()
    conn.close()
    
# pip3 install APScheduler
import time
from apscheduler.schedulers.blocking import BlockingScheduler
if __name__ == "__main__":

    sched = BlockingScheduler()
    
    # 每x秒
    # sched.add_job(my_job, 'interval', seconds=10)
    # sched.add_job(API_To_DB, 'interval', seconds=30)
    # 每x小時
    # sched.add_job(API_To_DB, 'interval', hours=2)
    # 每天固定時間
    sched.add_job(API_To_DB, 'cron', hour='11', minute='00')
    
    sched.start()    









    
    
    
   