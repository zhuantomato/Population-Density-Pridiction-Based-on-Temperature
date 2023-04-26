import io
import json
import math
import os
import sys
import numpy as np
import requests
from sklearn.discriminant_analysis import StandardScaler
import tensorflow as tf
import pandas as pd
amap_web_key = 'd7620288fea4be1bf89de3d32c0bf3b4'
baidu_web_key = 'pfARyIAcUfrGjnhtf2E4qKZOG4lXOUpG'

# 定义一些常量
EARTH_RADIUS = 6371 # 地球半径，单位为公里
DEG_TO_RAD = math.pi / 180 # 角度转弧度的因子
RAD_TO_DEG = 180 / math.pi # 弧度转角度的因子
DIAGONAL = 1 # 对角线长度，单位为公里
ANGLE = 45 # 对角线与经线的夹角，单位为度

# 计算经纬度矩形的四个顶点的经纬度
def ractangle(center):
    # 给定中心点的经纬度

    # 计算对角线的一半长度
    half_diagonal = DIAGONAL / 2

    # 计算对角线的方位角（正北为0度，顺时针增加）
    bearing = ANGLE + 90

    # 计算对角线的终点的经纬度
    end_lat = math.asin(math.sin(center['lat'] * DEG_TO_RAD) * math.cos(half_diagonal / EARTH_RADIUS) + math.cos(center['lat'] * DEG_TO_RAD) * math.sin(half_diagonal / EARTH_RADIUS) * math.cos(bearing * DEG_TO_RAD)) * RAD_TO_DEG
    end_lng = center['lng'] + math.atan2(math.sin(bearing * DEG_TO_RAD) * math.sin(half_diagonal / EARTH_RADIUS) * math.cos(center['lat'] * DEG_TO_RAD), math.cos(half_diagonal / EARTH_RADIUS) - math.sin(center['lat'] * DEG_TO_RAD) * math.sin(end_lat * DEG_TO_RAD)) * RAD_TO_DEG

    # 计算对角线的起点的经纬度（与终点相反）
    start_lat = 2 * center['lat'] - end_lat
    start_lng = 2 * center['lng'] - end_lng

    # 计算矩形的四个顶点的经纬度（顺时针),并保留6位小数
    top_right = {'lng': round(end_lng,6), 'lat': round(start_lat,6)}
    top_left = {'lng': round(start_lng,6), 'lat': round(start_lat,6)}
    bottom_left = {'lng': round(start_lng,6), 'lat': round(end_lat,6)}
    bottom_right = {'lng': round(end_lng,6), 'lat': round(end_lat,6)}

    return bottom_left,top_right

# 调用高德开发平台API，获取所在经纬度的城市名称
def get_city_name(lng, lat):
    url = 'https://restapi.amap.com/v3/geocode/regeo?output=json&location=' + str(lng) + ',' + str(lat) + '&key=' + amap_web_key
    result = requests.get(url)
    result = json.loads(result.text)
    #返回省份、城市名称和城市代码
    return result['regeocode']['addressComponent']['province'], result['regeocode']['addressComponent']['city'], result['regeocode']['addressComponent']['adcode']


# 调用高德开发平台API，获取所在城市的天气信息
def get_weather(citycode,type):
    #如果type是"Real-time"，将它的值改为"base"，否则改为"all"
    type = 'base' if type == 'Real-time' else 'all'
    url = 'https://restapi.amap.com/v3/weather/weatherInfo?key=' + amap_web_key + '&city=' + citycode + '&extensions=' + type
    result = requests.get(url)
    result = json.loads(result.text)
    #因为type类型不同，返回的数据格式也不同，所以需要分别处理
    if type == 'base':
        return result["lives"][0]["temperature"]
    else:
        return result['forecasts'][0]['casts'][0]['daytemp']

