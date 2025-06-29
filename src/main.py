# main.py
from pynput import keyboard as kb
import time
import cv2
import numpy as np

from config import NUM_QUADRADOS_GRID
from capture import (
    capture_wind1,
    capture_wind_decimal,
    capture_wind2,
    capture_angulo,
    capture_minimapa
)
from ocr_utils import ocr_read
from calculation import calcular_distancia

alvos = None

def selecionar_alvos(minimapa_path):
    img = cv2.imread(minimapa_path)
    pontos = []

    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            pontos.append((x, y))
            cor = (255,0,0) if len(pontos) == 1 else (0,0,255)
            cv2.circle(img, (x, y), 7, cor, 2)
            cv2.imshow('Selecione você (azul), depois o alvo (vermelho)', img)
            if len(pontos) == 2:
                cv2.line(img, pontos[0], pontos[1], (0,255,0), 2)
                cv2.imshow('Selecione você (azul), depois o alvo (vermelho)', img)

    cv2.imshow('Selecione você (azul), depois o alvo (vermelho)', img)
    cv2.setMouseCallback('Selecione você (azul), depois o alvo (vermelho)', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return pontos if len(pontos) == 2 else None

def capturar_dados():
    global alvos
    # 1) OCR do ângulo
    angulo_img = capture_angulo()
    angulo     = ocr_read(angulo_img, 'angulo')

    # 2) OCR do vento em 3 pedaços
    d1_img = capture_wind1()
    dot_img = capture_wind_decimal()
    d2_img = capture_wind2()

    d1   = ocr_read(d1_img,  'vento_digit')
    dot  = ocr_read(dot_img, 'vento_dot')
    d2   = ocr_read(d2_img,  'vento_digit')
    vento = f"{d1}{'.' if dot=='dot' else ''}{d2}" if d1 and d2 else d1 or d2 or "0"

    print(f"Ângulo: {angulo}, Vento: {vento}")

    # 3) Se alvos já definidos, calcule a distância em quadrados
    if alvos:
        px_azul, _         = alvos[0]
        px_vermelho, _     = alvos[1]
        minimap_img        = capture_minimapa()
        mm_w, _            = minimap_img.size

        dist_q = calcular_distancia(
            px_azul,
            px_vermelho,
            largura_grid_px=mm_w,
            num_quadrados=NUM_QUADRADOS_GRID
        )
        print(f"Distância: {dist_q:.2f} quadrados")
    else:
        print("Nenhum alvo definido. Pressione F7 para definir alvos.")

def definir_alvos():
    global alvos
    pil_minimap = capture_minimapa()
    img = cv2.cvtColor(np.array(pil_minimap), cv2.COLOR_RGB2BGR)

    pontos = []
    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            pontos.append((x, y))
            cor = (255,0,0) if len(pontos)==1 else (0,0,255)
            cv2.circle(img, (x,y), 5, cor, -1)
            if len(pontos)==2:
                cv2.line(img, pontos[0], pontos[1], (0,255,0), 2)
            cv2.imshow("Clique azul → vermelho", img)

    cv2.namedWindow("Clique azul → vermelho", cv2.WINDOW_NORMAL)
    cv2.imshow("Clique azul → vermelho", img)
    cv2.setMouseCallback("Clique azul → vermelho", click_event)
    cv2.waitKey(0)

    # substitua apenas esta linha:
    cv2.destroyAllWindows()

    if len(pontos)==2:
        alvos = pontos
        print(f"Alvos definidos: você={pontos[0]}, alvo={pontos[1]}")
    else:
        print("Nenhum ou número incorreto de cliques. Tente de novo.")
    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            pontos.append((x, y))
            cor = (255,0,0) if len(pontos)==1 else (0,0,255)
            cv2.circle(img, (x,y), 5, cor, -1)
            if len(pontos)==2:
                cv2.line(img, pontos[0], pontos[1], (0,255,0), 2)
            cv2.imshow("Clique azul → vermelho", img)

    cv2.namedWindow("Clique azul → vermelho", cv2.WINDOW_NORMAL)
    cv2.imshow("Clique azul → vermelho", img)
    cv2.setMouseCallback("Clique azul → vermelho", click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if len(pontos)==2:
        alvos = pontos
        print(f"Alvos definidos: você={pontos[0]}, alvo={pontos[1]}")
    else:
        print("Nenhum ou número incorreto de cliques. Tente de novo.")

def on_press(key):
    if key==kb.Key.f7:
        definir_alvos()
    elif key==kb.Key.f8:
        capturar_dados()

def main():
    print("F7=definir alvos, F8=capturar dados, ESC=sair")
    with kb.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
