import pyautogui
from config import DDTANK_TOPLEFT_X, DDTANK_TOPLEFT_Y
from config import WIND1_BOX, WIND_DECIMAL_BOX, WIND2_BOX, ANGULO_BOX, MINIMAPA_BOX

def screenshot(region):
    x1,y1,x2,y2 = region
    return pyautogui.screenshot(region=(
        DDTANK_TOPLEFT_X + x1,
        DDTANK_TOPLEFT_Y + y1,
        x2 - x1,
        y2 - y1))

def capture_wind1():        return screenshot(WIND1_BOX)
def capture_wind_decimal(): return screenshot(WIND_DECIMAL_BOX)
def capture_wind2():        return screenshot(WIND2_BOX)
def capture_angulo():       return screenshot(ANGULO_BOX)
def capture_minimapa():     return screenshot(MINIMAPA_BOX)
