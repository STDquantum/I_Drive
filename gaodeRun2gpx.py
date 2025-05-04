import sqlite3
import json
import math
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

# ========= 坐标转换相关 =========

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

# ========= 像素转经纬度 =========

def pixelsToLatLon(j, j2, i=20):
    d = 4.007501668557849e7 / ((1 << i) * 256)
    y = 1.5707963267948966 - (math.atan(math.exp(-(2.0037508342789244e7 - (j2 * d)) / 6378137.0)) * 2.0)
    y = y * 57.29577951308232
    x = (((j * d) - 2.0037508342789244e7) / 6378137.0)
    x = x * 57.29577951308232
    return (x, y)

# ========= 时间处理 =========

def timestamp_to_iso8601(ts):
    local_dt = datetime.fromtimestamp(ts, tz=timezone(timedelta(hours=8)))
    utc_dt = local_dt.astimezone(timezone.utc)
    return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def timestamp_to_local_filename(ts):
    local_dt = datetime.fromtimestamp(ts, tz=timezone(timedelta(hours=8)))
    return local_dt.strftime("%Y%m%d_%H%M%S")

# ========= GPX生成 =========

def create_gpx(points, start_ts, output_dir):
    gpx = ET.Element('gpx', version="1.1", creator="RunGPXExporter", xmlns="http://www.topografix.com/GPX/1/1")
    trk = ET.SubElement(gpx, 'trk')
    name = ET.SubElement(trk, 'name')
    name.text = f"Run {start_ts}"
    trkseg = ET.SubElement(trk, 'trkseg')

    for lon, lat, time_iso8601 in points:
        trkpt = ET.SubElement(trkseg, 'trkpt', lat=str(lat), lon=str(lon))
        time_elem = ET.SubElement(trkpt, 'time')
        time_elem.text = time_iso8601

    tree = ET.ElementTree(gpx)
    os.makedirs(output_dir, exist_ok=True)
    filename = timestamp_to_local_filename(start_ts) + ".gpx"
    output_path = os.path.join(output_dir, filename)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"GPX文件已保存：{output_path}")

# ========= 主程序 =========

def main():
    db_path = r"E:\download\com.autonavi.minimap\databases\aMap.db"
    output_dir = r"gpx_output_run"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT RUN_POI FROM run_table")
    rows = cursor.fetchall()

    for row in rows:
        a = row[0]
        if not a:
            continue
        try:
            point_list = json.loads(json.loads(a)["pointList"])
        except Exception as e:
            print(f"解析失败：{e}")
            continue

        gpx_points = []
        start_ts = None

        ori_x, ori_y = 0, 0
        for point in point_list:
            x = point.get("x")
            y = point.get("y")
            if len(gpx_points) == 0:
                ori_x = x
                ori_y = y
            else:
                x = x + ori_x
                y = y + ori_y
            ts = point.get("PointTime")  # 秒时间戳

            if x is None or y is None or ts is None:
                continue

            lon_gcj, lat_gcj = pixelsToLatLon(x, y)
            lon_wgs, lat_wgs = gcj02_to_wgs84(lon_gcj, lat_gcj)

            if start_ts is None:
                start_ts = ts

            time_iso8601 = timestamp_to_iso8601(ts)
            gpx_points.append((lon_wgs, lat_wgs, time_iso8601))

        if gpx_points and start_ts:
            create_gpx(gpx_points, start_ts, output_dir)

    conn.close()

if __name__ == "__main__":
    main()
