"""MoodTracker — 个人情绪追踪工具

用法:
    python moodtracker.py log       记录今天的心情
    python moodtracker.py history   查看最近 7 天记录
    python moodtracker.py stats     简单统计
"""

import sys
from datetime import datetime

from storage import load_records, save_records


def cmd_log():
    """记录一条情绪日志。"""
    print("--- 记录心情 ---")

    # 情绪分数 1-5
    while True:
        raw = input("情绪分数 (1=很低 2=低 3=一般 4=好 5=很好): ").strip()
        if raw in ("1", "2", "3", "4", "5"):
            mood = int(raw)
            break
        print("  请输入 1 到 5 之间的数字。")

    # 可选备注
    note = input("备注 (可直接回车跳过): ").strip()

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

    print(f"\n已保存! 日期 {record['date']} {record['time']}，情绪分数 {mood}/5")


def cmd_history():
    """查看最近 7 天记录。"""
    records = load_records()
    if not records:
        print("还没有任何记录。先用 `python moodtracker.py log` 记一条吧。")
        return

    print("--- 最近记录 ---\n")
    for r in records[-7:]:
        note = f"  {r['note']}" if r["note"] else ""
        print(f"  {r['date']} {r['time']}  {'█' * r['mood']}{'░' * (5 - r['mood'])}  {r['mood']}/5{note}")


def cmd_stats():
    """简单统计。"""
    records = load_records()
    if not records:
        print("还没有任何记录，无法统计。")
        return

    moods = [r["mood"] for r in records]
    avg = sum(moods) / len(moods)
    print("--- 统计 ---\n")
    print(f"  总记录数:  {len(records)}")
    print(f"  平均情绪:  {avg:.1f}/5")
    print(f"  最高:      {max(moods)}/5")
    print(f"  最低:      {min(moods)}/5")

    # 简单分布
    print("\n  分布:")
    for score in range(5, 0, -1):
        count = moods.count(score)
        bar = "█" * count
        print(f"    {score}/5  {bar} ({count})")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]
    if cmd == "log":
        cmd_log()
    elif cmd == "history":
        cmd_history()
    elif cmd == "stats":
        cmd_stats()
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
