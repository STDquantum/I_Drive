# 还是处理不了中文！！！！
import subprocess
import json
import os

# 获取 Git 状态，找到已修改的 .gpx 文件
def get_modified_gpx_files():
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, encoding='utf-8')
    print(result.stdout.encode().decode())  # 调试输出
    files = []
    for line in result.stdout.splitlines():
        status, filepath = line[:2], line[3:]
        if filepath.lower().endswith('.gpx'):
            files.append(filepath)
    return files

# 载入 imported.json
def load_imported_json(path='imported.json'):
    if not os.path.exists(path):
        print(f"错误：{path} 文件不存在。")
        return []
    with open(path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"错误：{path} 不是合法的 JSON 文件。")
            return []
    return data

# 保存 imported.json
def save_imported_json(data, path='imported.json'):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    modified_files = get_modified_gpx_files()
    imported = load_imported_json()

    if not imported:
        print("没有数据，退出。")
        return

    imported_set = set(imported)
    changed = False

    for file in modified_files:
        file_basename = os.path.basename(file)
        if file_basename in imported_set:
            print(f"删除 imported.json 中的条目：{file_basename}")
            imported.remove(file_basename)
            changed = True
        else:
            print(f"警告：{file_basename} 不在 imported.json 中")

    if changed:
        save_imported_json(imported)
        print("imported.json 已更新。")
    else:
        print("imported.json 无需更改。")

if __name__ == '__main__':
    main()
