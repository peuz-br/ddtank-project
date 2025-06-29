import cv2
import numpy as np
import os

# Carrega somente uma vez, ao importar
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets')
templates = {}
for name in [str(d) for d in range(10)] + ['dot']:
    path = os.path.join(TEMPLATE_DIR, f"{name}.png")
    tpl  = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if tpl is None:
        raise FileNotFoundError(f"{name}.png não encontrado em {path}")
    templates[name] = tpl

def read_angle(pil_img):
    """OCR de ângulo via Tesseract (PSM7)."""
    import pytesseract
    img_gray = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2GRAY)
    _, binar = cv2.threshold(img_gray, 120, 255, cv2.THRESH_BINARY)
    cfg = '--psm 7 -c tessedit_char_whitelist=0123456789'
    txt = pytesseract.image_to_string(binar, config=cfg).strip()
    return ''.join(c for c in txt if c.isdigit()) or "0"

def read_wind(pil_img):
    """
    Detecta cada caractere do vento por contorno + template matching.
    """
    img_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    gray    = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    hsv     = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # máscara para vermelho (números do vento são vermelhos)
    l1, u1 = np.array([0,70,50]),   np.array([10,255,255])
    l2, u2 = np.array([170,70,50]), np.array([180,255,255])
    mask = cv2.inRange(hsv, l1, u1) | cv2.inRange(hsv, l2, u2)

    # limpa usando morfologia
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)

    # aplica máscara e binariza para achar contornos
    isolated = cv2.bitwise_and(gray, gray, mask=mask)
    _, binar  = cv2.threshold(isolated, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cnts, _   = cv2.findContours(binar, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # pega só áreas grandes (descarta ruídos)
    boxes = [cv2.boundingRect(c) for c in cnts if cv2.contourArea(c)>50]
    if not boxes:
        return "0"

    # ordena por X e faz matching contra cada template
    boxes.sort(key=lambda b: b[0])
    result = ""
    for x,y,w,h in boxes:
        roi = gray[y:y+h, x:x+w]
        best_char, best_val = "", 0
        for k,tpl in templates.items():
            th,tw = tpl.shape
            if th>h or tw>w: continue
            val = cv2.matchTemplate(roi, tpl, cv2.TM_CCOEFF_NORMED).max()
            if val>best_val:
                best_val, best_char = val, k
        if best_val>=0.85:
            result += "." if best_char=="dot" else best_char

    return result or "0"

def ocr_read(img, kind):
    return read_angle(img) if kind=="angulo" else read_wind(img)
