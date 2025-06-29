# region_selector_click.py
from pynput import mouse

print("🖱️  REGISTRADOR DE REGIÃO VIA CLIQUE")
print("→ Clique com o botão ESQUERDO no canto SUPERIOR ESQUERDO da área desejada.")
print("→ Depois clique no canto INFERIOR DIREITO.")

coords = []

def on_click(x, y, button, pressed):
    if pressed:
        coords.append((x, y))
        print(f"✔️  Clique registrado: ({x}, {y})")
        if len(coords) == 2:
            print("\n📦 Coordenadas finais:")
            x1, y1 = coords[0]
            x2, y2 = coords[1]
            print(f"({x1}, {y1}, {x2}, {y2})  ← copie e cole no seu config.py como uma BOX")
            return False  # Para o listener

with mouse.Listener(on_click=on_click) as listener:
    listener.join()
