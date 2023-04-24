import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import geopandas as gpd

class MapWidget(QMainWindow):
    def __init__(self, map_data):
        super().__init__()

        self.map_data = map_data

        # 创建一个图形和轴对象
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        # 将地图数据绘制到轴对象上
        self.map_data.plot(ax=self.axes)

        # 设置轴对象的初始状态
        self.axes.set_xlim(self.map_data.total_bounds[0], self.map_data.total_bounds[2])
        self.axes.set_ylim(self.map_data.total_bounds[1], self.map_data.total_bounds[3])
        self.axes.set_aspect('equal')

        # 添加canvas到窗口中
        self.setCentralWidget(self.canvas)

        # 连接canvas的点击事件处理器
        self.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        # 将点击的坐标转换为经纬度
        x, y = event.xdata, event.ydata
        lon, lat = self.axes.transData.inverted().transform((x, y))

        # 在屏幕上显示经纬度
        print(f"Clicked on ({lon:.4f}, {lat:.4f})")

if __name__ == '__main__':
    # 读取中国区域地图数据
    map_data = gpd.read_file('path/to/shapefile')

    # 初始化应用程序和主窗口
    app = QApplication(sys.argv)
    window = MapWidget(map_data)

    # 显示主窗口
    window.show()
    sys.exit(app.exec_())
