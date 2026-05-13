import multiprocessing
import os
import sys

# Ensure the working directory is the stealthShield folder so all relative imports work
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)

from alert_system.telegram_bot import send_alert
from usb_monitor import monitor_usb
from surveillance_engine.file_watchdog import monitor_directory
from surveillance_engine.login_tracker import track_logins
from surveillance_engine.process_monitor import monitor_processes

def start_honeypot():
    os.chdir(BASE_DIR)
    sys.path.insert(0, BASE_DIR)
    try:
        print("[+] Starting Honeypot on http://0.0.0.0:8080 ...")
        from honeypot.fake_admin_panel.app import app
        print("[+] Honeypot Flask app loaded. Visit http://localhost:8080")
        app.run(host="0.0.0.0", port=8080, use_reloader=False, debug=False)
    except Exception as e:
        import traceback
        print(f"[!] Honeypot Error: {e}")
        traceback.print_exc()

def safe_start(module_function, name):
    # Re-apply path fix inside each subprocess (needed on Windows)
    os.chdir(BASE_DIR)
    sys.path.insert(0, BASE_DIR)
    try:
        print(f"[+] Starting {name}...")
        module_function()
    except Exception as e:
        print(f"[!] Error in {name}: {e}")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    os.makedirs("logs", exist_ok=True)
    print("[*] StealthShield: Initializing Modules...\n")

    try:
        p1 = multiprocessing.Process(target=safe_start, args=(monitor_processes, "Process Monitor"))
        p2 = multiprocessing.Process(target=safe_start, args=(monitor_directory, "File Watchdog"))
        p3 = multiprocessing.Process(target=start_honeypot)
        p4 = multiprocessing.Process(target=safe_start, args=(track_logins, "Login Tracker"))
        p5 = multiprocessing.Process(target=safe_start, args=(monitor_usb, "USB Monitor"))

        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()

        print("[*] All modules started. Press Ctrl+C to stop.\n")

        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()

    except KeyboardInterrupt:
        print("\n[!] Shutting down StealthShield...")
        for p in [p1, p2, p3, p4, p5]:
            p.terminate()
        sys.exit(0)

    except Exception as e:
        print(f"[!] Critical Error: {e}")
        sys.exit(1)
