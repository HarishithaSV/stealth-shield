# surveillance_engine/process_monitor.py
import psutil
import time
from datetime import datetime
import os
from alert_system.telegram_bot import send_alert

LOG_FILE = "logs/process_log.txt"
known_pids = set()

# 🔴 ADD THIS (ignore system processes)
IGNORE_PROCESSES = [
    "system",
    "system idle process",
    "svchost.exe",
    "lsass.exe",
    "csrss.exe",
    "wininit.exe",
    "winlogon.exe",
    "services.exe",
    "registry",
    "smss.exe"
]

def log_process(proc):
    process_name = proc.name().lower()

    # 🔴 FILTER HERE (VERY IMPORTANT)
    if process_name in IGNORE_PROCESSES:
        return

    log_msg = f"[{datetime.now()}] New process: {proc.pid} - {proc.name()}"

    with open(LOG_FILE, "a") as f:
        f.write(log_msg + "\n")

    send_alert(f"⚙️ New process detected: {proc.name()} (PID {proc.pid})")


def monitor_processes():
    global known_pids
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    while True:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.pid not in known_pids:
                known_pids.add(proc.pid)
                log_process(proc)

        time.sleep(5)


if __name__ == "__main__":
    monitor_processes()