# 调用百度地图开放平台API，获取经纬度矩形的交通信息
def get_traffic(top_right, bottom_left,citycode):
    bounds = str(bottom_left['lat']) + ',' + str(bottom_left['lng']) + ';' + str(top_right['lat']) + ',' + str(top_right['lng'])
    url = f"http://api.map.baidu.com/traffic/v1/bound?ak={baidu_web_key}&bounds={bounds}&coord_type_input=gcj02&coord_type_output=gcj02"
    response = requests.get(url) #返回的原数据
    if response.status_code == 200:
        data = json.loads(response.text)
        if data["status"] == 0:
            for road in data["road_traffic"]:
                if(road["road_name"]!="UNKNOW"):
                    if len(road)>=2:         
                        get_page(road["road_name"],citycode)       
                        es(road["road_name"],citycode)                   
                    else:
                        es(road["road_name"],citycode) 
        else: print("data status != 0")
    else: print("response error")
    return get_average()

#改变标准输出的默认编码
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
#Construct the data functions about the road
def fers(road_name,citycode): 
    city = citycode      
    ak = 'pfARyIAcUfrGjnhtf2E4qKZOG4lXOUpG'        
    url = 'http://api.map.baidu.com/traffic/v1/road?road_name={}&city={}&ak={}'.format(str(road_name),city,ak)  
    re=requests.get(url) #returning data
    decodejson=json.loads(re.text)
    road_traffic_s=decodejson['road_traffic'][0]      #get traffic status                       
    v=road_traffic_s['congestion_sections']
    ty=pd.DataFrame(v)
    ty['name']=pd.DataFrame([road_traffic_s['road_name']]*len(v))      
    return ty

#Construct descriptive functions
def es(road_name,citycode):
    city = citycode
    ak = 'pfARyIAcUfrGjnhtf2E4qKZOG4lXOUpG'
    url = 'http://api.map.baidu.com/traffic/v1/road?road_name={}&city={}&ak={}'.format(str(road_name),city,ak)
    re=requests.get(url) 
    res=re.json() 
    decodejson = json.loads(re.text)
    evaluation=decodejson['evaluation']     #overall status
    road_traffic=decodejson['road_traffic'][0]
    road_data=pd.DataFrame([evaluation])
    road_data['road_name']=road_traffic['road_name']   
#     return road_data      
    if not os.path.exists('TempData/temp.csv'):
            road_data.to_csv('TempData/temp.csv',encoding='gbk',mode='w',index=False,index_label=False)      
    else:
            road_data.to_csv('TempData/temp.csv', encoding='gbk', mode='a', index=False, index_label=False,header=False)

#Construct the function to get the page
def get_page(road_name,citycode):
    s=fers(road_name,citycode)
    if not os.path.exists('TempData/tempJam.csv'):
           s.to_csv('TempData/tempJam.csv',encoding='gbk',mode='w',index=False,index_label=False)
    else:
            s.to_csv('TempData/tempJam.csv', encoding='gbk', mode='a', index=False, index_label=False,header=False)

#获取平均拥堵程度
def get_average():
    dataset1 = 'TempData/temp.csv'
    dataset2 = 'TempData/tempJam.csv'
    data1 = pd.read_csv(dataset1, encoding='gbk',usecols=['status'])
    data = data1
    #如果dataset2存在，则读取
    if os.path.exists(dataset2):
        data2 = pd.read_csv(dataset2, encoding='gbk', usecols=['status'])
        data = pd.concat([data1, data2])
    # 计算每个地点每个时间点的平均交通状况
    mean_data = data.mean(numeric_only=True)
    # 将数据转换为数值型数据
    numeric_data = round(mean_data.item(),6)
    os.remove(dataset1)
    if os.path.exists(dataset2):
        os.remove(dataset2)
    return numeric_data

#将深度学习模型载入，并进行预测
def predict(data):
    #载入模型
    model = tf.keras.models.load_model('AutoAdjustedModels\DNN\DNNSimple.h5')
    #进行预测
    result = model.predict(data)
    #返回预测结果
    return result





