# -*- coding: utf-8 -*-

"""
更新data.db中缺失的起始点（location_country）和终止点（ending_point_pos）
脚本会检查所有记录，对于缺失位置的记录，从对应的GPX文件中读取坐标，
然后使用Nominatim地理编码器来获取位置名称。
"""

import os
import sqlite3
import time
import random
import string
from typing import Tuple, Optional

import geopy
from geopy.geocoders import Nominatim
import polyline

# 配置
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_FILE = os.path.join(parent_dir, "run_page", "data.db")

# 初始化地理编码器
def randomword():
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(4))

geopy.geocoders.options.default_user_agent = "my-application"
geocoder = Nominatim(user_agent=randomword())


def get_coords_from_polyline(summary_polyline: str) -> Optional[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """
    从summary_polyline解码起始点和终止点的坐标。
    返回：((start_lat, start_lon), (end_lat, end_lon))
    """
    try:
        if not summary_polyline:
            return None
        
        # 解码polyline，返回 [(lat, lon), ...]
        coords = polyline.decode(summary_polyline)
        
        if len(coords) < 2:
            print(f"警告: polyline中坐标点不足2个")
            return None
        
        start_lat, start_lon = coords[0]
        end_lat, end_lon = coords[-1]
        
        return ((start_lat, start_lon), (end_lat, end_lon))
    except Exception as e:
        print(f"错误: 无法解析polyline: {e}")
        return None


def get_location_name(lat: float, lon: float, retry_count: int = 2) -> str:
    """
    通过坐标获取地名。
    """
    for attempt in range(retry_count):
        try:
            location = geocoder.reverse(f"{lat}, {lon}", language="zh-CN")
            return str(location.address)
        except Exception as e:
            if attempt < retry_count - 1:
                print(f"  重试 ({attempt + 1}/{retry_count})...")
                time.sleep(1)  # 等待后重试
            else:
                print(f"  警告: 无法获取地名 ({lat}, {lon}): {e}")
                return ""
    return ""


def update_missing_locations():
    """
    更新data.db中缺失的起始点和终止点。
    """
    print(f"连接到数据库: {SQL_FILE}")
    conn = sqlite3.connect(SQL_FILE)
    cursor = conn.cursor()
    
    # 查询缺失起始点或终止点的记录
    cursor.execute("""
        SELECT run_id, name, summary_polyline FROM activities 
        WHERE (location_country IS NULL OR location_country = '') 
           OR (ending_point_pos IS NULL OR ending_point_pos = '')
        ORDER BY run_id DESC
    """)
    
    records = cursor.fetchall()
    print(f"\n找到 {len(records)} 条记录需要更新\n")
    
    if not records:
        print("没有需要更新的记录")
        conn.close()
        return
    
    updated_count = 0
    
    for i, (run_id, name, summary_polyline) in enumerate(records, 1):
        print(f"[{i}/{len(records)}] 处理: run_id={run_id}, name={name}")
        
        if not summary_polyline:
            print(f"  summary_polyline为空，跳过")
            continue
        
        # 从polyline中获取坐标
        coords = get_coords_from_polyline(summary_polyline)
        if not coords:
            print(f"  无法从polyline中提取坐标")
            continue
        
        start_coords, end_coords = coords
        start_location = ""
        end_location = ""
        
        # 获取起始点地名
        cursor.execute("SELECT location_country FROM activities WHERE run_id = ?", (run_id,))
        result = cursor.fetchone()
        current_location = result[0] if result and result[0] else ""
        
        if not current_location:
            print(f"  获取起始点地名 ({start_coords[0]}, {start_coords[1]})...")
            start_location = get_location_name(start_coords[0], start_coords[1])
            if start_location:
                print(f"  起始点: {start_location}")
        else:
            print(f"  起始点已有: {current_location}")
            start_location = current_location
        
        # 获取终止点地名
        cursor.execute("SELECT ending_point_pos FROM activities WHERE run_id = ?", (run_id,))
        result = cursor.fetchone()
        current_ending = result[0] if result and result[0] else ""
        
        if not current_ending:
            print(f"  获取终止点地名 ({end_coords[0]}, {end_coords[1]})...")
            end_location = get_location_name(end_coords[0], end_coords[1])
            if end_location:
                print(f"  终止点: {end_location}")
        else:
            print(f"  终止点已有: {current_ending}")
            end_location = current_ending
        
        # 更新数据库
        if start_location or end_location:
            cursor.execute("""
                UPDATE activities 
                SET location_country = ?, ending_point_pos = ?
                WHERE run_id = ?
            """, (start_location or current_location, end_location or current_ending, run_id))
            updated_count += 1
            print(f"  ✓ 已更新")
        
        # 限制请求频率，避免触发速率限制
        time.sleep(0.5)
    
    conn.commit()
    conn.close()
    
    print(f"\n完成！共更新 {updated_count} 条记录")


if __name__ == "__main__":
    update_missing_locations()
