import os
import gpxpy
import gpxpy.gpx
from datetime import datetime, timezone, timedelta
from collections import defaultdict

def parse_gpx(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        gpx = gpxpy.parse(f)
    return gpx

def read_all_gpx_in_folder(folder_path):
    """读取文件夹内所有GPX文件，返回[filename, gpx对象]列表"""
    all_gpxs = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.gpx'):
            file_path = os.path.join(folder_path, filename)
            gpx = parse_gpx(file_path)
            all_gpxs.append([filename, gpx])
    return all_gpxs

def first_point_time(segment):
    """取Segment第一个点的时间"""
    for point in segment.points:
        if point.time:
            return point.time
    return None

def date_of_point(time_point):
    """根据时间戳得到东八区日期字符串：YYYYMMDD"""
    if time_point is None:
        return None
    dt_utc = time_point.replace(tzinfo=timezone.utc)
    dt_cst = dt_utc + timedelta(hours=8)
    return dt_cst.strftime('%Y%m%d')

def save_gpx(file_path, gpx):
    """保存gpx对象"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(gpx.to_xml())

def merge_ori_into_dst(ori_folder, dst_folder):
    ori_files = read_all_gpx_in_folder(ori_folder)
    dst_files = read_all_gpx_in_folder(dst_folder)

    dst_by_date = defaultdict(list)  # date -> [(filename, gpx对象)]

    for filename, gpx in dst_files:
        for track in gpx.tracks:
            for segment in track.segments:
                time_point = first_point_time(segment)
                if time_point:
                    date = date_of_point(time_point)
                    if date:
                        dst_by_date[date].append((filename, gpx))
                        break  # 一个track里只用第一个segment的第一个时间决定

    for ori_filename, ori_gpx in ori_files:
        for track in ori_gpx.tracks:
            for segment in track.segments:
                time_point = first_point_time(segment)
                if time_point is None:
                    continue
                point_date = date_of_point(time_point)

                if point_date not in dst_by_date:
                    # 创建新文件
                    new_gpx = gpxpy.gpx.GPX()
                    new_track = gpxpy.gpx.GPXTrack(name=track.name)
                    new_segment = gpxpy.gpx.GPXTrackSegment()
                    new_segment.points = segment.points
                    new_track.segments.append(new_segment)
                    new_gpx.tracks.append(new_track)

                    new_gpx_name = f"{point_date}.gpx"
                    new_gpx_path = os.path.join(dst_folder, new_gpx_name)
                    print(f"创建新的GPX文件：{new_gpx_name}")
                    save_gpx(new_gpx_path, new_gpx)
                    dst_by_date[point_date].append((new_gpx_name, new_gpx))
                else:
                    # 已有这天的文件，找合适的位置插入
                    for track in ori_gpx.tracks:
                        for segment in track.segments:
                            for point in segment.points:
                                if not point.time:
                                    continue
                                point_date = date_of_point(point.time)

                                if point_date not in dst_by_date:
                                    # 创建新的GPX文件
                                    new_gpx = gpxpy.gpx.GPX()
                                    new_track = gpxpy.gpx.GPXTrack(name=track.name)
                                    new_segment = gpxpy.gpx.GPXTrackSegment()
                                    new_segment.points.append(point)
                                    new_track.segments.append(new_segment)
                                    new_gpx.tracks.append(new_track)

                                    new_gpx_name = f"{point_date}.gpx"
                                    new_gpx_path = os.path.join(dst_folder, new_gpx_name)
                                    print(f"创建新的GPX文件：{new_gpx_name}")
                                    save_gpx(new_gpx_path, new_gpx)
                                    dst_by_date[point_date].append((new_gpx_name, new_gpx))
                                else:
                                    # 已有这天的文件，找合适的地方插入这个点
                                    inserted = False
                                    candidates = dst_by_date[point_date]
                                    candidates.sort(key=lambda x: first_point_time(x[1].tracks[0].segments[0]))  # 按开始时间排序

                                    for idx, (dst_filename, dst_gpx) in enumerate(candidates):
                                        dst_track = dst_gpx.tracks[0]
                                        dst_segment = dst_track.segments[0]
                                        timestamps = [p.time for p in dst_segment.points if p.time]

                                        if point.time in timestamps:
                                            inserted = True
                                            break  # 有相同时间点，跳过

                                        if point.time < timestamps[0]:
                                            # 插到最前
                                            dst_segment.points.insert(0, point)
                                            inserted = True
                                            break

                                        if point.time > timestamps[-1]:
                                            continue  # 继续找下一个文件

                                        for i in range(len(timestamps) - 1):
                                            if timestamps[i] < point.time < timestamps[i+1]:
                                                dst_segment.points.insert(i+1, point)
                                                inserted = True
                                                break
                                        if inserted:
                                            break

                                    if not inserted:
                                        # 没插进去，加到最后一个文件的最后
                                        dst_filename, dst_gpx = candidates[-1]
                                        dst_track = dst_gpx.tracks[0]
                                        dst_segment = dst_track.segments[0]
                                        dst_segment.points.append(point)


    # 保存所有文件
    for date, filelist in dst_by_date.items():
        for filename, gpx in filelist:
            full_path = os.path.join(dst_folder, filename)
            save_gpx(full_path, gpx)

    print("合并完成！")

if __name__ == '__main__':
    ori = r"D:\image\yeah\gpx_output"
    dst = r'D:\Mine\I_Drive\GPX_OUT'
    merge_ori_into_dst(ori, dst)
