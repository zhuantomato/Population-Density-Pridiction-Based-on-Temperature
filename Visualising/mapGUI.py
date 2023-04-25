import tkinter as tk #导入tkinter库 
from PIL import Image, ImageTk #导入PIL库 
import math #导入math库 
 
#定义一个类，用于显示中国区域地图的GUI程序 
class MapViewer(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        
    # 创建GUI所需的所有控件
    def create_widgets(self):
        # 创建一个画布用于显示中国区域地图
        self.canvas = tk.Canvas(self, width=600, height=400, bg="white")
        self.canvas.pack()
        # 将地图图片加载到画布中
        self.image = Image.open('Visualising\china_map.png')
        self.image = self.image.resize((600, 400), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")
        
        # 创建一个放大按钮
        self.zoom_in_btn = tk.Button(self, text="放大", command=self.zoom_in)
        self.zoom_in_btn.pack()
        
        # 创建一个缩小按钮
        self.zoom_out_btn = tk.Button(self, text="缩小", command=self.zoom_out)
        self.zoom_out_btn.pack()
        
        # 创建一个移动按钮
        self.move_btn = tk.Button(self, text="移动", command=self.move)
        self.move_btn.pack()
        
        # 创建一个显示地理坐标信息的标签
        self.coordinate_label = tk.Label(self, text="经纬度：")
        self.coordinate_label.pack()
        
    # 放大函数，用于放大地图
    def zoom_in(self):
        # 获取画布的当前大小
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        # 画布放大一倍
        self.canvas.config(width=width*2, height=height*2)
        # 将放大后的地图图片加载到画布中
        self.image = Image.open('Visualising\china_map.png')
        self.image = self.image.resize((width*2, height*2), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")
        # 绑定点击事件
        self.canvas.bind("<Button-1>", self.click_map)
        
    # 缩小函数，用于缩小地图
    def zoom_out(self):
        # 获取画布的当前大小
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        # 画布缩小一倍
        self.canvas.config(width=width//2, height=height//2)
        # 将缩小后的地图图片加载到画布中
        self.image = Image.open('map.jpg')
        self.image = self.image.resize((width//2, height//2), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")
        # 绑定点击事件
        self.canvas.bind("<Button-1>", self.click_map)
        
    # 移动函数，用于移动地图
    def move(self):
        # 获取画布的当前大小
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        # 获取画布的当前位置
        x = self.canvas.winfo_x()
        y = self.canvas.winfo_y()
        # 计算移动之后的位置
        x += 10
        y += 10
        if x > width:
            x = 0
        if y > height:
            y = 0
        # 画布移动到新的位置
        self.canvas.place(x=x, y=y)
        # 绑定点击事件
        self.canvas.bind("<Button-1>", self.click_map)
    
    # 点击事件，用于返回点击位置的经纬度
    def click_map(self, event):
        # 获取点击位置的像素坐标
        x = event.x
        y = event.y
        # 计算点击位置的地理坐标（经纬度）
        longitude = round(x / self.canvas.winfo_width() * 360 - 180, 3)
        latitude = round(math.degrees(math.atan(math.exp(y / self.canvas.winfo_height() * math.pi - math.pi / 2)) - 90, 3))
        # 更新显示地理坐标信息的标签
        self.coordinate_label.config(text="经纬度："+str(longitude)+", "+str(latitude))
        
# 启动GUI程序
root = tk.Tk()
app = MapViewer(master=root)
app.mainloop()