# -*- coding: utf-8 -*-
"""
空氣品質指標-API-JSON
"""

import json
import ssl
import urllib.request

import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime

# 圓點圖函式
def plot_ro(x, y,row):
    plt.figure(figsize=(18,4))
    plt.subplot(1, 2, row)
    plt.ylim(10,50)
    plt.plot(x,y,"ro") 
    plt.title("空氣品質指標(AQI)-圓點圖",loc="left")
    plt.xlabel("觀測站")
    plt.ylabel("AQI")
    plt.show()

# 折線圖函式
def plot_line(x, y,row):
    plt.figure(figsize=(18,4))
    # plt.bar(x,y,width=5,label="sample1")
    plt.subplot(1, 2, row)
    plt.ylim(10,50)
    plt.plot(x,y, color='maroon', marker='o')
    plt.title("空氣品質指標(AQI)-折線圖",loc="Right")
    # plt.legend()
    plt.xlabel("觀測站")
    plt.ylabel("AQI")
    plt.show

# 長條圖函式
def plot_bar(df,SiteName,AQI,row):
    df.plot(x =SiteName, y=AQI, kind = 'bar')
    # plt.show()
    
# 長條圖函式
def schedule(df,SiteName,AQI,row):
    df.plot(x =SiteName, y=AQI, kind = 'bar')
    # plt.show()    

# 主程式
if __name__ == "__main__": 	
    
    url = 'https://data.epa.gov.tw/api/v1/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&format=json'    
    context = ssl._create_unverified_context()   
    # print(context)    
    with urllib.request.urlopen(url, context=context) as jsondata:
         #將JSON進行UTF-8的BOM解碼，並把解碼後的資料載入JSON陣列中
         data = json.loads(jsondata.read().decode('utf-8-sig')) 
        
    # print(data)
    
    # 儲存成local json檔,檔名加上儲存時間
    now = datetime.now()
    current_time = now.strftime("%Y%m%d%H%M%S")    
    local_json_data="Jsons\local_json_data" + current_time + ".json"   
    with open(local_json_data, "w", encoding='utf-8-sig') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
            
    # 中文標籤
    plt.rcParams['font.family']='Microsoft Yahei'
    
    # 先顯示2筆   
    for i in range(10,12):
        localDic=data['records'][i]
        SiteName=localDic['SiteName']
        AQI=localDic['AQI']
        Status=localDic['Status']
        print(SiteName,'\t',AQI,'\t',Status)
        
    
    # 輸入地區關鍵字查符合的觀測站空氣品質  
    SiteNamelst_key = [] 
    AQIlst_key = [] 
    name=input("請輸入地區關鍵字名稱:")
    for localDic in data['records']:
        SiteName=localDic['SiteName']
        AQI=localDic['AQI']
        Status=localDic['Status']
        if name in localDic["SiteName"]:
            print(SiteName,' AQI=',AQI, ' 狀態=', Status)    
            SiteNamelst_key.append(SiteName) 
            AQIlst_key.append(int(AQI)) 
    
    
    # 搜尋範圍 輸入最小值,最大值 找出符合的資料
    SiteNamelst_range = [] 
    AQIlst_range = [] 
    min=input("請輸入查詢的AQI最小值:")
    max=input("請輸入查詢的AQI最大值:")
    for localDic in data['records']:
        SiteName=localDic['SiteName']
        AQI=localDic['AQI']
        Status=localDic['Status']
        if AQI > min and AQI < max:
            print(SiteName,' AQI=',AQI, ' 狀態=', Status)    
            SiteNamelst_range.append(SiteName) 
            AQIlst_range.append(int(AQI)) 
        
    # 圖表輸出符合條件的資料  
    dict_key = {"SiteNamelst_key": SiteNamelst_key,"AQIlst_key": AQIlst_key} 
    df_key = pd.DataFrame(dict_key)
       
    dict_range = {"SiteName_range": SiteNamelst_range,"AQIlst_range": AQIlst_range} 
    df_range = pd.DataFrame(dict_range)
    
    #呼叫圓點圖函式
    plot_ro(SiteNamelst_key, AQIlst_key, 1)
    plot_ro(SiteNamelst_range, AQIlst_range, 2)
    
    #呼叫折線圖函式
    plot_line(SiteNamelst_key, AQIlst_key, 1)
    plot_line(SiteNamelst_range, AQIlst_range, 2)
    
    #呼叫長條圖函式
    plot_bar(df_key,'SiteNamelst_key','AQIlst_key',1)
    plot_bar(df_range,'SiteName_range','AQIlst_range',2)
    
       
    # 輸入完整地區名稱,從資料庫撈取資料呈現該地區空氣品質指標變化圖表
    name_sql=input("請輸入完整地區名稱:")
    import pymysql as maria
    conn = maria.connect(host="127.0.0.1", user="root", passwd="1234", 
                          db="mylab", port=3307, charset="utf8")
    cusr = conn.cursor()
    sql_query = "select * from airquality where SiteName ='" + name_sql + "' order by Date"
    # print(sql_query)
    
    cusr.execute(sql_query)
    rs=cusr.fetchall()
    
    AQIlst_sql = []
    Datelst_sql = []         
    for row in rs:
        AQIlst_sql.append(int(row[2]))
        Datelst_sql.append(str(row[3].strftime("%m%d %H")))
    
    plt.figure(figsize=(18,4))
    plt.subplot(1, 2, 1)
    plt.ylim(10,50)
    plt.plot(Datelst_sql,AQIlst_sql, color='maroon', marker='o')
    plt.title("空氣品質指標(AQI)-折線圖",loc="Right")
    plt.xlabel("%s觀測站" %name_sql)
    plt.ylabel("AQI")
    plt.show
        
    cusr.close() 
    conn.close()



    # test 20220727
    # Plus Tkinter 操作介面可視化操作 主操作介面+輸入查詢+列表和圖表顯示在主視窗








