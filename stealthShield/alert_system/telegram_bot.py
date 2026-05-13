import os
import requests
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }

    try:
        response = requests.post(url, data=payload)
        print("📡 Telegram response:", response.text)

    except Exception as e:
        print(f"❌ Failed to send alert: {e}")


def send_video(video_path, caption="🎥 Motion Captured"):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"

    try:
        with open(video_path, 'rb') as video:

            files = {'video': video}

            data = {
                'chat_id': CHAT_ID,
                'caption': caption
            }

            response = requests.post(url, files=files, data=data)
            response.raise_for_status()

    except Exception as e:
        print(f"Failed to send video: {e}")