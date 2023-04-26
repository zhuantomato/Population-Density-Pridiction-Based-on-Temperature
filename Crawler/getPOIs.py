#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from urllib.parse import quote
from urllib import request
import json
import xlwt
import io
import sys

#改变标准输出的默认编码
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
amap_web_key = 'd7620288fea4be1bf89de3d32c0bf3b4'

poi_search_url = "http://restapi.amap.com/v3/place/text"
poi_boundary_url = "https://ditu.amap.com/detail/get/detail"

# cityname is the city name of the POI to be crawled, 
# city_areas is the administrative area under the city,
# classes is the set of multiple POI categories.
cityname = '贵阳市'
city_areas = ['花溪区']
classes = ['050000']

# Get poi data based on city name and category keywords
def getpois(cityname, keywords):
    i = 1
    poilist = []
    while True:  # using while to continuous getting data
        result = getpoi_page(cityname, keywords, i)
        print(result)
        result = json.loads(result)  # convert string to json
        if result['count'] == '0':
            break
        hand(poilist, result)
        i = i + 1
    return poilist


# Write to excel
def write_to_excel(poilist, cityname, classfield):
    # A Workbook object, which is equivalent to creating an Excel file
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(classfield, cell_overwrite_ok=True)

    # Headings
    sheet.write(0, 0, 'x')
    sheet.write(0, 1, 'y')
    sheet.write(0, 2, 'count')
    sheet.write(0, 3, 'name')
    sheet.write(0, 4, 'address')
    sheet.write(0, 5, 'adname')


    for i in range(len(poilist)):
        location = poilist[i]['location']
        name = poilist[i]['name']
        address = poilist[i]['address']
        adname = poilist[i]['adname']
        lng = str(location).split(",")[0]
        lat = str(location).split(",")[1]

        # #location transform
        # result = gcj02_to_wgs84(float(lng), float(lat))
        # lng = result[0]
        # lat = result[1]

        # Writing in line
        sheet.write(i + 1, 0, lng)
        sheet.write(i + 1, 1, lat)
        sheet.write(i + 1, 2, 1)
        sheet.write(i + 1, 3, name)
        sheet.write(i + 1, 4, address)
        sheet.write(i + 1, 5, adname)

    book.save(r'' + cityname + "_" + classfield + '.xls')


# store returned poi data
def hand(poilist, result):
    # result = json.loads(result)  # turning string to json
    pois = result['pois']
    for i in range(len(pois)):
        poilist.append(pois[i])


# get pois in a single page
def getpoi_page(cityname, keywords, page):
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&types=' + quote(
        keywords) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    '''req_url = "https://restapi.amap.com/v3/place/around?key=" + amap_web_key + "&location=116.473168,39.993015&radius=10000&types=011100"'''
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data

# #Get in district
# for clas in classes:
#     classes_all_pois = []
#     for area in city_areas:
#         pois_area = getpois(area, clas)
#         print('District：' + str(area) + ', Class：' + str(clas) + ", Total:" + str(len(pois_area)) + "data length")
#         classes_all_pois.extend(pois_area)
#     print("Summary of all district：" + str(len(classes_all_pois)))
#     write_to_excel(classes_all_pois, cityname, clas)
#     print('================Class：'  + str(clas) + "Success")


#Get in city
for clas in classes:
    classes_all_pois = []
    pois_area = getpois(cityname, clas)
    classes_all_pois.extend(pois_area)
    print("数据总数为：" + str(len(classes_all_pois)))
    write_to_excel(classes_all_pois, cityname, clas)
    print('================分类：'  + str(clas) + "写入成功")

