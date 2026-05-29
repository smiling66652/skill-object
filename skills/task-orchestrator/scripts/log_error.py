#!/usr/bin/env python3
"""
错误日志生成器 - 用于 task-orchestrator 技能
用法: python log_error.py <task_id> <subtask> <error_summary> [manual_fix]
"""
import os, sys, json
from datetime import datetime

task_id = sys.argv[1] if len(sys.argv) > 1 else "unknown"
subtask = sys.argv[2] if len(sys.argv) > 2 else "unknown"
error_summary = sys.argv[3] if len(sys.argv) > 3 else "No details"
manual_fix = sys.argv[4] if len(sys.argv) > 4 else "手动检查并重试"

log_dir = os.path.expanduser("~/.workbuddy/logs/task-errors")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"{task_id}.log")

entry = {
    "timestamp": datetime.now().isoformat(),
    "task_id": task_id,
    "subtask": subtask,
    "error": error_summary,
    "manual_fix": manual_fix
}

with open(log_file, "a", encoding="utf-8") as f:
    f.write(f"[ERROR] {entry['timestamp']} - {task_id} - {subtask}\n")
    f.write(f"  错误: {error_summary}\n")
    f.write(f"  操作指导: {manual_fix}\n")
    f.write(f"  ---\n")

print(f"错误已记录: {log_file}")
