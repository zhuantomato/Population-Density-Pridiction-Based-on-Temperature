'''
Author: Ruijie Ni 1924975712@qq.com
Date: 2023-04-11 13:46:33
LastEditors: Ruijie Ni 1924975712@qq.com
LastEditTime: 2023-04-11 14:32:35
FilePath: \Population-Density-Pridiction-Based-on-Temperature\Modelling\DataPreprocess\CenterPoints.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# 定义经纬度范围
beijing_bounds = ['39.914614,116.446179;39.924614,116.456179', '39.987258,116.479573;39.997258,116.489573', '39.875608,116.461821;39.885608,116.471821']
guiyang_bounds = ['26.58033,106.715074;26.59033,106.725074', '26.581553,106.702252;26.591553,106.712252', '26.595023,106.706234;26.605023,106.716234']
haerbin_bounds = ['45.76729,126.619968;45.77729,126.629968', '45.762358,126.650482;45.772358,126.660482', '45.75104,126.65113;45.76104,126.66113']
haikou_bounds = ['20.030734,110.317357;20.040734,110.327357', '20.034288,110.347809;20.044288,110.357809', '20.038505,110.336464;20.048505,110.346464']


# 定义函数，用于计算经纬度范围的中心点
def calculate_center(bounds):
    # 将字符串经纬度分割为两个列表
    left_bottom_lng_lat = bounds.split(';')[0].split(',')
    right_top_lng_lat = bounds.split(';')[1].split(',')
    # 计算中心点经纬度
    center_lng = (float(left_bottom_lng_lat[0]) + float(right_top_lng_lat[0])) / 2
    center_lat = (float(left_bottom_lng_lat[1]) + float(right_top_lng_lat[1])) / 2
    # 保留小数点后6位
    center_lng = round(center_lng, 6)
    center_lat = round(center_lat, 6)
    # 返回中心点经纬度
    return center_lng, center_lat

# 定义列表，用于存放各城市中心点经纬度
beijing_center_list = []
guiyang_center_list = []
haerbin_center_list = []
haikou_center_list = []

# 计算北京经纬度范围的中心点
for bounds in beijing_bounds:
    beijing_center_list.append(calculate_center(bounds))
# 计算贵阳经纬度范围的中心点
for bounds in guiyang_bounds:
    guiyang_center_list.append(calculate_center(bounds))
# 计算哈尔滨经纬度范围的中心点
for bounds in haerbin_bounds:
    haerbin_center_list.append(calculate_center(bounds))
# 计算海口经纬度范围的中心点
for bounds in haikou_bounds:
    haikou_center_list.append(calculate_center(bounds))

# 打印中心点经纬度列表
print(beijing_center_list)
print(guiyang_center_list)
print(haerbin_center_list)
print(haikou_center_list)