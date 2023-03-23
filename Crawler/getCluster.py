# 导入pandas模块，用来读取xls文件
import pandas as pd
import io
import sys

#改变标准输出的默认编码
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
# 读取xls文件，返回一个DataFrame对象df
df = pd.read_excel("Codes\data.xls")

# 获取df中的经度和纬度列，并且转换成列表x和y
x = df["x"].tolist()
y = df["y"].tolist()

# 创建一个空字典，用来存储矩形的坐标点和计数器
width = 0.01
height = 0.01
rect_dict = {}

# 定义一个函数，用来判断两个点是否在同一个矩形范围内
def is_in_same_rect(x1, y1, x2, y2):
  # 设置矩形的宽度和高度为0.01度
  width = 0.01
  height = 0.01
  # 计算两个点的横向距离和纵向距离
  dx = abs(x2 - x1)
  dy = abs(y2 - y1)
  # 如果两个点的横向距离小于等于宽度，并且纵向距离小于等于高度，就返回True，否则返回False
  return dx <= width and dy <= height

# 遍历所有的点的坐标值
for i in range(len(x)):
  # 获取第i个点的经度和纬度值
  xi = x[i]
  yi = y[i]
  # 初始化计数器为1，表示当前点本身就是一个餐厅
  count = 1
  # 遍历除了第i个点之外的其他点的坐标值
  for j in range(len(x)):
    # 如果j不等于i，就继续执行
    if j != i:
      # 获取第j个点的经度和纬度值
      xj = x[j]
      yj = y[j]
      # 判断第i个点和第j个点是否在同一个矩形范围内，如果是，就增加计数器
      if is_in_same_rect(xi, yi, xj, yj):
        count += 1
  # 计算当前点所在矩形范围的左下角和右上角的坐标值，并且转换成字符串格式，纬度在前，经度在后，用分号和逗号分隔
  key = ";".join([str(yi), str(xi), str(yi + height), str(xi + width)])
  # 将当前矩形范围的坐标点和计数器存储在字典中，如果已经存在相同的键，就更新值为较大的计数器
  rect_dict[key] = max(rect_dict.get(key, 0), count)

# 导入shapely模块，用来处理几何形状
from shapely.geometry import Polygon

# 创建一个空列表，用来存储不重复的矩形
rect_list = []

# 遍历字典中的键（即矩形的坐标点）
for key in rect_dict:
  # 将键分割成四个坐标值，并且转换成浮点数
  y1, x1, y2, x2 = map(float, key.replace(";", ",").split(","))
  # 创建一个多边形对象，表示矩形
  rect = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
  # 初始化一个标志变量，表示当前矩形是否与已有的矩形重叠
  overlap = False
  # 遍历已有的矩形列表
  for r in rect_list:
    # 判断当前矩形是否与某个已有的矩形相交，如果是，就将标志变量设为True，并且跳出循环
    if rect.intersects(r):
      overlap = True
      break
  # 如果标志变量为False，表示当前矩形不与任何已有的矩形重叠，就将其添加到矩形列表中
  if not overlap:
    rect_list.append(rect)

# 创建一个新字典，用来存储不重复的矩形的坐标点和计数器
new_rect_dict = {}

# 遍历不重复的矩形列表
for rect in rect_list:
  # 获取矩形的边界值，即最小和最大的经度和纬度值，并且转换成字符串格式，纬度在前，经度在后，用分号和逗号分隔
  key = ";".join(map(str, [rect.bounds[1], rect.bounds[0], rect.bounds[3], rect.bounds[2]]))
  # 获取原字典中对应键的值（即计数器），并且存储在新字典中
  new_rect_dict[key] = rect_dict[key]

# 导入csv模块，用来写入csv文件
import csv

# 打开一个csv文件，以写入模式，并且指定编码为utf-8
with open("output.csv", "w", encoding="utf-8") as f:
  # 创建一个csv写入对象w
  w = csv.writer(f)
  # 写入表头行，包括四个字段：左下角纬度、左下角经度、右上角纬度、右上角经度、对角线公里数、餐厅数量
  w.writerow(["ldy", "ldx", "ruy", "rux", "kilometers", "counts"])
  # 对新字典按值降序排序，返回一个列表，每个元素是一个键值对元组
  sorted_list = sorted(new_rect_dict.items(), key=lambda x: x[1], reverse=True)
  # 只保留前5个元素
  sorted_list = sorted_list[:3]
  # 遍历列表中的元素
  for item in sorted_list:
    # 获取键（即矩形的坐标点）和值（即计数器）
    key, value = item
    # 将键分割成四个坐标值，并且转换成浮点数
    y1, x1, y2, x2 = map(float, key.replace(";", ",").split(","))
    # 计算矩形的对角线长度，单位为公里，假设地球半径为6371公里，使用haversine公式
    import math
    dlon = math.radians(x2 - x1)
    dlat = math.radians(y2 - y1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(y1)) * math.cos(math.radians(y2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    diagonal = 6371 * c
    # 写入一行数据，包括四个坐标值、对角线长度和计数器
    w.writerow([y1, x1, y2, x2, diagonal, value])