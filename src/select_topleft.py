import time
import cv2
import numpy as np
from PIL import ImageGrab

def select_region(name):
    print(f">>> Em 1s abre a seleção para '{name}'. Coloque o jogo em foco.")
    time.sleep(1)
    screen = np.array(ImageGrab.grab())
    screen_bgr = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    roi = cv2.selectROI(name, screen_bgr, showCrosshair=True, fromCenter=False)
    cv2.destroyAllWindows()
    x, y, w, h = roi
    print(f"{name}: X={x}, Y={y}, W={w}, H={h}")
    return x, y, w, h

if __name__ == "__main__":
    # Selecione aqui **a janela inteira do jogo DDTank**
    gx, gy, gw, gh = select_region("Selecione a janela DO JOGO")
    print("\n>>> Cole em config.py:\n")
    print(f"DDTANK_TOPLEFT_X = {gx}")
    print(f"DDTANK_TOPLEFT_Y = {gy}")
