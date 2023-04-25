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
    selectedOption = data['option']
    lnglat = data['lnglat']
    # 在这里处理数据...
    print(selectedOption, lnglat)
    result = 'your result'
    # 将处理结果作为 JSON 格式的响应返回给前端页面
    return jsonify(result=result)

if __name__ == '__main__':
    app.run()