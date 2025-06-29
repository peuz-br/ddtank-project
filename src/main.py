import math
from pynput import keyboard as kb
from config import NUM_QUADRADOS_GRID
from capture import (
     
    capture_wind1,
    capture_wind_decimal,
    capture_wind2,
    capture_angulo,
    capture_minimapa
)
from ocr_utils import ocr_read
from calculation import calcular_distancia, ajustar_forca

alvos = []

def definir_alvos():
    img = capture_minimapa()
    # Isso é placeholder — substitua com lógica real de encontrar pixel do jogador e alvo
    print("⚠️  Função definir_alvos() precisa ser implementada com lógica de pixel do jogador/alvo.")
    alvos.clear()
    alvos.append((0, 0))
    alvos.append((100, 0))

def capturar_dados():
    wind1     = int(ocr_read(capture_wind1(), kind="digits"))
    wind_dec  = int(ocr_read(capture_wind_decimal(), kind="digits"))
    wind2     = int(ocr_read(capture_wind2(), kind="digits"))
    angulo    = int(ocr_read(capture_angulo(), kind="angle"))

    vento_total = wind1 + wind_dec * 0.1

    # isso é fictício — substitua com os pixels REAIS do jogador e do alvo
    px_jogador = 100
    px_alvo    = 300
    largura_grid_px = 400

    distancia = calcular_distancia(px_jogador, px_alvo, largura_grid_px, NUM_QUADRADOS_GRID)
    forca = ajustar_forca(distancia, angulo, vento_total)

    print(f"Ângulo: {angulo} | Vento: {vento_total:.1f} | Distância: {distancia:.2f} | Força sugerida: {forca}")

def on_press(key):
    try:
        if key == kb.Key.f7:

            definir_alvos()
            from minimap_utils import obter_posicoes
            jogador, inimigo = obter_posicoes()
            if jogador and inimigo:
                    print(f"Sua posição no minimapa (grid): {jogador}")
                    print(f"Inimigo mais distante (grid): {inimigo}")
                    distancia = math.dist(jogador, inimigo)
                    print(f"Distância estimada: {distancia:.2f}")
            else:
                     print("Jogador ou inimigo não detectado no minimapa.")
        elif key == kb.Key.f8:
            capturar_dados()
        elif key == kb.Key.esc:
            print("Encerrando…")
            return False
    except Exception as e:
        print("Erro durante execução:", e)

def main():
    print("🎯 Pressione F7 para definir alvos")
    print("💨 Pressione F8 para capturar vento e ângulo")
    print("🛑 Pressione ESC para sair")
    with kb.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
