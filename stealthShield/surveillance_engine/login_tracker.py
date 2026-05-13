# surveillance_engine/login_tracker.py
import subprocess
import platform
from datetime import datetime
import os
from alert_system.telegram_bot import send_alert

LOG_FILE = "logs/login_log.txt"

def track_logins():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    system = platform.system()

    if system == "Windows":
        result = subprocess.run(
            ['powershell', '-Command',
             'Get-EventLog -LogName Security -InstanceId 4624 -Newest 5 | Select-Object TimeGenerated, Message | Format-List'],
            capture_output=True, text=True
        )
        output = result.stdout if result.stdout else "No login events found (may need admin privileges)"
    else:
        result = subprocess.run(['last', '-n', '5'], capture_output=True, text=True)
        output = result.stdout

    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] Last 5 logins:\n{output}\n")
    send_alert(f"Last 5 logins:\n{output}")

if __name__ == "__main__":
    track_logins()
