# 导入requests、json、csv和time库
import requests
import json
import csv
import time

# 定义AK
ak = "d7620288fea4be1bf89de3d32c0bf3b4"

# 定义城市编码的列表
cities = ["110000", "520100", "230100", "460100"] # 北京市、贵阳市、哈尔滨市、海口市

# 定义查询间隔为10分钟（600秒）
interval = 1200

# 使用while循环来重复执行查询和写入操作
while True:
    # 使用for循环来遍历每个城市编码
    for city in cities:
        # 构造请求URL
        url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={ak}&city={city}"

        # 发送GET请求并获取响应
        response = requests.get(url)

        # 解析响应数据为JSON格式
        data = json.loads(response.text)

        # 提取有用的数据
        city_name = data["lives"][0]["city"] # 城市名
        weather = data["lives"][0]["weather"] # 实况天气状况
        temperature = data["lives"][0]["temperature"] # 实时气温
        report_time = data["lives"][0]["reporttime"] # 数据获取时间

        # 打开或创建一个名为“weather.csv”的csv文件，使用a模式追加写入数据
        with open("Outputs\weather.csv", "a", encoding="utf-8", newline="") as f:
            # 创建一个csv写入对象
            writer = csv.writer(f)
            # 写入一行数据，包括城市名、天气、温度和时间
            writer.writerow([city_name, weather, temperature, report_time])

    # 等待10分钟后再次执行循环
    time.sleep(interval)