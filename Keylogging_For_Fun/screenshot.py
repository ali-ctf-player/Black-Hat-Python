


import platform
import time
from datetime import datetime
import os


SCREENSHOT_DIR = "screenshots"
INTERVAL = 30

def create_screenshot_dir():
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)


def take_screenshot():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{SCREENSHOT_DIR}/screenshot_{timestamp}.png"

    try:
        if platform.system() == "Windows":
            import pyautogui
            pyautogui.screenshot(filename)

        else:
            os.system(f"scrot -q 80 {filename}")
        print(f"[+] Saved: {filename}")
    except Exception as e:
        print(f"[-] Error: {e}")


if __name__ == "__main__":
    create_screenshot_dir()
    while True:
        take_screenshot()
        time.sleep(INTERVAL)
