import glob
import os
from math import radians, sin, cos, sqrt
from datetime import datetime
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 地球半径，单位为公里
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) * sin(dlat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) * sin(dlon / 2)
    c = 2 * math.atan2(sqrt(a), sqrt(1 - a))
    d = R * c  # 两点之间的距离
    return d

def get_speed_from_geo_info(lat1, lon1, lat2, lon2, time1, time2):
    distance = haversine(lat1, lon1, lat2, lon2)
    time_gap = time2 - time1
    speed = distance / time_gap * 3600
    return speed

if __name__ == '__main__':
    csv_list = glob.glob("/Users/akiyo/Library/Mobile Documents/com~apple~CloudDocs/Document/驾驶/驾驶记录/*.csv")
    csv_path = "/Users/akiyo/Library/Mobile Documents/com~apple~CloudDocs/Document/驾驶/驾驶记录/20231123_kyoto_vellfire.csv"
    
    geo_info = []
    new_csv_path = csv_path.replace('.csv', '_analyze.csv')

    with open(csv_path, mode='r') as f:
        context = f.readlines()
        context.pop(0)     
        for i, line in enumerate(context):
            lat, lon, time = line.split(',')
            lat, lon, time = float(lat), float(lon), time
            time = datetime.strptime(time.strip(), '%Y-%m-%d %H:%M:%S %z')
            timestamp = time.timestamp()
            if i == 0:
                speed = 0
                acceleration = 0
            else:
                lat0, lon0, timestamp0, speed0, _ = geo_info[i - 1]
                #lat2, lon2, time2, speed2, _ = geo_info[i]
                try:
                    speed = int(get_speed_from_geo_info(lat0, lon0, lat, lon, timestamp0, timestamp))
                    acceleration = (speed - speed0)/(timestamp - timestamp0)
                except ZeroDivisionError:
                    speed = speed0
                    acceleration = 0
                
            geo_info.append([lat, lon, timestamp, speed, acceleration])


    with open(new_csv_path, mode='w') as f:
        for i, (lat, lon, time, speed, acceleration) in enumerate(geo_info):
            if i == 0:
                line = f.write('latitude,longitude,time,speed,acceleration\n')
            elif i < len(geo_info) - 1:
                str_time = datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
                if i % 10 == 0:
                #if True:
                    f.write(f"{lat},{lon},{str_time},{speed},{acceleration}\n")

