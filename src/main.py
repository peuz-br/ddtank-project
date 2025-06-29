from pynput import keyboard as kb
import cv2
import numpy as np
from config import NUM_QUADRADOS_GRID
from capture import (
    capture_wind1, capture_wind_decimal, capture_wind2,
    capture_angulo, capture_minimapa
)
from ocr_utils import ocr_read
from calculation import calcular_distancia

alvos = []

def definir_alvos():
    global alvos
    # mostra só o minimapa para clique
    pil = capture_minimapa()
    img = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
    pts = []
    def on_click(evt,x,y,flags,_) :
        if evt==cv2.EVENT_LBUTTONDOWN:
            pts.append((x,y))
            cv2.circle(img,(x,y),5,(0,0,255),-1)
    cv2.namedWindow("Alvos"); cv2.setMouseCallback("Alvos",on_click)
    cv2.imshow("Alvos",img); cv2.waitKey(0); cv2.destroyAllWindows()
    if len(pts)==2:
        alvos=pts; print("Alvos:",pts)
    else:
        print("Clique dois pontos (você e inimigo).")

def capturar_dados():
    if not alvos:
        print("Pressione F7 para definir alvos primeiro."); return
    # OCR
    ang   = ocr_read(capture_angulo(), "angulo")
    d1    = ocr_read(capture_wind1(),  "vento")
    dot   = ocr_read(capture_wind_decimal(),"vento")
    d2    = ocr_read(capture_wind2(),  "vento")
    vento = f"{d1}{'.' if dot=='dot' else ''}{d2}"
    # Distância
    (ax,_),(bx,_) = alvos
    mm_w,_ = capture_minimapa().size
    dist   = calcular_distancia(ax, bx, mm_w, NUM_QUADRADOS_GRID)
    print(f"Ângulo: {ang}, Vento: {vento}, Distância: {dist:.2f} quad.")
    
def on_press(key):
    if key==kb.Key.f7: definir_alvos()
    if key==kb.Key.f8: capturar_dados()
    if key==kb.Key.esc: return False

def main():
    print("F7=alvos, F8=tirar dados, ESC=sair")
    with kb.Listener(on_press=on_press): kb.Listener.join()

if __name__=="__main__":
    main()
