# src/minimap_utils.py
import cv2
import numpy as np
from capture import capture_region
from config import MINIMAPA_BOX

# Cores BGR aproximadas para detectar as bolinhas
VERMELHO_BOLA = ([0, 0, 150], [80, 80, 255])
AZUL_BOLA = ([150, 0, 0], [255, 80, 80])


def detectar_bolas(imagem, cor_min, cor_max):
    mask = cv2.inRange(imagem, np.array(cor_min), np.array(cor_max))
    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return [cv2.boundingRect(c) for c in contornos if cv2.contourArea(c) > 5]


def converter_para_grid(coord_pixel):
    x1, y1, x2, y2 = MINIMAPA_BOX
    largura = x2 - x1
    altura = y2 - y1
    rel_x = coord_pixel[0] - x1
    rel_y = coord_pixel[1] - y1
    grid_x = int(rel_x / (largura / 15))
    grid_y = int(rel_y / (altura / 15))
    return (grid_x, grid_y)


def obter_posicoes():
    imagem = capture_region(MINIMAPA_BOX)

    bolas_vermelhas = detectar_bolas(imagem, *VERMELHO_BOLA)
    bolas_azuis = detectar_bolas(imagem, *AZUL_BOLA)

    todas_bolas = [(x + w // 2, y + h // 2) for (x, y, w, h) in bolas_vermelhas + bolas_azuis]

    if not todas_bolas:
        return None, None

    jogador = todas_bolas[0]
    inimigo = max(todas_bolas[1:], key=lambda p: abs(p[0] - jogador[0])) if len(todas_bolas) > 1 else None

    jogador_grid = converter_para_grid(jogador)
    inimigo_grid = converter_para_grid(inimigo) if inimigo else None

    return jogador_grid, inimigo_grid
