# 引入需要的库
import tkinter as tk
import requests
import json
from tkinter import messagebox
import urllib

# 百度地图API需要的ak
ak = "pfARyIAcUfrGjnhtf2E4qKZOG4lXOUpG"

# 定义主窗口
root = tk.Tk()
root.title("Population predict")
root.geometry("500x400")

# 定义变量用于保存用户点击的坐标
longitude = 0
latitude = 0

# 定义按钮点击事件
def clickButton():
    global longitude
    global latitude
    # 利用百度地图API获取城市名
    url = "http://api.map.baidu.com/geocoder/v2/"
    params = {
        "callback": "renderReverse",
        "location": str(longitude) + "," + str(latitude),
        "output": "json",
        "pois": "1",
        "ak": ak
    }
    r = requests.get(url, params=params)
    result = r.json()
    city = result["result"]["addressComponent"]["city"]
    # 显示获取到的城市名
    messagebox.showinfo("提示", "你点击的位置所在城市是：" + city)

# 添加一个按钮
btn = tk.Button(root, text="Get prediction", command=clickButton)
btn.pack()

# 定义画布
canvas = tk.Canvas(root, bg="white", width=500, height=400)
canvas.pack()

# 加载中国地图
url = "http://api.map.baidu.com/staticimage/v2?"
params = {
    "ak": ak,
    "width": 500,
    "height": 400,
    "center": "116.403874,39.914889",
    "markers": "116.403874,39.914889",
    "markerStyles": "l,A",
    "format": "png"  # 修改图片格式
}
url += urllib.parse.urlencode(params)
image_data = urllib.request.urlopen(url).read()
image = tk.PhotoImage(data=image_data)
canvas.create_image(250, 200, image=image)

# 定义鼠标点击事件
def click(event):
    global longitude
    global latitude
    # 获取用户点击的坐标
    x = event.x
    y = event.y
    # 标记用户点击的位置
    canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")
    # 保存经纬度值
    longitude = x
    latitude = y
    # 将经纬度值显示在屏幕上
    label = tk.Label(root, text="经度：" + str(longitude) + "\n纬度：" + str(latitude))
    label.pack()

# 绑定鼠标点击事件
canvas.bind('<Button-1>', click)

# 开启消息循环
root.mainloop()