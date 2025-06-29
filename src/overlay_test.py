import time
import numpy as np
import cv2
from PIL import ImageGrab, Image as PILImage

# Ajuste aqui para os valores que estão em config.py
X1, Y1, X2, Y2 = 478, 21, 521, 43

if __name__ == "__main__":
    print("Você terá 2 segundos para posicionar o DDTank em primeiro plano...")
    time.sleep(2)  # ←←← delay de 2 segundos

    # Captura a tela inteira após o delay
    screen = np.array(ImageGrab.grab())
    # Converte para BGR (OpenCV)
    screen_bgr = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    # Desenha retângulo em vermelho na região do vento
    cv2.rectangle(screen_bgr, (X1, Y1), (X2, Y2), (0, 0, 255), 2)
    # Converte de volta para RGB e salva
    screen_rgb = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2RGB)
    overlay = PILImage.fromarray(screen_rgb)
    overlay.save("vento_box_overlay.png")
    print(">> vento_box_overlay.png criado com overlay após 2s de delay.")
