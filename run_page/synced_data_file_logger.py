import os
from config import SYNCED_FILE
import json


def save_synced_data_file_list(file_list: list):
    old_list = load_synced_file_list()

    with open(SYNCED_FILE, "w", encoding="utf-8") as f:
        file_list.extend(old_list)

        json.dump(file_list, f, indent=4, ensure_ascii=False)


def load_synced_file_list():
    if os.path.exists(SYNCED_FILE):
        with open(SYNCED_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception as e:
                print(f"json load {SYNCED_FILE} \nerror {e}")
                pass

    return []
