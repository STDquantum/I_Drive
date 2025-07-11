a = ""
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import math 

# 地球常量
PI = math.pi
AXIS = 6378245.0  # 长半轴
EE = 0.006693421622965943  # 扁率平方

def out_of_china(lat, lon):
    # 判断是否在中国范围外
    if lon < 72.004 or lon > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False

def transform_lat(x, y):
    ret = -100.0 + 2.0*x + 3.0*y + 0.2*y*y + 0.1*x*y + 0.2*math.sqrt(abs(x))
    ret += (20.0*math.sin(6.0*x*PI) + 20.0*math.sin(2.0*x*PI)) * 2.0/3.0
    ret += (20.0*math.sin(y*PI) + 40.0*math.sin(y/3.0*PI)) * 2.0/3.0
    ret += (160.0*math.sin(y/12.0*PI) + 320*math.sin(y*PI/30.0)) * 2.0/3.0
    return ret

def transform_lon(x, y):
    ret = 300.0 + x + 2.0*y + 0.1*x*x + 0.1*x*y + 0.1*math.sqrt(abs(x))
    ret += (20.0*math.sin(6.0*x*PI) + 20.0*math.sin(2.0*x*PI)) * 2.0/3.0
    ret += (20.0*math.sin(x*PI) + 40.0*math.sin(x/3.0*PI)) * 2.0/3.0
    ret += (150.0*math.sin(x/12.0*PI) + 300.0*math.sin(x/30.0*PI)) * 2.0/3.0
    return ret

def gcj02_to_wgs84(lon, lat):
    if out_of_china(lat, lon):
        return lon, lat
    dlat = transform_lat(lon - 105.0, lat - 35.0)
    dlon = transform_lon(lon - 105.0, lat - 35.0)
    radlat = lat / 180.0 * PI
    magic = math.sin(radlat)
    magic = 1 - EE * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((AXIS * (1 - EE)) / (magic * sqrtmagic) * PI)
    dlon = (dlon * 180.0) / (AXIS / sqrtmagic * math.cos(radlat) * PI)
    mglat = lat + dlat
    mglon = lon + dlon
    return lon * 2 - mglon, lat * 2 - mglat

# 解析数据
points = []
for entry in a.strip(';').split(';'):
    fields = entry.split(',')
    time_str = fields[0]
    lon = float(fields[1])
    lat = float(fields[2])
    lon, lat = gcj02_to_wgs84(lon, lat)  # 坐标系转换！
    # 东八区转UTC
    time_local = datetime.strptime(time_str, "%Y%m%d%H%M%S")
    time_utc = time_local - timedelta(hours=8)
    points.append((lat, lon, time_utc))

# 生成GPX XML
gpx = ET.Element('gpx', version="1.1", creator="Generated by Script", xmlns="http://www.topografix.com/GPX/1/1")
trk = ET.SubElement(gpx, 'trk')
trkseg = ET.SubElement(trk, 'trkseg')

for lat, lon, time_utc in points:
    trkpt = ET.SubElement(trkseg, 'trkpt', lat=str(lat), lon=str(lon))
    time_elem = ET.SubElement(trkpt, 'time')
    time_elem.text = time_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

# 文件名，用第一个点的本地时间
first_time_local = datetime.strptime(points[0][2].strftime("%Y%m%d%H%M%S"), "%Y%m%d%H%M%S") + timedelta(hours=8)
file_name = first_time_local.strftime("%Y%m%d%H%M%S") + ".gpx"

# 保存到文件
tree = ET.ElementTree(gpx)
tree.write(file_name, encoding='utf-8', xml_declaration=True)

print(f"GPX文件已生成：{file_name}")