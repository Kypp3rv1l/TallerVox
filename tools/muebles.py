"""Muebles de cajas finas (mismas medidas del catalogo del juego + los de la Taberna v1).
Cada pieza: lista de cajas (x0,y0,z0,x1,y1,z1,(r,g,b),pat,glow) en coordenadas locales; el frente mira a -z."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
PL = json.load(open(os.path.join(HERE, 'plantillas.json')))
WD = (132, 92, 58); WDD = (96, 66, 42); IRON = (58, 58, 66); GOLD = (200, 160, 60)
CLAY = (176, 104, 70); GRN = (70, 110, 64); LIN = (230, 222, 204)
BAR_TOP = (45, 30, 24)


def B(v, x0, y0, z0, x1, y1, z1, c, pat=0, glow=0):
    v.append((x0, y0, z0, x1, y1, z1, c, pat, glow))


def taburete():
    v = []
    B(v, 0.1, 0.65, 0.1, 0.9, 0.75, 0.9, WD)
    for k in range(4):
        x = 0.75 if k & 1 else 0.15; z = 0.75 if k & 2 else 0.15
        B(v, x, 0, z, x + 0.1, 0.65, z + 0.1, WDD)
    return v, 1, 1


def estanteria():
    v = []
    for y in (0.3, 1.3, 2.3, 3.2):
        B(v, 0, y, 0, 3, y + 0.1, 0.5, WD, 2)
    B(v, 0, 0, 0, 0.12, 3.3, 0.5, WDD); B(v, 2.88, 0, 0, 3, 3.3, 0.5, WDD); B(v, 0, 0, 0.45, 3, 3.3, 0.5, WDD)
    for k in range(6):
        x = 0.2 + k * 0.45
        B(v, x, 1.4, 0.1, x + 0.3, 1.7 + (k % 2) * 0.15, 0.4, CLAY if k % 3 == 0 else (GRN if k % 3 == 1 else LIN))
    return v, 3, 1


def barril():
    v = []
    B(v, 0.12, 0, 0.12, 0.88, 1.25, 0.88, WD, 2); B(v, 0.05, 0.12, 0.05, 0.95, 1.13, 0.95, WD, 2)
    for hy in (0.2, 1.0):
        B(v, 0.04, hy, 0.04, 0.96, hy + 0.125, 0.96, IRON)
    B(v, 0.15, 1.25, 0.15, 0.85, 1.3, 0.85, WDD)
    return v, 1, 1


def cofre():
    v = []
    B(v, 0, 0, 0, 2, 1, 1, WDD, 2); B(v, -0.03, 1, -0.03, 2.03, 1.15, 1.03, (82, 56, 36), 2)
    for x in (0.25, 1.6):
        B(v, x, 0, -0.04, x + 0.15, 1.17, 1.04, IRON)
    B(v, 0.9, 0.6, -0.06, 1.1, 0.85, 0, GOLD)
    return v, 2, 1


def banco():
    v = []
    B(v, 0, 0.7, 0, 3, 0.82, 0.5, WD, 2)
    for x in (0.3, 2.55):
        B(v, x, 0, 0.08, x + 0.15, 0.7, 0.4, WDD)
    return v, 3, 1


def mesa_redonda():
    """mesa redonda con pedestal de la Taberna (2,5 x 2,5, alto 1,5); huella 3x3 con el centro en (1.5,1.5)"""
    v = []
    for u0, u1, y0, y1, w0, w1, r, g, b, pat, glow in PL['mesa_redonda']:
        v.append((u0 + 1.5, y0, w0 + 1.5, u1 + 1.5, y1, w1 + 1.5, (r, g, b), pat, glow))
    return v, 3, 3


def barra(largo, fondo=2):
    """mostrador de la Taberna: base de Leno B (se pone como cubos) + tapa oscura de 0,2 con 0,2 de vuelo al lado del cliente"""
    v = []
    B(v, 0, 2.0, -0.2, largo, 2.2, fondo, BAR_TOP)
    return v, largo, fondo


def rotar(boxes, w, d, rot):
    for _ in range(rot % 4):
        nb = []
        for x0, y0, z0, x1, y1, z1, c, p, g in boxes:
            nb.append((d - z1, y0, x0, d - z0, y1, x1, c, p, g))
        boxes = nb; w, d = d, w
    return boxes, w, d
