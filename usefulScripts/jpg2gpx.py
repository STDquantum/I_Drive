import os
import piexif
import datetime
import collections
import gpxpy
import gpxpy.gpx
import random
import pytz

# 定义时区
TZ_UTC = pytz.utc
TZ_E8 = pytz.timezone('Asia/Shanghai')  # UTC+8
TZ_E9 = pytz.timezone('Asia/Tokyo')     # UTC+9
TZ_E3 = pytz.timezone('Europe/Moscow')  # UTC+3

# 特殊时段（本地时间，无需转换，直接比较 naive datetime）
SPECIAL_PERIODS = [
    (datetime.datetime(2019, 8, 3, 0, 0, 0), datetime.datetime(2019, 8, 9, 14, 0, 0), TZ_E9),
    (datetime.datetime(2025, 2, 7, 21, 0, 0), datetime.datetime(2025, 2, 17, 22, 0, 0), TZ_E3),
]

def get_exif(filepath):
    try:
        exif_dict = piexif.load(filepath)
        gps = exif_dict.get('GPS')
        datetime_original = exif_dict.get('Exif', {}).get(piexif.ExifIFD.DateTimeOriginal)
        if gps and datetime_original:
            return gps, datetime_original.decode()
    except Exception as e:
        print(f"Failed to read EXIF from {filepath}: {e}")
    return None, None

def dms_to_deg(dms, ref):
    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1]
    seconds = dms[2][0] / dms[2][1]
    deg = degrees + minutes / 60 + seconds / 3600
    if ref in ['S', 'W']:
        deg = -deg
    return deg

def parse_gps_info(gps_info):
    try:
        lat = dms_to_deg(gps_info[piexif.GPSIFD.GPSLatitude], gps_info[piexif.GPSIFD.GPSLatitudeRef].decode())
        lon = dms_to_deg(gps_info[piexif.GPSIFD.GPSLongitude], gps_info[piexif.GPSIFD.GPSLongitudeRef].decode())
        alt = 0
        if piexif.GPSIFD.GPSAltitude in gps_info:
            alt_value = gps_info[piexif.GPSIFD.GPSAltitude]
            alt = alt_value[0] / alt_value[1]
        return lat, lon, alt
    except Exception as e:
        print(f"Failed to parse GPS info: {e}")
    return None, None, None

def determine_timezone(local_dt):
    """
    根据拍摄时间选择正确时区
    local_dt: naive datetime（未带 tzinfo）
    """
    for start, end, tz in SPECIAL_PERIODS:
        if start <= local_dt <= end:
            return tz
    return TZ_E8  # 默认东八区

def collect_photos(directory, previous_data=collections.defaultdict(list)):
    data = previous_data  # key: date str (东八区日期), value: list of (UTC datetime, lat, lon, alt)
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(('.jpg', '.jpeg')):
                filepath = os.path.join(root, filename)
                gps_info, datetime_original = get_exif(filepath)
                if gps_info and datetime_original:
                    lat, lon, alt = parse_gps_info(gps_info)
                    if lat is not None and lon is not None:
                        try:
                            naive_dt = datetime.datetime.strptime(datetime_original, "%Y:%m:%d %H:%M:%S")
                            tz = determine_timezone(naive_dt)
                            local_dt = tz.localize(naive_dt)
                            utc_dt = local_dt.astimezone(TZ_UTC)

                            # 获取东八区日期作为 key
                            dt_in_e8 = utc_dt.astimezone(TZ_E8)
                            date_key = dt_in_e8.date().isoformat()

                            data[date_key].append((utc_dt, lat, lon, alt))
                        except Exception as e:
                            print(f"Failed to parse date/time from {filepath}: {e}")
    # 去重（按 UTC 时间 & 坐标去重）
    for date_key in data:
        data[date_key] = list(set(data[date_key]))
    return data

def add_fake_point(point):
    """
    给单个点增加一点小扰动生成第二个点
    """
    dt, lat, lon, alt = point
    new_dt = dt + datetime.timedelta(seconds=60)  # 时间扰动60秒
    lat_offset = 0.00050
    lon_offset = 0.00050
    new_lat = lat + lat_offset
    new_lon = lon + lon_offset
    if alt is not None:
        alt_offset = random.uniform(-1, 1)
        new_alt = alt + alt_offset
    else:
        new_alt = None
    return (new_dt, new_lat, new_lon, new_alt)

def write_gpx(date_key, points, output_dir):
    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    points.sort()  # 按 UTC 时间排序

    fake_point = add_fake_point(points[-1])
    points.append(fake_point)

    for dt, lat, lon, alt in points:
        pt = gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=alt, time=dt)
        gpx_segment.points.append(pt)

    output_path = os.path.join(output_dir, f"{date_key}.gpx")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(gpx.to_xml())

def main():
    image_dir = r"D:\image"
    image_dir_1 = r"E:\QQ空间备份_405720329"
    image_dir_2 = r"E:\image"
    output_dir = r"D:\image\yeah\gpx_output11"
    os.makedirs(output_dir, exist_ok=True)

    photo_data = collect_photos(image_dir)
    photo_data = collect_photos(image_dir_1, photo_data)
    photo_data = collect_photos(image_dir_2, photo_data)

    for date_key, points in photo_data.items():
        if points:
            write_gpx(date_key, points, output_dir)
            print(f"GPX file for {date_key} written with {len(points)} points.")

if __name__ == "__main__":
    main()
