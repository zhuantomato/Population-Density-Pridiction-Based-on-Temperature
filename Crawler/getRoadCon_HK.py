'''
Author: Ruijie Ni 1924975712@qq.com
Date: 2023-02-20 15:49:44
LastEditors: Ruijie Ni 1924975712@qq.com
LastEditTime: 2023-03-19 12:38:31
FilePath: \毕设\getRoadCon.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pandas as pd
import requests
import os
import time     
import datetime
from time import strftime,asctime,ctime,gmtime,mktime
import json
import csv
import io
import sys

#改变标准输出的默认编码
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
#Construct the data functions about the road
def fers(road_name): 
    city = '海口市'      
    ak = 'pYXwBQyGeD9LSApqsDnYTPPBz3RGo3Yx'        
    url = 'http://api.map.baidu.com/traffic/v1/road?road_name={}&city={}&ak={}'.format(str(road_name),city,ak)          #爬过数据的人应该都知道这是什么东西吧，哈哈
    #url = f"http://api.map.baidu.com/traffic/v1/bound?ak={ak}&bounds={bounds}"
    re=requests.get(url) #returning data
    decodejson=json.loads(re.text)
    road_traffic_s=decodejson['road_traffic'][0]      #get traffic status                       
    v=road_traffic_s['congestion_sections']
    curr_time=datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')    #get current time
    ty=pd.DataFrame(v)
    ty['name']=pd.DataFrame([road_traffic_s['road_name']]*len(v))   
    ty['time']=pd.DataFrame([time_str]*len(v))    
    return ty

#Construct descriptive functions
def es(road_name,i):
    city = '海口市'
    ak = 'pYXwBQyGeD9LSApqsDnYTPPBz3RGo3Yx'
    url = 'http://api.map.baidu.com/traffic/v1/road?road_name={}&city={}&ak={}'.format(str(road_name),city,ak)
    #url = f"http://api.map.baidu.com/traffic/v1/bound?ak={ak}&bounds={bounds}"
    re=requests.get(url) 
    res=re.json() 
    decodejson = json.loads(re.text)
    description=decodejson['description']         #overall description
    evaluation=decodejson['evaluation']     #overall status
    road_traffic=decodejson['road_traffic'][0]
    road_data=pd.DataFrame([evaluation])
    road_data['road_name']=road_traffic['road_name']   
    curr_time=datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
    road_data['时间']=pd.DataFrame([time_str])              
    road_data['路况描述']=description
#     return road_data      
    if not os.path.exists('Outputs\Haikou'+str(i)+'.csv'):
            road_data.to_csv('Outputs\Haikou'+str(i)+'.csv',encoding='gbk',mode='a',index=False,index_label=False)      
    else:
            road_data.to_csv('Outputs\Haikou'+str(i)+'.csv', encoding='gbk', mode='a', index=False, index_label=False,header=False)

#Def storing functions
def get_page(road_name,i):
    city = '海口市'
    s=fers(road_name)
    if not os.path.exists('Outputs\Haikou'+str(i)+'Jam.csv'):
           s.to_csv('Outputs\Haikou'+str(i)+'Jam.csv',encoding='gbk',mode='a',index=False,index_label=False)
    else:
            s.to_csv('Outputs\Haikou'+str(i)+'Jam.csv', encoding='gbk', mode='a', index=False, index_label=False,header=False)

#crawling every 5 mins
while True:
    if __name__ == '__main__':
        # road_name = ['西单北大街','宣武门内大街','复兴门内大街','西长安街'] 
        # for i in road_name:
        #         city = '北京市'
        #         ak = 'pfARyIAcUfrGjnhtf2E4qKZOG4lXOUpG'
        #         url = 'http://api.map.baidu.com/traffic/v1/road?road_name={}&city={}&ak={}'.format(str(i),city,ak)
        #         re=requests.get(url) 
        #         decodejson = json.loads(re.text) 
        #         road_traffics=decodejson['road_traffic']     
        #         if len(road_traffics[0])>=2:         #对拥堵路段进行详细数据提取，为什么这样写呢，就是因为拥堵时数据长度为2，非拥堵时段长度为1，这真是我观察了好久，不断报错找到的规律啊，我太难了！！！苦啊
        #             get_page(i)       #store detailed traffic data for traffic jam.
        #             es(i)                        
        #         else:
        #             es(i)     #store overall traffic data for clear traffic.
        ak = 'pYXwBQyGeD9LSApqsDnYTPPBz3RGo3Yx'
        #bounds = "39.905,116.371;39.909,116.377"
        # 定义5个bounds
        bounds1 = "20.030734,110.317357;20.040734,110.327357"
        bounds2 = "20.034288,110.347809;20.044288,110.357809"
        bounds3 = "20.038505,110.336464;20.048505,110.346464"

        # 将5个bounds放入一个列表中
        bounds_list = [bounds1, bounds2, bounds3]
        i=1
        for bounds in bounds_list:
            url = f"http://api.map.baidu.com/traffic/v1/bound?ak={ak}&bounds={bounds}&coord_type_input=gcj02&coord_type_output=gcj02"
            response = requests.get(url) #返回的原数据
            if response.status_code == 200:
                data = json.loads(response.text)
                if data["status"] == 0:
                    for road in data["road_traffic"]:
                        if(road["road_name"]!="UNKNOW"):
                            if len(road)>=2:         #对拥堵路段进行详细数据提取，为什么这样写呢，就是因为拥堵时数据长度为2，非拥堵时段长度为1，这真是我观察了好久，不断报错找到的规律啊，我太难了！！！苦啊
                                get_page(road["road_name"],i)       #拥堵时段爬取拥堵时段的详细数据，保存一个文件
                                es(road["road_name"],i)                        #保存描述性数据
                            else:
                                es(road["road_name"],i) 
                else: print("data status != 0")
            else: print("response error")
            i=i+1
    time.sleep(1200)

