import os
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from collections import defaultdict

def parse_gpx(file_path):
    # 同前，读取GPX文件
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespaces = [
        {'default': 'http://www.topografix.com/GPX/1/1'},
        {'default': 'http://www.topografix.com/GPX/1/0'}
    ]

    points = []
    for ns in namespaces:
        trkpts = root.findall('.//default:trkpt', ns)
        if trkpts:
            for trkpt in trkpts:
                lat = trkpt.get('lat')
                lon = trkpt.get('lon')
                ele_elem = trkpt.find('default:ele', ns)
                time_elem = trkpt.find('default:time', ns)

                ele = ele_elem.text if ele_elem is not None else None
                time_text = time_elem.text if time_elem is not None else None

                if time_text:
                    dt = datetime.fromisoformat(time_text.replace('Z', '+00:00'))
                    timestamp = int(dt.timestamp())
                else:
                    timestamp = None

                points.append({
                    'latitude': float(lat),
                    'longitude': float(lon),
                    'elevation': float(ele) if ele else None,
                    'timestamp': timestamp,
                    'timestamp_iso': time_text
                })
            break
    return points

def read_all_gpx_in_folder(folder_path):
    """读取文件夹内所有GPX文件，返回[filename, points]列表"""
    all_points = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.gpx'):
            file_path = os.path.join(folder_path, filename)
            points = parse_gpx(file_path)
            all_points.append([filename, points])
    return all_points

def date_of_point(timestamp):
    """根据时间戳得到东八区日期字符串：YYYYMMDD"""
    # 转为 UTC 时间
    dt_utc = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    # 转为东八区时间
    dt_cst = dt_utc + timedelta(hours=8)
    return dt_cst.strftime('%Y%m%d')

def save_gpx(file_path, points):
    """根据points列表保存成GPX文件"""
    gpx = ET.Element('gpx', version="1.1", creator="AutoMerger", xmlns="http://www.topografix.com/GPX/1/1")
    trk = ET.SubElement(gpx, 'trk')
    trkseg = ET.SubElement(trk, 'trkseg')

    for point in points:
        trkpt = ET.SubElement(trkseg, 'trkpt', lat=str(point['latitude']), lon=str(point['longitude']))
        if point['elevation'] is not None:
            ele = ET.SubElement(trkpt, 'ele')
            ele.text = str(point['elevation'])
        if point['timestamp_iso'] is not None:
            time_elem = ET.SubElement(trkpt, 'time')
            time_elem.text = point['timestamp_iso']

    tree = ET.ElementTree(gpx)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)

def merge_ori_into_dst(ori_folder, dst_folder):
    ori_files = read_all_gpx_in_folder(ori_folder)
    dst_files = read_all_gpx_in_folder(dst_folder)

    # 整理dst，按日期归类
    dst_by_date = defaultdict(list)  # date -> [(filename, points)]

    for filename, points in dst_files:
        if points:
            first_point = points[0]
            date = date_of_point(first_point['timestamp'])
            dst_by_date[date].append((filename, points))

    # 处理ori
    for ori_filename, ori_points in ori_files:
        for point in ori_points:
            point_date = date_of_point(point['timestamp'])

            if point_date not in dst_by_date:
                # 没有这一天，新建GPX
                new_gpx_name = f"{point_date}.gpx"
                new_gpx_path = os.path.join(dst_folder, new_gpx_name)
                print(f"创建新的GPX文件：{new_gpx_name}")
                save_gpx(new_gpx_path, [point])
                dst_by_date[point_date].append((new_gpx_name, [point]))
            else:
                # 已有这一天的文件，找合适的插入
                inserted = False
                candidates = dst_by_date[point_date]
                candidates.sort(key=lambda x: x[1][0]['timestamp'])  # 按开始时间排序

                for idx, (dst_filename, dst_points) in enumerate(candidates):
                    timestamps = [p['timestamp'] for p in dst_points]
                    if point['timestamp'] in timestamps:
                        inserted = True
                        break  # 已有相同点，跳过
                    if point['timestamp'] < timestamps[0]:
                        # 插入到最前
                        dst_points.insert(0, point)
                        inserted = True
                        break
                    if point['timestamp'] > timestamps[-1]:
                        # 可能还需要看下一个文件
                        continue
                    # 插入中间
                    for i in range(len(timestamps) - 1):
                        if timestamps[i] < point['timestamp'] < timestamps[i+1]:
                            dst_points.insert(i+1, point)
                            inserted = True
                            break
                    if inserted:
                        break

                if not inserted:
                    # 如果没插进去，就加到最末尾的文件
                    dst_by_date[point_date][-1][1].append(point)

    # 全部保存回去
    for date, filelist in dst_by_date.items():
        for filename, points in filelist:
            full_path = os.path.join(dst_folder, filename)
            points.sort(key=lambda x: x['timestamp'])
            save_gpx(full_path, points)

    print("合并完成！")


if __name__ == '__main__':
    ori = r"D:\image\yeah\gpx_out_freerecord"
    dst = r'D:\Mine\I_Drive\GPX_OUT'
    merge_ori_into_dst(ori, dst)
    
    # all_points = read_all_gpx_in_folder(dst)

    # print(f"共读取了 {len(all_points)} 个文件")
    # for filename, points in all_points:
    #     print(f"文件: {filename}，包含 {len(points)} 个点")
        # for point in points:
        #     print(point)

