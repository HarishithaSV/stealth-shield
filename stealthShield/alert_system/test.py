import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from alert_system.telegram_bot import send_alert

send_alert("TEST MESSAGE 🚀")
print("Alert sent successfully!")