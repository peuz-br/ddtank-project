from PIL import ImageGrab
import time

# Coordena­das que você mediu (ajuste se quiser testar variações)
X1, Y1, X2, Y2 = 478, 22, 521, 43

if __name__ == "__main__":
    print("Em 2 segundos vou capturar a região de vento...")
    time.sleep(2)
    # bhu­ga: bbox = (left, top, right, bottom)
    img = ImageGrab.grab(bbox=(X1, Y1, X2, Y2))
    img.save("test_vento_region.png")
    img.show()
    print("Teste salvo em test_vento_region.png")
