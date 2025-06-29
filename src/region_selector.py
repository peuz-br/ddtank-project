# region_selector4.py
import time
import cv2
import numpy as np
from PIL import ImageGrab

def select_region(name):
    print(f">>> Posicione o DDTank e em 1s abre o ROI para '{name}'")
    time.sleep(1)
    screen = np.array(ImageGrab.grab())
    screen_bgr = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    roi = cv2.selectROI(name, screen_bgr, showCrosshair=True, fromCenter=False)
    cv2.destroyAllWindows()
    x, y, w, h = roi
    print(f"  → {name} = (X={x}, Y={y}, W={w}, H={h})\n")
    return x, y, w, h

if __name__ == "__main__":
    # 1ª caixinha: primeiro dígito do vento
    w1_x, w1_y, w1_w, w1_h = select_region("Wind Digit 1")
    # 2ª caixinha: ponto decimal
    wd_x, wd_y, wd_w, wd_h = select_region("Wind Decimal Point")
    # 3ª caixinha: segundo dígito do vento
    w2_x, w2_y, w2_w, w2_h = select_region("Wind Digit 2")
    # 4ª caixinha: mostrador de ângulo completo
    a_x,  a_y,  a_w,  a_h  = select_region("Angle Dial")

    print("Agora cole em config.py (substituindo as regiões antigas):\n")
    print(f"WIND1_BOX       = ({w1_x}, {w1_y}, {w1_x+w1_w}, {w1_y+w1_h})")
    print(f"WIND_DECIMAL_BOX= ({wd_x}, {wd_y}, {wd_x+wd_w}, {wd_y+wd_h})")
    print(f"WIND2_BOX       = ({w2_x}, {w2_y}, {w2_x+w2_w}, {w2_y+w2_h})")
    print(f"ANGULO_BOX      = ({a_x},  {a_y},  {a_x+a_w},  {a_y+a_h})")
