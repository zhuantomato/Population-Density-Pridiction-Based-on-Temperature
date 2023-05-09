import datetime
import pickle

import numpy as np
from sklearn.discriminant_analysis import StandardScaler
import WebGUI.BusinessLogic as BL
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app) # enable CORS for all routes

@app.route('/process', methods=['POST'])
@cross_origin() # enable CORS for this route
def handle_data():
    # 获取 JSON 格式的请求数据
    data = request.get_json()
    # 获取下拉菜单的选中值和鼠标点击的经纬度
    type = data['type']
    POI = data['POI']
    lnglat = data['lnglat']
    bottom_left,top_right = BL.ractangle(lnglat)
    province,city,citycode = BL.get_city_name(lnglat['lng'], lnglat['lat'])
    temperature = BL.get_weather(citycode, type)
    newtemp = temperature
    if POI == 'Eating POIs':
        Model = pickle.load(open('AutoModelling\LR_Eating.pkl', 'rb'))
    elif POI == 'Sports POIs':
        Model = pickle.load(open('AutoModelling\LR_Sports.pkl', 'rb'))
    else:
        Model = pickle.load(open('AutoModelling\LR_Entertainment.pkl', 'rb'))
    #获取当前时间，并只保留小时
    hour = datetime.datetime.now().hour
    #判断当前日期是否是周末
    is_weekend = int(datetime.datetime.now().weekday() in [5,6])
    data = [temperature, lnglat['lat'], lnglat['lng'], is_weekend, hour]
    data = [float(x) for x in data]
    data = np.array(data).reshape(1,5)
    scaler = pickle.load(open('WebGUI\scaler.pkl', 'rb'))
    data = scaler.transform(data)
    temperature = newtemp
    # 调用模型进行预测
    if isinstance(city, str):
        address = province + city
    else:
        address = province
    if type == 'Real-time':
        curr_time=datetime.datetime.now()
        time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M')
        predict = BL.get_traffic(top_right, bottom_left,citycode)

    else:
        today = datetime.date.today()
        time_str = str(today + datetime.timedelta(days=1))
        result = BL.predict(data)
        predict = round(result.item(),6)
    # 将城市名称、温度、当前时间、处理结果装入result中
    result = {'address': address,'temperature':temperature,'time':time_str,'predict':predict}
    # 将处理结果作为 JSON 格式的响应返回给前端页面
    return jsonify(result = result)

if __name__ == '__main__':
    app.run()