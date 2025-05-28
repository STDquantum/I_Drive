import gpxpy
from datetime import timedelta

# 读取 GPX 文件
input_file = r'GPX_OUT\20250528.gpx'
output_file = 'GPX_OUT\\20250508健步_adjusted.gpx'
output_file = input_file[:-4] + "_adjusted.gpx"

f = open(input_file, 'r', encoding='utf-8')
gpx = gpxpy.parse(f)
f.close()

gpx.creator = 'miHealth'

# 遍历所有轨迹点，修改时间
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            if point.time:
                # 减去 8 小时
                point.time = (point.time - timedelta(hours=8)).replace(microsecond=0)

# 保存修改后的 GPX
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(gpx.to_xml())
