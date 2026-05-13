import requests

# Replace with your actual token and chat_id
BOT_TOKEN = "8665578250:AAGFgJUFMPE1BeX8TvM4_97ljIDgmEAS1TY"
CHAT_ID = "1341672672"

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        print("📡 Telegram response:", response.text)   # 👈 ADD THIS
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")

def send_video(video_path, caption="🎥 Motion Captured"):
    url = f"https://api.telegram.org/bot8665578250:AAGFgJUFMPE1BeX8TvM4_97ljIDgmEAS1TY/sendVideo"
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
