"""数据存储模块 — 手机端版本

数据存在 App 用户目录下，兼容 Android 沙盒权限。
"""

import json
import os


def get_data_file():
    """返回数据文件路径，兼容桌面和 Android。"""
    # Android 上 user_data_dir 由 Kivy App 提供
    try:
        from kivy.app import App
        app = App.get_running_app()
        if app and hasattr(app, "user_data_dir"):
            data_dir = app.user_data_dir
        else:
            raise Exception("no running app")
    except Exception:
        # 桌面环境 fallback
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "records.json")


def load_records():
    """读取全部记录。"""
    path = get_data_file()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_records(records):
    """保存全部记录。"""
    path = get_data_file()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def add_record(mood, note=""):
    """新增一条记录，返回新记录。"""
    from datetime import datetime
    now = datetime.now()
    record = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "mood": mood,
        "note": note,
    }
    records = load_records()
    records.append(record)
    save_records(records)
    return record
