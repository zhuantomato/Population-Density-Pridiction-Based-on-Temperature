import pandas as pd
import numpy as np


# 读取交通数据
traffic_data = []
for city in ['Beijing', 'Guiyang', 'HaErBin', 'Haikou']:
    for i in range(1, 4):
        filename = 'Modelling\DataPreprocess\MeanTraffic\\' + city + str(i) + 'Mean.csv'
        df = pd.read_csv(filename)
        df['location'] = city
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

# 保存数据
data.to_csv('Modelling\DataPreprocess\Weather\data.csv', index=False)

    