import pandas as pd
import numpy as np


# 定义经纬度范围
beijing_bounds = ['39.914614,116.446179;39.924614,116.456179', '39.987258,116.479573;39.997258,116.489573', '39.875608,116.461821;39.885608,116.471821']
guiyang_bounds = ['26.58033,106.715074;26.59033,106.725074', '26.581553,106.702252;26.591553,106.712252', '26.595023,106.706234;26.605023,106.716234']
haerbin_bounds = ['45.76729,126.619968;45.77729,126.629968', '45.762358,126.650482;45.772358,126.660482', '45.75104,126.65113;45.76104,126.66113']
haikou_bounds = ['20.030734,110.317357;20.040734,110.327357', '20.034288,110.347809;20.044288,110.357809', '20.038505,110.336464;20.048505,110.346464']

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
        df['area'] = bounds_str
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
data = data.drop(['area'],axis=1)
data = data.dropna()

# 保存数据
data.to_csv('Modelling\DataPreprocess\Weather\data.csv', index=False)

    