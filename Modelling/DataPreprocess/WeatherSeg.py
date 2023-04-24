'''
Author: Ruijie Ni 1924975712@qq.com
Date: 2023-03-24 19:40:59
LastEditors: Ruijie Ni 1924975712@qq.com
LastEditTime: 2023-03-24 20:13:09
FilePath: \Population-Density-Pridiction-Based-on-Temperature\Modelling\DataPreprocess\WeatherSeg.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import csv
import os

# 读取csv文件
with open('Crawler\Outputs\weather.csv', 'r',encoding='utf-8') as f:
    reader = csv.reader(f)
    # 跳过第一行
    next(reader)
    # 遍历每一行数据
    for row in reader:
        # 获取城市名
        city = row[0]
        # 获取天气信息
        weather = row[1]
        # 获取温度
        temp = row[2]
        # 获取时间
        time = row[3]
        # 创建文件夹
        if not os.path.exists(city):
            os.makedirs(city)
        # 创建文件
        with open(f'Modelling\DataPreprocess\Weather/{city}.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            # 写入数据
            writer.writerow([weather, temp, time])