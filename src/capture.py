

import pyautogui
from config import DDTANK_TOPLEFT_X, DDTANK_TOPLEFT_Y
from config import WIND1_BOX, WIND_DECIMAL_BOX, WIND2_BOX, ANGULO_BOX, MINIMAPA_BOX

def screenshot_region(region_box):
    x1, y1, x2, y2 = region_box
    return pyautogui.screenshot(region=(DDTANK_TOPLEFT_X + x1,
                                        DDTANK_TOPLEFT_Y + y1,
                                        x2 - x1,
                                        y2 - y1))

def capture_wind1():
    return screenshot_region(WIND1_BOX)

def capture_wind_decimal():
    return screenshot_region(WIND_DECIMAL_BOX)

def capture_wind2():
    return screenshot_region(WIND2_BOX)

def capture_angulo():
    return screenshot_region(ANGULO_BOX)

def capture_minimapa():
    return screenshot_region(MINIMAPA_BOX)