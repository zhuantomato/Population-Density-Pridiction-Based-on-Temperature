'''
Author: Ruijie Ni 1924975712@qq.com
Date: 2023-03-23 19:06:52
LastEditors: Ruijie Ni 1924975712@qq.com
LastEditTime: 2023-03-23 21:39:11
FilePath: \Population-Density-Pridiction-Based-on-Temperature\Modelling\DataPreprocess\DataTransform.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pandas as pd
dataset1 = 'Crawler\Outputs\Haikou3.csv'
dataset2 = 'Crawler\Outputs\Haikou3Jam.csv'
output = 'Modelling\DataPreprocess\MeanTraffic\Haikou3Mean.csv'

# 读取数据
data1 = pd.read_csv(dataset1, encoding='gbk',usecols=['时间', 'status'])
data2 = pd.read_csv(dataset2, encoding='gbk', usecols=['time', 'status'])

# 将时间列转换为Pandas的日期时间类型
data1['time'] = pd.to_datetime(data1['时间']).dt.floor('min')
data2['time'] = pd.to_datetime(data2['time']).dt.floor('min')

# 将数据按照时间和地点分组
data = pd.concat([data1, data2])
grouped_data = data.groupby(['time'])

# 计算每个地点每个时间点的平均交通状况
mean_data = grouped_data.mean(numeric_only=True)

# 将数据转换为数值型数据
numeric_data = mean_data.apply(pd.to_numeric)

numeric_data.to_csv(output, encoding='gbk')