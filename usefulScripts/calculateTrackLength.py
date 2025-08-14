import gpxpy
from geopy.distance import geodesic

def calculate_track_length(gpx_data: str) -> float:
    """
    Calculate the total length of a GPX track in meters.
    
    :param gpx_data: GPX data as a string.
    :return: Total length of the track in meters.
    """
    gpx = gpxpy.parse(gpx_data)
    total_length = 0.0
    
    for track in gpx.tracks:
        for segment in track.segments:
            for i in range(len(segment.points) - 1):
                point1 = segment.points[i]
                point2 = segment.points[i + 1]
                # Calculate distance between two points
                distance = geodesic((point1.latitude, point1.longitude), (point2.latitude, point2.longitude)).meters
                total_length += distance

    
    return total_length

file = r"GPX_OUT\20250729-143225.gpx"
with open(file, 'r', encoding='utf-8') as f:
    gpx_data = f.read()
length = calculate_track_length(gpx_data)
print(f"Total track length: {length:.2f} meters")