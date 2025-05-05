import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import math

# 坐标系转换参数
PI = math.pi
AXIS = 6378245.0
EE = 0.006693421622965943

def out_of_china(lat, lon):
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

# 主程序
base_folder = r"E:\download\com.autonavi.minimap\files\content_value\track_record\track_detail"
output_folder = "gpx_output"
os.makedirs(output_folder, exist_ok=True)

# 统一存储所有点，准备按时间统一排
all_points = []

# 遍历所有轨迹文件夹
for folder_name in os.listdir(base_folder):
    folder_path = os.path.join(base_folder, folder_name)
    if not os.path.isdir(folder_path):
        continue

    try:
        # 读取info.txt或info.json
        info_path_txt = os.path.join(folder_path, "info.txt")
        info_path_json = os.path.join(folder_path, "info.json")
        info_path = info_path_json if os.path.exists(info_path_json) else info_path_txt
        
        with open(info_path, "r", encoding="utf-8") as f:
            info_content = f.read()
            info_json = json.loads(info_content)

        line_info = info_json["lineInfo"]
        end_time = line_info["endTime"]
        eta_time = line_info["etaTime"]

        # 修正beginTime
        begin_time = end_time - eta_time * 1000

        # 读取轨迹点
        lines_path = os.path.join(folder_path, "lines", "1.txt")
        with open(lines_path, "r", encoding="utf-8") as f:
            points_str = f.read()

        points = []
        for entry in points_str.strip(';').split(';'):
            if entry:
                lon, lat = map(float, entry.split(','))
                lon, lat = gcj02_to_wgs84(lon, lat)
                points.append((lat, lon))

        if len(points) < 2:
            print(f"跳过 {folder_name}，轨迹点不足2个。")
            continue

        # 时间计算
        start_time = datetime.utcfromtimestamp(begin_time / 1000.0)
        final_time = datetime.utcfromtimestamp(end_time / 1000.0)
        if start_time > final_time:
            start_time, final_time = final_time, start_time

        total_seconds = (final_time - start_time).total_seconds()
        interval = total_seconds / (len(points) - 1)

        # 保存每个点及其对应时间
        for idx, (lat, lon) in enumerate(points):
            point_time = start_time + timedelta(seconds=interval * idx)
            all_points.append((point_time, lat, lon))

        print(f"提取轨迹成功：{folder_name}")

    except Exception as e:
        print(f"处理 {folder_name} 出错：{e}")

# 按时间排序所有点
all_points.sort(key=lambda x: x[0])

# 创建最终GPX文件
gpx = ET.Element('gpx', version="1.1", creator="Merged by Script", xmlns="http://www.topografix.com/GPX/1/1")
trk = ET.SubElement(gpx, 'trk')
trkseg = ET.SubElement(trk, 'trkseg')

for point_time, lat, lon in all_points:
    trkpt = ET.SubElement(trkseg, 'trkpt', lat=str(lat), lon=str(lon))
    time_elem = ET.SubElement(trkpt, 'time')
    time_elem.text = point_time.strftime("%Y-%m-%dT%H:%M:%SZ")

# 保存输出
output_path = os.path.join(output_folder, "merged_tracks_one_seg.gpx")
tree = ET.ElementTree(gpx)
tree.write(output_path, encoding='utf-8', xml_declaration=True)

print(f"\n所有轨迹点已按时间合并成一个轨迹段，文件位置：{output_path}")
