import requests
import json
import csv
import time
import io
import sys

#改变标准输出的默认编码
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
ak = "pfARyIAcUfrGjnhtf2E4qKZOG4lXOUpG"
bounds = "39.905,116.371;39.909,116.377"
filename = "traffic_data.csv"
interval = 10 * 60
duration = 10#24 * 60 * 60
start_time = time.time()

with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["fetch_time", "road_name", "road_length", "road_speed", "congestion_status"])
    while time.time() < start_time + duration:
        url = f"http://api.map.baidu.com/traffic/v1/bound?ak={ak}&bounds={bounds}&coord_type_input=gcj02&coord_type_output=gcj02"
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            if data["status"] == 0:
                fetch_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                for road in data["road_traffic"]:
                    road_name = road["road_name"]
                    road_length = road["length"]
                    road_speed = road["speed"]
                    congestion_status = road["congestion_status"]
                    writer.writerow([fetch_time, road_name, road_length, road_speed, congestion_status])
                print(f"Data saved successfully. Current time: {fetch_time}. Next fetch time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + interval))}")
            else:
                print(f"Data fetch failed. Error message: {data['message']}. Error code: {data['status']}")
        else:
            print(f"Request failed. Error message: {response.text}. Status code: {response.status_code}")
        #time.sleep(interval)
f.close()