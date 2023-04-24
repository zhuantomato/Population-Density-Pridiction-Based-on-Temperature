'''
Author: Ruijie Ni 1924975712@qq.com
Date: 2023-03-24 20:41:49
LastEditors: Ruijie Ni 1924975712@qq.com
LastEditTime: 2023-04-11 16:00:08
FilePath: \Population-Density-Pridiction-Based-on-Temperature\Modelling\DataPreprocess\TrafficMerge.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pandas as pd
import numpy as np


# 定义经纬度范围
beijing_bounds = [(39.919614, 116.451179), (39.992258, 116.484573), (39.880608, 116.466821)]
guiyang_bounds = [(26.58533, 106.720074), (26.586553, 106.707252), (26.600023, 106.711234)]
haerbin_bounds = [(45.77229, 126.624968), (45.767358, 126.655482), (45.75604, 126.65613)]
haikou_bounds = [(20.035734, 110.322357), (20.039288, 110.352809), (20.043505, 110.341464)]
# 定义城市列表和对应的经纬度范围
cities = ['Beijing', 'Guiyang', 'HaErBin', 'Haikou']
bounds = [beijing_bounds, guiyang_bounds, haerbin_bounds, haikou_bounds]

# 读取交通数据
traffic_data = []
for i in range(len(cities)):
    city = cities[i]
    for j in range(1, 4):
        bounds_str = bounds[i][j-1]
        filename = 'Modelling\DataPreprocess\MeanTraffic\\' + city + str(j) + 'Mean.csv'
        df = pd.read_csv(filename)
        df['location'] = city
        df['latitude'] = bounds_str[0]
        df['longitude'] = bounds_str[1]
        traffic_data.append(df)
traffic_data = pd.concat(traffic_data)

# 读取温度数据
temperature_data = []
for city in ['Beijing', 'Guiyang', 'HaErBin', 'Haikou']:
    filename = 'Modelling\DataPreprocess\Weather\\' +city + '.csv'
    df = pd.read_csv(filename, header=None, names=['weather', 'temperature', 'time'],encoding='gbk')
    df['location'] = city
    temperature_data.append(df)
temperature_data = pd.concat(temperature_data)

# 合并数据
traffic_data['time'] = pd.to_datetime(traffic_data['time'])
temperature_data['time'] = pd.to_datetime(temperature_data['time'])
traffic_data = traffic_data.sort_values(['time'])
temperature_data = temperature_data.sort_values(['time'])
data = pd.merge_asof(traffic_data, temperature_data, on='time', by='location', tolerance=pd.Timedelta('30min'))
data['status'] = data['status'].round(5)

# 处理时间数据
data['time'] = pd.to_datetime(data['time'])
data['is_weekend'] = data['time'].apply(lambda x: 1 if x.weekday()>=5 else 0)
data['hour'] = data['time'].dt.hour
data = data.drop(['time'], axis=1)
data = data.drop(['weather'],axis=1)

data = data.drop(['location'],axis=1)
#data = data.drop(['temperature'],axis=1)
#data = data.drop(['latitude'],axis=1)
#data = data.drop(['longitude'],axis=1)
data = data.dropna()

# 保存数据
data.to_csv('Modelling\DataPreprocess\MergedData\data.csv', index=False)

    