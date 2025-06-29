import pytesseract
import cv2
import numpy as np
import os
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ----------------------------
# 1) Pré-carrega os templates
# ----------------------------
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets')
templates = {}
for name in [str(d) for d in range(10)] + ['dot']:
    path = os.path.join(TEMPLATE_DIR, f"{name}.png")
    tpl = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if tpl is None:
        raise FileNotFoundError(f"Template {name}.png não encontrado em {path}")
    templates[name] = tpl

# ---------------------------------------------------
# 2) Definição dos offsets (em pixels) dentro da VENTO_BOX
# ---------------------------------------------------
# Ajuste estes valores até cada caixinha cobrir só o seu caractere no HUD
_d1_x1, _d1_x2 = 0, 12      # primeiro dígito
_dot_x1, _dot_x2 = 12, 18   # ponto
_d2_x1, _d2_x2 = 18, 37     # segundo dígito




def read_angle(pil_img):
    """
    OCR para ângulo: threshold fixo e PSM 7, whitelist de dígitos.
    Método 100% estável conforme antes.
    """
    # converte PIL → escala de cinza OpenCV
    img_cv = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2GRAY)
    _, bin_img = cv2.threshold(img_cv, 120, 255, cv2.THRESH_BINARY)
    # OCR configurado apenas para dígitos
    config = '--psm 7 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(bin_img, config=config).strip()
    # filtra apenas caracteres numéricos
    filtered = ''.join(c for c in text if c.isdigit())
    return filtered or "0"

# Carrega templates ao importar o módulo
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets')
print(">> TEMPLATE_DIR =", TEMPLATE_DIR)
print(">> Conteúdo de assets:", os.listdir(TEMPLATE_DIR))
templates = {}
for name in [str(d) for d in range(10)] + ['dot']:
    path = os.path.join(TEMPLATE_DIR, f"{name}.png")
    tpl = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if tpl is None:
        raise FileNotFoundError(f"Template {name}.png não encontrado em {path}")
    templates[name] = tpl

def read_wind(pil_img):
    # 1) converte PIL → BGR → cinza
    img_bgr  = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    gray     = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    hsv      = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # 2) isola vermelho em HSV
    lower1, upper1 = np.array([0,70,50]),   np.array([10,255,255])
    lower2, upper2 = np.array([170,70,50]), np.array([180,255,255])
    mask = cv2.inRange(hsv, lower1, upper1) | cv2.inRange(hsv, lower2, upper2)

    # 3) limpa ruídos
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)

    # 4) aplica no canal cinza e binariza
    isolated = cv2.bitwise_and(gray, gray, mask=mask)
    _, bin_img = cv2.threshold(isolated, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 5) encontra contornos dos caracteres
    contours, _ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # filtra por área mínima (descarta ruídos)
    boxes = [cv2.boundingRect(c) for c in contours if cv2.contourArea(c) > 50]
    if not boxes:
        return "0"

    # 6) ordena caixas por posição X
    boxes = sorted(boxes, key=lambda b: b[0])

    result = ""
    for x, y, w, h in boxes:
        char_img = gray[y:y+h, x:x+w]
        # para cada template (0-9 e dot), faz match
        best, best_val = "", 0
        for k, tpl in templates.items():
            # pula se tpl for maior
            th, tw = tpl.shape
            if th>h or tw>w: continue
            res = cv2.matchTemplate(char_img, tpl, cv2.TM_CCOEFF_NORMED)
            val = res.max()
            if val > best_val:
                best_val, best = val, k
        # só aceita matches fortes
        if best_val >= 0.85:
            result += "." if best=="dot" else best

    return result or "0"

    def match_char(img_region, keys):
        """
        varre só os templates em `keys` (lista de nomes em templates),
        retorna o primeiro cujo max(res) ≥ 0.9.
        """
        for k in keys:
            tpl = templates[k]
            th, tw = tpl.shape
            # pula templates maiores
            if th>img_region.shape[0] or tw>img_region.shape[1]:
                continue
            res = cv2.matchTemplate(img_region, tpl, cv2.TM_CCOEFF_NORMED)
            if res.max() >= 0.9:
                return k
        return ''

    # primeiro dígito: só 0–9
    d1 = match_char(d1_img, [str(i) for i in range(10)])
    # ponto: só dot
    dot = match_char(dot_img, ['dot'])
    # segundo dígito: só 0–9
    d2 = match_char(d2_img, [str(i) for i in range(10)])

    # monta o vento final
    if d1 and d2:
        return f"{d1}{'.' if dot=='dot' else ''}{d2}"
    # fallback simples
    return d1 or d2 or "0"

def ocr_read(img, tipo):
    if tipo == 'angulo':
        return read_angle(img)
    elif tipo == 'vento':
        return read_wind(img)
    return "0"
