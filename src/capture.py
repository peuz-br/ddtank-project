import time
import pyautogui
import pygetwindow as gw
from config import (
    WINDOW_TITLE,
    WIND1_BOX,
    WIND_DECIMAL_BOX,
    WIND2_BOX,
    ANGULO_BOX,
    MINIMAPA_BOX
)

from PIL import ImageGrab
import numpy as np

def capture_region(box):
    """Captura uma região da tela definida por (x1, y1, x2, y2)."""
    img = ImageGrab.grab(bbox=box)
    return np.array(img)

def activate_window():
    wins = gw.getWindowsWithTitle(WINDOW_TITLE)
    if not wins:
        raise RuntimeError(f"Janela '{WINDOW_TITLE}' não encontrada")
    win = wins[0]
    if win.isMinimized:
        win.restore()
    win.activate()
    time.sleep(0.15)

def get_window_offset():
    wins = gw.getWindowsWithTitle(WINDOW_TITLE)
    if not wins:
        raise RuntimeError(f"Janela '{WINDOW_TITLE}' não encontrada")
    win = wins[0]
    return win.left, win.top

def box_to_region(box):
    x1, y1, x2, y2 = box
    win_left, win_top = get_window_offset()
    left   = int(win_left + min(x1, x2))
    top    = int(win_top  + min(y1, y2))
    width  = int(abs(x2 - x1))
    height = int(abs(y2 - y1))
    return (left, top, width, height)

def capture_wind1():
    activate_window()
    return pyautogui.screenshot(region=box_to_region(WIND1_BOX))

def capture_wind_decimal():
    activate_window()
    return pyautogui.screenshot(region=box_to_region(WIND_DECIMAL_BOX))

def capture_wind2():
    activate_window()
    return pyautogui.screenshot(region=box_to_region(WIND2_BOX))

def capture_angulo():
    activate_window()
    return pyautogui.screenshot(region=box_to_region(ANGULO_BOX))

def capture_minimapa():
    activate_window()
    return pyautogui.screenshot(region=box_to_region(MINIMAPA_BOX))