
from serpent.utilities import is_windows,display_serpent_logo
import ctypes

print(is_windows())
print(display_serpent_logo())

import win32gui
import pyautogui,time
import pyperclip
VK_J = 0x4A
ad = 1
time.sleep(2)
print("kaishi ")
while True:

    ad += 1


    # pyautogui.press('j')

    # 按下J按键
    ctypes.windll.user32.keybd_event(VK_J, 0, 0, 0)

    # 释放J按键
    ctypes.windll.user32.keybd_event(VK_J, 0, 2, 0)

    time.sleep(0.2)
    print("B a ", ad)
    if ad > 200:
        break
jj