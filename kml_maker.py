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

def generate_specified_color_levels(color1: int, color2: int, num: 16):
    pass


def generate_route_line(geo_info):
    route_string_info = f"""
	<Placemark>
    	<Style id="route">
			<LineStyle>
				<color>ffffffff</color>
				<width>5</width>
			</LineStyle>
		</Style>
		<name>Route</name>
			<LineString>
            	<styleUrl>#route</styleUrl>
				<tessellate>1</tessellate>
				<coordinates>
        """
    for i, (lat, lon, time, speed, acceleration) in enumerate(geo_info):   
        route_string_info += f"{lon},{lat},0 "
        if i % 3 == 0:
            route_string_info += "\n"
    route_string_info += """
                </coordinates>
			</LineString>
	</Placemark>
        """
    return route_string_info
    

def generate_speed_sampling_placemark(geo_info, sampling_interval=50):
    speed_string_info = """
	<Folder>
		<name>Speed</name>
		<Style>
			<ListStyle>
				<listItemType>checkHideChildren</listItemType>
				<maxSnippetLines>2</maxSnippetLines>
			</ListStyle>
		</Style>
    """
	
    for i, (lat, lon, time, speed, acceleration) in enumerate(geo_info):
        style_id = str(int(speed / 10) * 10)
        
        if i == 0:
            init_time = time
        elif sampling_interval > 0 and i % sampling_interval == 0:
            speed_string_info += f"""
            <Placemark>
                <name>{speed}km/h</name>
                <styleUrl>#kmh{style_id}</styleUrl>
                <description>
                    Idx: {i}
                    Timestamp: {datetime.fromtimestamp(time).strftime('%H:%M:%S')}
                    During: {datetime.fromtimestamp(time - init_time).strftime('%H:%M:%S')}
                    Speed: {speed}km/h
                    Acceleration: {acceleration}m/s2
                </description>
                <Point>
                    <gx:drawOrder>1</gx:drawOrder>
                    <coordinates>{lon},{lat},0</coordinates>
                </Point>
            </Placemark>
            """
    speed_string_info += """
	</Folder>
    """

    return speed_string_info

def write_to_kml(route_name, kml_path, route_string_info, speed_string_info, acceleration_string_info=None):
    kml_string_info = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<name>{route_name}</name>
	<open>1</open>
	<Style id="kmh0">
		<IconStyle><color>ffFFFFFF</color><scale>0.5</scale><Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon></IconStyle>
		<LabelStyle><scale>0.5</scale></LabelStyle>
	</Style>
	<Style id="kmh10">
		<IconStyle><scale>0.5</scale><color>ffF8F1FF</color><Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon></IconStyle>
		<LabelStyle><scale>0.5</scale></LabelStyle>
	</Style>
	<Style id="kmh20">
		<IconStyle><scale>0.5</scale><color>ffF1E4FF</color><Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon></IconStyle>
		<LabelStyle><scale>0.5</scale></LabelStyle>
	</Style>
	<Style id="kmh30">
		<IconStyle><scale>0.5</scale><color>ffE9D8FF</color><Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon></IconStyle>
		<LabelStyle><scale>0.5</scale></LabelStyle>
	</Style>
	<Style id="kmh40">
		<IconStyle><scale>0.5</scale><color>ffE2CBFF</color><Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon></IconStyle>
		<LabelStyle><scale>0.5</scale></LabelStyle>
	</Style>
	<Style id="kmh50">
		<IconStyle><scale>0.5</scale><color>ffDABEFF</color><Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon></IconStyle>
		<LabelStyle><scale>0.5</scale></LabelStyle>
	</Style>
	<Style id="kmh60">
		<IconStyle><scale>0.5</scale><color>ffD3B2FF</color><Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon></IconStyle>
		<LabelStyle><scale>0.5</scale></LabelStyle>
	</Style>
	<Style id="kmh70">
		<IconStyle><scale>0.5</scale><color>ffCCA5FF</color><Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon></IconStyle>
		<LabelStyle><scale>0.5</scale></LabelStyle>
	</Style>
	<Style id="kmh80">
		<IconStyle><scale>0.5</scale><color>ffC59AFF</color><Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon></IconStyle>
		<LabelStyle><scale>0.5</scale></LabelStyle>
	</Style>
	<Style id="kmh90">
		<IconStyle><scale>0.5</scale><color>ffBD8DFF</color><Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon></IconStyle>
		<LabelStyle><scale>0.5</scale></LabelStyle>
	</Style>
	<Style id="kmh100">
		<IconStyle><scale>0.5</scale><color>ffB680FF</color><Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon></IconStyle>
		<LabelStyle><scale>0.5</scale></LabelStyle>
	</Style>
	<Style id="kmh110">
		<IconStyle><scale>0.5</scale><color>ffAE73FF</color><Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon></IconStyle>
		<LabelStyle><scale>0.5</scale></LabelStyle>
	</Style>
	<Style id="kmh120">
		<IconStyle><scale>0.5</scale><color>ffA666FF</color><Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon></IconStyle>
		<LabelStyle><scale>0.5</scale></LabelStyle>
	</Style>
	<Style id="kmh130">
		<IconStyle><scale>0.5</scale><color>ff9F59FF</color><Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon></IconStyle>
		<LabelStyle><scale>0.5</scale></LabelStyle>
	</Style>
	<Style id="kmh140">
		<IconStyle><scale>0.5</scale><color>ff984DFF</color><Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon></IconStyle>
		<LabelStyle><scale>0.5</scale></LabelStyle>
	</Style>
	<Style id="kmh150">
		<IconStyle><scale>0.5</scale><color>ff9040FF</color><Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon></IconStyle>
		<LabelStyle><scale>0.5</scale></LabelStyle>
	</Style>
    """

    kml_string_info += route_string_info
    kml_string_info += speed_string_info
    kml_string_info += acceleration_string_info if acceleration_string_info else ""
    kml_string_info += """
</Document>
</kml>
    """
    with open(kml_path, 'w+') as f:
        f.write(kml_string_info)
    
    print(kml_path)
    print("Finish writing to kml file.")


if __name__ == '__main__':
    csv_path = "/Users/akiyo/Library/Mobile Documents/com~apple~CloudDocs/Document/驾驶/驾驶记录/20230930_kyoto.csv"
    basename = os.path.basename(csv_path).split('.')[0]
    output_path = "/Users/akiyo/Desktop/20230930_kyoto.kml"

    geo_info = []

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


    route_string_info = generate_route_line(geo_info)
    speed_string_info = generate_speed_sampling_placemark(geo_info)
    write_to_kml(basename, output_path, route_string_info, speed_string_info)