import win32gui as w32
import ctypes
from PIL import ImageGrab
import time
import numpy as np
import os
import win32api
import win32con


try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    ctypes.windll.user32.SetProcessDPIAware()

def press_jump(window_name):
    # Sends a "Spacebar" key down and key up signal
    hwnd = w32.FindWindow(None, window_name)
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
    time.sleep(0.05)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_SPACE, 0)

def get_window_pixels(window_name):
    hwnd = w32.FindWindow(None, window_name)
    if not hwnd:
        print("Window not found!")
        return None

    x, y = w32.ClientToScreen(hwnd, (0, 0))

    left, top, right, bottom = w32.GetClientRect(hwnd)

    bbox = (x, y, x + right, y + bottom)

    img = ImageGrab.grab(bbox).convert('L')
    img = img.resize((128,128))
    observation = np.array(img)/255.0

    return observation

def get_and_reset_reward(file_path):
    reward = 0
    if os.path.exists(file_path):
        try:
            # 1. Read the score
            with open(file_path, "r") as f:
                content = f.read().strip()
                if content:
                    reward = float(content)
            
            # 2. Reset the file to 0 if we found a score
            if reward > 0:
                with open(file_path, "w") as f:
                    f.write("0")
        except PermissionError:
            # Game is currently writing to the file, skip this frame
            return 0
    return reward

