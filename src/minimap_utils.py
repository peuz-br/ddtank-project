import cv2
import numpy as np
from PIL import ImageGrab
from config import MINIMAPA_BOX


def capturar_minimapa():
    x1, y1, x2, y2 = MINIMAPA_BOX
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    img_np = np.array(img)
    return img_np


def detectar_bolinhas_minimapa(imagem):
    hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    lower_red1 = np.array([0, 150, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 150, 50])
    upper_red2 = np.array([180, 255, 255])
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)

    bolinhas = []
    for color, mask in [("azul", mask_blue), ("vermelho", mask_red)]:
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            (x, y), raio = cv2.minEnclosingCircle(cnt)
            if 2 < raio < 10:
                bolinhas.append((int(x), int(y), raio, color))

    return bolinhas


def identificar_jogador(bolinhas):
    return max(bolinhas, key=lambda b: b[2], default=None)


def identificar_inimigo(bolinhas, jogador):
    if jogador is None:
        return None
    jx, jy = jogador[0], jogador[1]
    restantes = [b for b in bolinhas if b != jogador]
    if not restantes:
        return None
    return max(restantes, key=lambda b: (b[0]-jx)**2 + (b[1]-jy)**2)


def obter_posicoes():
    imagem = capturar_minimapa()
    bolinhas = detectar_bolinhas_minimapa(imagem)
    jogador = identificar_jogador(bolinhas)
    inimigo = identificar_inimigo(bolinhas, jogador)
    return jogador, inimigo