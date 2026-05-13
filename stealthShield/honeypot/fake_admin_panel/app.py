import sys
import os
import json
from collections import defaultdict
from alert_system.telegram_bot import send_alert

# Fix paths regardless of where the script is called from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '..', '..')))

from flask import Flask, request, render_template
from datetime import datetime
from alert_system.telegram_bot import send_alert

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "honeypot_log.txt")

login_attempts = defaultdict(list)
THRESHOLD = 3

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("🔥 LOGIN ATTEMPT DETECTED")
        username = request.form.get('username')
        password = request.form.get('password')
        ip = request.remote_addr
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_agent = request.headers.get('User-Agent', 'Unknown')

        login_attempts[ip].append(timestamp)
        attempt_count = len(login_attempts[ip])

        log_data = {
            "timestamp": timestamp,
            "ip": ip,
            "username": username,
            "password": password,
            "user_agent": user_agent,
            "attempt_count": attempt_count
        }

        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(log_data) + "\n")

        alert_msg = f"🚨 Honeypot Alert!\nIP: {ip}\nUser: {username}\nPassword: {password}\nAgent: {user_agent}"
        if attempt_count >= THRESHOLD:
            alert_msg += f"\n⚠️ Multiple attempts from same IP ({attempt_count}x)"
            print("📩 Sending Telegram alert...")
            send_alert(alert_msg)
            print("✅ Alert sent!")


    return render_template('login.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
