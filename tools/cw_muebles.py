# Farlands Taller v0.1.8 - muebles, herramientas y decoracion propios (detallados, en rejilla de 1/8 o 1/16 de bloque).
# Al importarlo, los ids del catalogo (121 cama, 122 cofre, 123/124 mesas, 125 banco, 126 taburete, 127 estanteria,
# 128 barril, 129 saco, 131 silla, 133 armario, 135 yunque, 138 candelabro, 155 valla, 159 maceta, 161 lena,
# 1006 junco, 1016 carreta) se arman con estos modelos en vez de los del juego. Mismas huellas y giros que el catalogo.
import math
from cw_lib import CONSTRUCTORES, COL_INV, _h
from cw_vox import Pieza, Vox, torno

MAD = (138, 92, 56); MADO = (96, 62, 38); MADC = (164, 114, 70); MADCC = (186, 136, 88)
HIE = (34, 34, 40); HIE2 = (58, 58, 66); ACERO = (176, 180, 190); ACERO2 = (140, 144, 154)
ORO = (214, 170, 70); CUERO = (122, 76, 44); CUERO2 = (96, 58, 34)
TELA_B = (240, 234, 220); PAJA = (226, 200, 118); PAJA2 = (204, 176, 96); PAJA3 = (238, 216, 140)
HOJA = (64, 150, 54); HOJA2 = (88, 178, 66); HOJA3 = (50, 124, 46); TALLO = (70, 92, 40)
BARRO = (176, 100, 62); BARRO2 = (150, 84, 52)


def _var(col, k, d=8):
    t = (k % 5 - 2) * d / 2.0
    return (col[0] + t, col[1] + t, col[2] + t * 0.9)


# ======================================================================== muebles (marco local, frente a -Z)
def cama(col=(176, 48, 52), franja=(232, 200, 96)):
    p = Pieza(2, 4)
    o = 0.75
    for x in (0.0, 1.75):
        p.f(x, 0, 3.75, x + 0.25, 1.875, 4.0, MADO, 2)
        p.f(x + 0.0625, 1.875, 3.8125, x + 0.1875, 2.0, 3.9375, MADC)
        p.f(x, 0, o, x + 0.25, 1.25, o + 0.25, MADO, 2)
        p.f(x + 0.0625, 1.25, o + 0.0625, x + 0.1875, 1.375, o + 0.1875, MADC)
    p.f(0.25, 0.5, 3.8125, 1.75, 1.5625, 3.9375, MAD, 2)             # cabecero
    p.f(0.25, 1.5625, 3.78, 1.75, 1.6875, 3.97, MADC, 2)
    p.f(0.5, 0.75, 3.79, 1.5, 1.375, 3.8125, MADC, 2)                # panel en relieve
    p.f(0.25, 0.5, o + 0.0625, 1.75, 1.0, o + 0.1875, MAD, 2)        # piecero
    p.f(0.25, 1.0, o + 0.03, 1.75, 1.0625, o + 0.22, MADC, 2)
    for x in (0.03, 1.78):                                           # largueros
        p.f(x, 0.375, o + 0.25, x + 0.19, 0.625, 3.75, MADO, 2)
    p.f(0.1875, 0.5, o + 0.25, 1.8125, 0.875, 3.75, (226, 214, 180))   # colchon
    p.f(0.375, 0.875, 3.0, 1.625, 1.0625, 3.6875, TELA_B)            # almohada
    p.f(0.3125, 0.875, 3.0625, 0.4375, 1.0, 3.625, (226, 220, 206))
    p.f(1.5625, 0.875, 3.0625, 1.6875, 1.0, 3.625, (226, 220, 206))
    p.f(0.125, 0.875, o + 0.25, 1.875, 0.9375, 2.875, col)           # manta
    p.f(0.125, 0.5625, o + 0.25, 0.1875, 0.875, 2.875, col)          # caidas de la manta
    p.f(1.8125, 0.5625, o + 0.25, 1.875, 0.875, 2.875, col)
    p.f(0.125, 0.9375, 2.625, 1.875, 1.0, 2.9375, TELA_B)            # sabana doblada
    p.f(0.125, 0.9375, 1.25, 1.875, 0.95, 1.5, franja)               # franja
    p.f(0.125, 0.9375, 1.625, 1.875, 0.95, 1.6875, franja)
    return p


def cofre():
    p = Pieza(2, 1)
    p.f(0.0625, 0, 0.0625, 1.9375, 0.75, 0.9375, MADO, 2)
    for i, (y0, y1) in enumerate(((0.02, 0.23), (0.27, 0.48), (0.52, 0.73))):
        p.f(0.0625, y0, 0.03, 1.9375, y1, 0.0625, MAD if i % 2 else MADC, 2)
        p.f(0.0625, y0, 0.9375, 1.9375, y1, 0.97, MAD if i % 2 else MADC, 2)
        p.f(0.03, y0, 0.0625, 0.0625, y1, 0.9375, MAD if i % 2 else MADC, 2)
        p.f(1.9375, y0, 0.0625, 1.97, y1, 0.9375, MAD if i % 2 else MADC, 2)
    p.f(0.0, 0.75, 0.0, 2.0, 1.0, 1.0, MAD, 2)                       # tapa
    p.f(0.0625, 1.0, 0.125, 1.9375, 1.125, 0.875, MADC, 2)
    for x in (0.25, 1.625):                                          # zunchos
        p.f(x, 0.0, -0.03, x + 0.125, 1.0, 1.03, HIE2)
        p.f(x, 1.0, 0.09, x + 0.125, 1.155, 0.91, HIE2)
    for x in (0.0, 1.8125):                                          # esquineros
        p.f(x - 0.02, 0, -0.03, x + 0.2075, 0.1875, 0.1875, HIE)
        p.f(x - 0.02, 0.8125, -0.03, x + 0.2075, 1.0, 0.1875, HIE)
    p.f(0.875, 0.5, -0.06, 1.125, 0.875, 0.0, HIE)                   # cerradura
    p.f(0.97, 0.6, -0.07, 1.03, 0.72, -0.06, (12, 12, 14))
    p.f(0.9375, 0.875, -0.05, 1.0625, 1.05, 0.0, ORO)
    for x in (-0.06, 2.0):                                           # asas
        p.f(x, 0.5, 0.375, x + 0.06, 0.5625, 0.625, HIE)
    return p


def mesa(W):
    p = Pieza(W, 1)
    for i in range(4):
        z0 = i * 0.25 + 0.01
        p.f(0, 1.125, z0, W, 1.3, z0 + 0.23, MAD if i % 2 else MADC, 2)
    p.f(0.03, 1.12, 0.0, W - 0.03, 1.125, 1.0, MADO)
    p.f(0.125, 0.875, 0.125, W - 0.125, 1.125, 0.875, MADO, 2)       # faldon
    for x in (0.0625, W - 0.25):
        for z in (0.0625, 0.75):
            p.f(x, 0.0625, z, x + 0.1875, 0.875, z + 0.1875, MAD, 2)
            p.f(x - 0.03, 0.0, z - 0.03, x + 0.2175, 0.0625, z + 0.2175, MADO)
    p.f(0.25, 0.25, 0.4375, W - 0.25, 0.375, 0.5625, MADO)           # travesanos
    for x in (0.0625, W - 0.25):
        p.f(x + 0.03, 0.25, 0.25, x + 0.1575, 0.375, 0.75, MADO)
    return p


def silla():
    p = Pieza(1, 1)
    p.f(0.125, 0.625, 0.125, 0.5, 0.75, 0.875, MADC, 2)
    p.f(0.5, 0.625, 0.125, 0.875, 0.75, 0.875, MAD, 2)
    for x in (0.125, 0.75):
        p.f(x, 0, 0.125, x + 0.125, 0.625, 0.25, MADO)
        p.f(x, 0, 0.75, x + 0.125, 1.625, 0.875, MADO)
        p.f(x + 0.03, 0.25, 0.25, x + 0.095, 0.3125, 0.75, MADO)
    p.f(0.25, 1.0, 0.77, 0.75, 1.0625, 0.855, MAD)
    for x in (0.34, 0.47, 0.6):
        p.f(x, 0.75, 0.78, x + 0.0625, 1.375, 0.845, MAD)
    p.f(0.0625, 1.375, 0.74, 0.9375, 1.5, 0.885, MADC, 2)
    p.f(0.125, 1.5, 0.75, 0.875, 1.5625, 0.875, MADC, 2)
    return p


def banco():
    p = Pieza(3, 1)
    p.f(0, 0.75, 0.0, 3, 0.875, 0.5, MADC, 2)
    p.f(0.03, 0.7, 0.03, 2.97, 0.75, 0.47, MADO)
    for x in (0.25, 2.625):
        p.f(x, 0.5, 0.0625, x + 0.125, 0.7, 0.4375, MAD, 2)
        p.f(x, 0, 0.0625, x + 0.125, 0.5, 0.1875, MAD, 2)
        p.f(x, 0, 0.3125, x + 0.125, 0.5, 0.4375, MAD, 2)
    p.f(0.375, 0.25, 0.1875, 2.625, 0.375, 0.3125, MADO)
    return p


def taburete():
    p = Pieza(1, 1)
    p.f(0.1875, 0.625, 0.125, 0.8125, 0.75, 0.875, MADC, 2)
    p.f(0.125, 0.625, 0.1875, 0.875, 0.75, 0.8125, MADC, 2)
    for (x, z) in ((0.125, 0.125), (0.75, 0.125), (0.125, 0.75), (0.75, 0.75)):
        dx = 0.0625 if x < 0.5 else -0.0625
        dz = 0.0625 if z < 0.5 else -0.0625
        p.f(x + dx, 0.3125, z + dz, x + dx + 0.125, 0.625, z + dz + 0.125, MAD)
        p.f(x, 0, z, x + 0.125, 0.3125, z + 0.125, MAD)
    p.f(0.25, 0.25, 0.25, 0.75, 0.3125, 0.3125, MADO)
    p.f(0.25, 0.25, 0.6875, 0.75, 0.3125, 0.75, MADO)
    return p


LIBROS = [(150, 40, 44), (52, 84, 150), (60, 120, 70), (120, 80, 150), (176, 120, 50), (90, 60, 40), (40, 110, 120)]


def estanteria(k=0):
    p = Pieza(3, 1)
    for x in (0.0, 2.875):
        p.f(x, 0, 0, x + 0.125, 3.375, 0.5, MADO, 2)
    p.f(0.125, 0.125, 0.4375, 2.875, 3.25, 0.5, MAD, 2)
    for y in (0.0, 1.0625, 2.125):
        p.f(0.125, y + 0.125, 0, 2.875, y + 0.25, 0.4375, MADC, 2)
    p.f(0.125, 0, 0.0625, 2.875, 0.125, 0.4375, MADO)
    p.f(0.0, 3.25, 0, 3.0, 3.375, 0.5, MADC, 2)
    p.f(-0.0625, 3.375, -0.0625, 3.0625, 3.5, 0.5, MADO, 2)
    for t, y in enumerate((0.25, 1.3125, 2.375)):
        x = 0.1875
        n = 0
        while x < 2.75:
            r = _h(k, t, n) % 10
            if r < 6:          # libro
                w = 0.125 + (r % 2) * 0.0625
                h = 0.5 + (r % 3) * 0.125
                if x + w > 2.8:
                    break
                c = LIBROS[_h(k, t, n, 1) % len(LIBROS)]
                p.f(x, y, 0.0625, x + w, y + h, 0.4375, c)
                p.f(x, y + h - 0.125, 0.05, x + w, y + h - 0.0625, 0.0625, ORO)
                x += w + 0.01
            elif r < 8:        # tarro
                if x + 0.3125 > 2.8:
                    break
                c = ((190, 120, 80), (200, 196, 180), (120, 150, 170))[r % 3]
                p.f(x + 0.03, y, 0.1, x + 0.28, y + 0.3125, 0.375, c)
                p.f(x + 0.0625, y + 0.3125, 0.125, x + 0.25, y + 0.375, 0.35, (150, 104, 60))
                x += 0.34
            elif r == 8:       # rollo
                if x + 0.25 > 2.8:
                    break
                p.f(x, y, 0.1, x + 0.25, y + 0.125, 0.375, (236, 226, 196))
                p.f(x + 0.08, y + 0.125, 0.15, x + 0.17, y + 0.18, 0.33, (180, 40, 40))
                x += 0.3
            else:
                x += 0.1875
            n += 1
    return p


def armario():
    p = Pieza(2, 1)
    p.f(0.0, 0.125, 0.0625, 2.0, 2.875, 1.0, MADO, 2)
    p.f(0.0625, 0, 0.125, 1.9375, 0.125, 0.9375, MADO)
    p.f(-0.0625, 2.875, 0.0, 2.0625, 3.0, 1.0625, MADC, 2)
    p.f(0.0, 3.0, 0.0625, 2.0, 3.0625, 1.0, MADO)
    for x0 in (0.0625, 1.03125):
        x1 = x0 + 0.90625
        p.f(x0, 0.1875, 0.0, x1, 2.8125, 0.0625, MAD, 2)
        for (ya, yb) in ((0.4375, 1.3125), (1.6875, 2.5625)):
            p.f(x0 + 0.125, ya, -0.03, x1 - 0.125, yb, 0.0, MADC, 2)
    p.f(0.875, 1.375, -0.1, 0.9375, 1.5625, -0.03, ORO)
    p.f(1.0625, 1.375, -0.1, 1.125, 1.5625, -0.03, ORO)
    return p


def barril(k=0, tapa=True):
    v = Vox(0.125)
    perf = [3.0, 3.4, 3.7, 3.85, 3.9, 3.9, 3.85, 3.7, 3.4, 3.0]
    aros = {1, 8}

    def col(a, t, borde):
        if t in aros and borde:
            return HIE2
        if t == len(perf) - 1 and not borde:
            return MADC
        s = int((a + math.pi) / (2 * math.pi) * 14)
        return MAD if s % 2 else (126, 84, 50)
    torno(v, 4.0, 4.0, 0, perf, col)
    if tapa:
        v.set(5, 9, 3, MADO); v.set(5, 9, 4, MADO)
    p = Pieza(1, 1)
    p.vox(v, 0, 0, 0, 2)
    return p


def saco(k=0):
    v = Vox(0.125)
    perf = [2.6, 3.0, 3.2, 3.2, 3.0, 2.6, 1.6, 1.0, 1.6]
    c1, c2 = (190, 164, 120), (172, 146, 104)

    def col(a, t, borde):
        if t == 6:
            return (120, 90, 56)
        return c1 if (int(a * 3) + t) % 3 else c2
    torno(v, 4.0, 4.0, 0, perf, col)
    p = Pieza(1, 1)
    p.vox(v)
    return p


def lena():
    p = Pieza(2, 1)
    filas = [(0, [0.0625, 0.5625, 1.0625, 1.5625]), (1, [0.3125, 0.8125, 1.3125]), (2, [0.5625, 1.0625])]
    for (fy, xs) in filas:
        y = fy * 0.4375
        for i, x in enumerate(xs):
            corteza = (92, 62, 40) if (i + fy) % 2 else (104, 70, 44)
            p.f(x, y, 0.125, x + 0.4375, y + 0.4375, 0.875, corteza)
            for z0, z1, s in ((0.0625, 0.125, -1), (0.875, 0.9375, 1)):
                p.f(x + 0.03, y + 0.03, z0, x + 0.4075, y + 0.4075, z1, (204, 168, 116))
                zr = z0 - 0.015 if s < 0 else z1
                p.f(x + 0.125, y + 0.125, zr, x + 0.3125, y + 0.3125, zr + 0.015, (176, 136, 90))
    return p


def yunque():
    p = Pieza(2, 1)
    v = Vox(0.125)
    torno(v, 8.0, 4.0, 0, [3.6, 3.6, 3.6, 3.6], lambda a, t, b: (98, 66, 42) if b else (196, 160, 110))
    p.vox(v)
    A, A2 = (66, 68, 78), (88, 90, 100)
    p.f(0.5, 0.5, 0.25, 1.375, 0.625, 0.75, A)
    p.f(0.625, 0.625, 0.375, 1.25, 0.8125, 0.625, A)
    p.f(0.375, 0.8125, 0.25, 1.375, 1.0625, 0.75, A2)
    p.f(1.375, 0.875, 0.3125, 1.625, 1.0625, 0.6875, A2)
    p.f(1.625, 0.9375, 0.375, 1.8125, 1.0625, 0.625, A2)
    p.f(1.8125, 1.0, 0.4375, 1.9375, 1.0625, 0.5625, A2)
    p.f(0.1875, 0.9375, 0.3125, 0.375, 1.0625, 0.6875, A2)
    p.f(0.5, 1.0625, 0.4375, 0.5625, 1.075, 0.5625, (20, 20, 22))
    p.f(0.75, 1.0625, 0.3125, 1.25, 1.07, 0.6875, (120, 122, 132))    # cara pulida
    return p


def candelabro():
    p = Pieza(1, 1)
    p.f(0.3125, 0, 0.3125, 0.6875, 0.0625, 0.6875, HIE)
    p.f(0.375, 0.0625, 0.375, 0.625, 0.125, 0.625, HIE2)
    p.f(0.4375, 0.125, 0.4375, 0.5625, 0.875, 0.5625, HIE)
    p.f(0.125, 0.875, 0.4375, 0.875, 0.9375, 0.5625, HIE)
    for x in (0.125, 0.4375, 0.75):
        p.f(x - 0.03, 0.9375, 0.4075, x + 0.155, 1.0, 0.5925, HIE2)
        h = 1.25 if x == 0.4375 else 1.1875
        p.f(x, 1.0, 0.4375, x + 0.125, h, 0.5625, (240, 232, 210))
        p.f(x + 0.03, h - 0.06, 0.4, x + 0.095, h - 0.02, 0.4375, (240, 232, 210))
        p.f(x + 0.03, h, 0.4675, x + 0.095, h + 0.1, 0.5325, (255, 200, 80), 0, 1)
    return p


def maceta(k=0):
    p = Pieza(1, 1)
    v = Vox(0.125)
    torno(v, 4.0, 4.0, 0, [2.2, 2.6, 2.8, 3.0, 3.2], lambda a, t, b: BARRO2 if t == 4 and b else BARRO)
    for i in range(3, 6):
        for k2 in range(3, 6):
            v.set(i, 4, k2, (70, 50, 36))
    for n in range(14):
        a = n * 2.4 + k
        r = 0.6 + (n % 4) * 0.5
        i, k2 = int(round(4 + math.cos(a) * r)), int(round(4 + math.sin(a) * r))
        for j in range(5, 7 + (n % 4)):
            v.set(i, j, k2, HOJA if (n + j) % 2 else HOJA2)
    for n in range(4):
        a = n * 1.6 + k
        v.set(int(round(4 + math.cos(a) * 1.5)), 9 + n % 2, int(round(4 + math.sin(a) * 1.5)), (220, 60, 90) if n % 2 else (244, 210, 70))
    p.vox(v)
    return p


def valla():
    p = Pieza(3, 1)
    for x in (0.0, 1.4375, 2.875):
        p.f(x, 0, 0.375, x + 0.125, 1.3125, 0.5625, MADO, 2)
        p.f(x + 0.03, 1.3125, 0.405, x + 0.095, 1.375, 0.5325, MADO)
    for y in (0.4375, 0.9375):
        p.f(0, y, 0.4375, 3, y + 0.125, 0.5, MAD, 2)
    return p


def junco(k=0):
    p = Pieza(1, 1)
    v = Vox(0.0625)
    for n in range(6):
        i, kk = 4 + (n * 3) % 8, 3 + (n * 5) % 9
        h = 8 + (n * 7) % 7
        for j in range(h):
            v.set(i + (1 if j > h - 3 and n % 2 else 0), j, kk, (80, 140, 60) if j % 3 else (96, 160, 70))
        if n % 2 == 0:
            for j in range(h, h + 3):
                v.set(i, j, kk, (120, 80, 50))
    p.vox(v)
    return p


def carreta():
    """Carreta de 2 ruedas (huella 4x2, frente -Z): caja de tablones, eje que une las ruedas pasando por los cubos,
    ruedas de 1,75 de diametro con llanta de hierro, 8 rayos y cubo, varas hacia el frente con travesano."""
    p = Pieza(2, 4)
    # caja
    p.f(0.25, 0.875, 0.5, 1.75, 1.0, 3.75, MADO, 2)
    for i in range(3):
        y = 1.0 + i * 0.25
        for (x0, x1) in ((0.25, 0.375), (1.625, 1.75)):
            p.f(x0, y, 0.5, x1, y + 0.22, 3.75, MAD if i % 2 else MADC, 2)
        p.f(0.375, y, 3.625, 1.625, y + 0.22, 3.75, MAD if i % 2 else MADC, 2)
        p.f(0.375, y, 0.5, 1.625, y + 0.22, 0.625, MAD if i % 2 else MADC, 2)
    for z in (0.5, 2.0625, 3.625):
        for x in (0.1875, 1.75):
            p.f(x, 0.875, z, x + 0.0625, 1.8125, z + 0.125, MADO)
    p.f(0.375, 1.0, 0.75, 1.625, 1.25, 2.0, PAJA)
    p.f(0.5, 1.25, 1.0, 1.375, 1.4375, 1.75, PAJA3)
    # eje (pasa bajo la caja y entra en los cubos)
    p.f(-0.25, 0.75, 2.0625, 2.25, 0.875, 2.1875, HIE2)
    p.f(0.25, 0.6875, 1.875, 1.75, 0.875, 2.375, MADO)
    # ruedas (en planos x = -0.125..0.0625 y 1.9375..2.125), centro en (y 0.8125, z 2.125)
    for (xa, xb) in ((-0.125, 0.0625), (1.9375, 2.125)):
        v = Vox(0.125)
        R = 7.0
        for j in range(-7, 7):
            for k in range(-7, 7):
                d = math.hypot(j + 0.5, k + 0.5)
                if R - 1.2 <= d < R:
                    v.set(0, j, k, HIE)
                elif R - 2.2 <= d < R - 1.2:
                    v.set(0, j, k, MADC)
                elif d < 1.5:
                    v.set(0, j, k, MADO)
                else:
                    for q in range(4):                       # 8 rayos (4 lineas por el centro)
                        a = q * math.pi / 4
                        if abs(-(j + 0.5) * math.cos(a) + (k + 0.5) * math.sin(a)) < 0.62:
                            v.set(0, j, k, MAD)
                            break
        for (x0, y0, z0, x1, y1, z1, col, g) in v.cajas():
            p.f(xa, 0.875 + y0, 2.125 + z0, xb, 0.875 + y1, 2.125 + z1, col)
        p.f(xa - 0.0625, 0.75, 2.0, xb + 0.0625, 1.0, 2.25, MADO)       # cubo
        p.f(xa - 0.09, 0.8125, 2.0625, xb + 0.09, 0.9375, 2.1875, HIE)
    # varas y travesano
    for x in (0.4375, 1.4375):                                         # varas rectas hacia adelante
        p.f(x, 0.875, -1.5, x + 0.125, 1.0, 0.5, MAD, 2)
        p.f(x - 0.02, 0.86, -1.6, x + 0.145, 1.015, -1.5, HIE2)
    p.f(0.4375, 0.875, -0.25, 1.5625, 1.0, -0.125, MADO)
    p.f(0.9375, 0.0, -1.4375, 1.0625, 0.875, -1.3125, MADO)            # pie de apoyo bajo el travesano delantero
    p.f(0.4375, 0.75, -1.4375, 1.5625, 0.875, -1.3125, MADO)
    p.f(0.375, 0.0, 3.5, 0.5, 0.875, 3.625, MADO)                       # pata de apoyo trasera
    p.f(1.5, 0.0, 3.5, 1.625, 0.875, 3.625, MADO)
    return p


def _reg(cat, fn, W, D, solido=None):
    def poner(o, x, y, z, rot=0):
        fn().poner(o, x, y, z, rot)
        if solido:
            w, d = (W, D) if rot % 2 == 0 else (D, W)
            for (cx, cz) in solido(w, d):
                o.put(int(math.floor(x + cx)), int(math.floor(y)), int(math.floor(z + cz)), COL_INV)
    CONSTRUCTORES[cat] = poner


def _centro(w, d):
    return [(w / 2.0, d / 2.0)]


def _todo(w, d):
    return [(i + 0.5, j + 0.5) for i in range(int(w)) for j in range(int(d))]


_reg(121, cama, 2, 4, None)
_reg(122, cofre, 2, 1, _todo)
_reg(123, lambda: mesa(3), 3, 1, _todo)
_reg(124, lambda: mesa(2), 2, 1, _todo)
_reg(125, banco, 3, 1, None)
_reg(126, taburete, 1, 1, None)
_reg(127, estanteria, 3, 1, _todo)
_reg(128, barril, 1, 1, _todo)
_reg(129, saco, 1, 1, None)
_reg(131, silla, 1, 1, None)
_reg(133, armario, 2, 1, _todo)
_reg(135, yunque, 2, 1, _todo)
_reg(138, candelabro, 1, 1, None)
_reg(155, valla, 3, 1, None)
_reg(159, maceta, 1, 1, None)
_reg(161, lena, 2, 1, None)
_reg(1006, junco, 1, 1, None)
_reg(1016, carreta, 2, 4, None)


# ======================================================================== herramientas (en un muro, marco de cara)
def _pared(o, cara, w0=-1.0):
    """Devuelve g(u0, v0, u1, v1, d0, d1, col): caja en el muro, d = distancia hacia la sala desde la cara interior."""
    def g(u0, v0, u1, v1, d0, d1, col, pat=0, glow=0):
        o.fc(cara, u0, v0, w0 - d0, u1, v1, w0 - d1, col, pat, glow)
    return g


def martillo(g, u, v, d=0.0625):
    g(u - 0.03, v, u + 0.03, v + 0.75, d, d + 0.0625, MADC)
    for vv in (v + 0.05, v + 0.15):
        g(u - 0.045, vv, u + 0.045, vv + 0.04, d - 0.01, d + 0.0725, CUERO2)
    g(u - 0.04, v, u + 0.04, v + 0.25, d - 0.005, d + 0.0675, CUERO)
    g(u - 0.1875, v + 0.75, u + 0.0625, v + 0.875, d - 0.02, d + 0.0825, HIE2)
    g(u + 0.0625, v + 0.7, u + 0.1875, v + 0.925, d - 0.03, d + 0.0925, HIE2)
    g(u + 0.1875, v + 0.72, u + 0.21, v + 0.905, d - 0.025, d + 0.0875, ACERO)
    g(u - 0.25, v + 0.78, u - 0.1875, v + 0.845, d, d + 0.0625, HIE2)


def tenazas(g, u, v, d=0.0625):
    for s in (-1, 1):
        for i in range(8):
            uu = u + s * (0.03 + i * 0.006)
            g(uu - 0.025, v + i * 0.08, uu + 0.025, v + i * 0.08 + 0.08, d, d + 0.04, HIE2)
        g(u + s * 0.02 - 0.03, v + 0.64, u + s * 0.02 + 0.03, v + 0.8, d + 0.04, d + 0.08, HIE)
        g(u + s * 0.06 - 0.03, v + 0.8, u + s * 0.06 + 0.03, v + 0.95, d, d + 0.04, HIE)
    g(u - 0.05, v + 0.62, u + 0.05, v + 0.68, d - 0.01, d + 0.09, ACERO2)


def lima(g, u, v, d=0.0625):
    g(u - 0.04, v, u + 0.04, v + 0.25, d, d + 0.0625, MADC)
    g(u - 0.05, v + 0.25, u + 0.05, v + 0.28, d - 0.005, d + 0.0675, HIE2)
    g(u - 0.035, v + 0.28, u + 0.035, v + 0.8, d + 0.005, d + 0.0575, ACERO2)
    for i in range(6):
        g(u - 0.036, v + 0.32 + i * 0.08, u + 0.036, v + 0.34 + i * 0.08, d + 0.0, d + 0.06, (110, 112, 122))


def atizador(g, u, v, d=0.0625):
    g(u - 0.025, v, u + 0.025, v + 1.0, d, d + 0.05, HIE2)
    g(u - 0.08, v + 1.0, u + 0.08, v + 1.05, d, d + 0.05, HIE2)
    g(u - 0.08, v + 1.05, u - 0.03, v + 1.15, d, d + 0.05, HIE2)
    g(u + 0.03, v + 1.05, u + 0.08, v + 1.15, d, d + 0.05, HIE2)
    g(u - 0.06, v - 0.06, u + 0.02, v, d, d + 0.05, HIE)


def herradura(g, u, v, d=0.03):
    for (a, b, c2, e) in ((-0.12, -0.06, 0.0, 0.2), (0.06, 0.12, 0.0, 0.2), (-0.12, 0.12, 0.2, 0.26)):
        g(u + a, v + c2, u + b, v + e, d, d + 0.04, HIE2)
    for vv in (0.05, 0.13):
        g(u - 0.1, v + vv, u - 0.08, v + vv + 0.02, d + 0.04, d + 0.045, ACERO)
        g(u + 0.08, v + vv, u + 0.1, v + vv + 0.02, d + 0.04, d + 0.045, ACERO)


def sierra(g, u, v, d=0.0625):
    g(u, v, u + 0.75, v + 0.25, d, d + 0.02, ACERO)
    for i in range(12):
        g(u + 0.02 + i * 0.06, v - 0.04, u + 0.05 + i * 0.06, v, d, d + 0.02, ACERO2)
    g(u + 0.75, v - 0.03, u + 0.97, v + 0.3, d - 0.02, d + 0.06, MADC)
    g(u + 0.8, v + 0.06, u + 0.92, v + 0.2, d - 0.03, d + 0.07, MADO)
    g(u + 0.1, v + 0.15, u + 0.13, v + 0.18, d + 0.02, d + 0.03, HIE)


def escuadra(g, u, v, d=0.03):
    g(u, v, u + 0.06, v + 0.6, d, d + 0.02, ACERO)
    g(u, v, u + 0.4, v + 0.06, d, d + 0.02, ACERO)
    for i in range(5):
        g(u + 0.06, v + 0.1 + i * 0.1, u + 0.09, v + 0.11 + i * 0.1, d + 0.02, d + 0.025, HIE)


def formon(g, u, v, d=0.0625):
    g(u - 0.035, v, u + 0.035, v + 0.25, d, d + 0.06, MADC)
    g(u - 0.04, v + 0.25, u + 0.04, v + 0.28, d - 0.005, d + 0.065, HIE2)
    g(u - 0.03, v + 0.28, u + 0.03, v + 0.55, d + 0.01, d + 0.04, ACERO)


def hacha(g, u, v, d=0.0625):
    g(u - 0.035, v, u + 0.035, v + 0.9, d, d + 0.06, MADC)
    g(u - 0.045, v + 0.02, u + 0.045, v + 0.12, d - 0.005, d + 0.065, CUERO)
    g(u - 0.06, v + 0.7, u + 0.06, v + 0.85, d - 0.01, d + 0.07, HIE2)
    g(u + 0.06, v + 0.66, u + 0.2, v + 0.88, d + 0.005, d + 0.055, HIE2)
    g(u + 0.2, v + 0.62, u + 0.26, v + 0.92, d + 0.01, d + 0.05, ACERO)


def panel_herramientas(o, cara, u0, u1, v, d0=0.0):
    """Tabla de pared con clavijas (las herramientas cuelgan delante, a d >= 0,0625)."""
    g = _pared(o, cara)
    g(u0, v, u1, v + 1.25, d0, d0 + 0.0625, MAD, 2)
    g(u0 - 0.05, v + 1.2, u1 + 0.05, v + 1.3125, d0 - 0.005, d0 + 0.09, MADO, 2)
    g(u0 - 0.05, v - 0.06, u1 + 0.05, v + 0.05, d0 - 0.005, d0 + 0.09, MADO, 2)
    return g


# ======================================================================== enredadera en rejilla (frondosa, 3 profundidades)
def enredadera_vox(seed, ancho_c, alto_c, evitar=lambda i, j: False):
    """Devuelve Vox (celda 1/8) en el marco de la cara: i = a lo largo, j = alto, k = hacia afuera (0 pegado al muro).
    Mata al pie, tallos que suben con quiebres y se abren, hojas en grupos de 2x2 a 1-3 celdas del muro,
    mas tupida abajo y rala arriba, con florcitas. 'evitar(i, j)' marca celdas prohibidas (ventanas, puertas)."""
    v = Vox(0.125)
    verdes = (HOJA3, HOJA, HOJA2, (74, 164, 60))
    cx = ancho_c // 2

    def hoja(i, j, k, c):
        for di in (0, 1):
            for dj in (0, 1):
                if not evitar(i + di, j + dj) and 0 <= i + di < ancho_c:
                    v.set(i + di, j + dj, k, c, pisar=False)
    # mata al pie
    for n in range(40):
        i = cx + int(((_h(seed, n) % 1000) / 1000.0 - 0.5) * ancho_c * 0.7)
        j = (_h(seed, n, 1) % 6)
        k = 1 + _h(seed, n, 2) % 3
        hoja(i, j, k, verdes[_h(seed, n, 3) % 4])
    # tallos
    tallos = 4
    for t in range(tallos):
        i = cx + (t - tallos // 2) * 2 + (_h(seed, t) % 3) - 1
        dirx = -1 if t < tallos // 2 else 1
        top = int(alto_c * (0.75 + 0.25 * ((_h(seed, t, 9) % 100) / 100.0)))
        j = 0
        while j < top:
            if evitar(i, j):
                i += dirx
                if evitar(i, j) or not 0 <= i < ancho_c:
                    break
                continue
            v.set(i, j, 0, TALLO)
            r = _h(seed, t, j) % 10
            if r < 2 and 1 <= i + dirx < ancho_c - 1 and j > alto_c * 0.2:
                i += dirx                                   # quiebre
                v.set(i, j, 0, TALLO)
            dens = 1.0 - 0.6 * j / max(alto_c, 1)
            if (_h(seed, t, j, 1) % 100) / 100.0 < 0.55 * dens + 0.15:
                s = -2 if (j + t) % 2 else 1
                hoja(i + s, j, 1 + (_h(seed, t, j, 2) % 2), verdes[(j // 2 + t) % 4])
            if (_h(seed, t, j, 3) % 100) / 100.0 < 0.3 * dens:
                hoja(i - 1, j + 1, 2 + (_h(seed, t, j, 4) % 2), verdes[(j + t + 1) % 4])
            if j % 9 == 5 and _h(seed, t, j, 5) % 2:     # ramita lateral
                bi = i
                for q in range(1, 5):
                    bi += -dirx
                    if not 0 <= bi < ancho_c or evitar(bi, j + q // 2):
                        break
                    v.set(bi, j + q // 2, 0, TALLO)
                    if q % 2 == 0:
                        hoja(bi - 1, j + q // 2 + 1, 1, verdes[q % 4])
            if (_h(seed, t, j, 6) % 37) == 0:
                v.set(i + 1, j, 3, (244, 240, 250), pisar=False)
                v.set(i + 1, j + 1, 3, (250, 220, 90), pisar=False)
            j += 1
        hoja(i - 1, top, 1, verdes[t % 4])
        hoja(i, top + 1, 2, verdes[(t + 2) % 4])
    return v


def heno_suelo(o, x0, z0, x1, z1, y, seed=0, densidad=0.85):
    """Capa de paja suelta en rejilla de 1/8: cubre casi todo, con montoncitos de 1-3 voxeles de alto y 3 tonos."""
    v = Vox(0.125)
    ni, nk = int((x1 - x0) / 0.125), int((z1 - z0) / 0.125)
    for i in range(ni):
        for k in range(nk):
            n = (math.sin(i * 0.7 + seed) + math.cos(k * 0.6 + seed * 1.3) + math.sin((i + k) * 0.31)) / 3.0
            if (_h(seed, i, k) % 100) / 100.0 > densidad + n * 0.2:
                continue
            h = 1 + (1 if n > 0.2 else 0) + (1 if n > 0.55 else 0)
            for j in range(h):
                c = (PAJA, PAJA2, PAJA3)[(_h(seed, i, k, j) % 3)]
                v.set(i, j, k, c)
    for (x0b, y0b, z0b, x1b, y1b, z1b, col, g) in v.cajas():
        o.f(x0 + x0b, y + y0b * 0.5, z0 + z0b, x0 + x1b, y + y1b * 0.5, z0 + z1b, col)


def fardo(o, x, y, z, rot=0, seed=0):
    """Fardo de paja 1,5 x 0,75 x 0,75 en rejilla de 1/8 con dos cuerdas y briznas sueltas."""
    W, D = (12, 6) if rot % 2 == 0 else (6, 12)
    v = Vox(0.125)
    for i in range(W):
        for j in range(6):
            for k in range(D):
                if 0 < i < W - 1 and 0 < j < 5 and 0 < k < D - 1:
                    continue
                c = (PAJA, PAJA2, PAJA3)[_h(seed, i, j, k) % 3]
                cuerda = (i in (3, W - 4)) if rot % 2 == 0 else (k in (3, D - 4))
                v.set(i, j, k, (150, 108, 60) if cuerda else c)
    v.poner(o, x, y, z)
    for n in range(4):
        i, k = _h(seed, n) % W, _h(seed, n, 1) % D
        o.f(x + i * 0.125, y + 0.75, z + k * 0.125, x + i * 0.125 + 0.125, y + 0.8125, z + k * 0.125 + 0.0625, PAJA3)


# ======================================================================== cocina
def fogon(o, x, y, z):
    """Cocina de hierro 2x1 (frente -Z): cuerpo con puerta de fuego que brilla, plancha con dos ollas, tubo al techo."""
    p = Pieza(2, 1)
    p.f(0.0625, 0.125, 0.0625, 1.9375, 1.125, 1.0, HIE)
    for (a, b) in ((0.0, 0.1875), (1.8125, 2.0)):
        p.f(a, 0, 0.0, b, 0.125, 0.25, HIE2); p.f(a, 0, 0.8125, b, 0.125, 1.0, HIE2)
    p.f(0.0, 1.125, 0.0, 2.0, 1.25, 1.0, HIE2)
    p.f(0.3125, 0.3125, 0.03, 0.9375, 0.8125, 0.0625, HIE2)
    p.f(0.4375, 0.4375, 0.02, 0.8125, 0.6875, 0.03, (255, 120, 30), 0, 1)
    p.f(0.375, 0.375, 0.01, 0.875, 0.4375, 0.02, HIE)
    p.f(1.1875, 0.4375, 0.03, 1.75, 0.6875, 0.0625, HIE2)
    p.f(1.375, 0.53, 0.0, 1.5625, 0.59, 0.03, ACERO)
    v = Vox(0.0625)
    torno(v, 6.0, 7.0, 0, [3, 3.5, 3.5, 3.5, 3.5, 3.6], lambda a, t, b: (60, 60, 70) if t < 5 else (90, 90, 100))
    p.vox(v, 0.125, 1.25, 0.0625)
    v2 = Vox(0.0625)
    torno(v2, 6.0, 7.0, 0, [2.5, 2.5, 2.6], lambda a, t, b: (150, 96, 56))
    p.vox(v2, 1.0, 1.25, 0.0625)
    p.f(1.6, 1.375, 0.45, 2.1, 1.4375, 0.5625, (150, 96, 56))
    p.f(0.2, 1.62, 0.2, 0.62, 1.64, 0.64, (230, 220, 200))         # vapor/caldo
    p.f(1.25, 1.25, 0.8125, 1.6875, 4.0, 1.0, HIE2)                # tubo
    p.f(1.1875, 2.5, 0.75, 1.75, 2.5625, 1.0, HIE)
    p.poner(o, x, y, z, 0)
    o.box(int(x), y, int(z), int(x) + 1, y, int(z), COL_INV)


def encimera(o, x, y, z, largo=3, k=0):
    """Mueble bajo de cocina (frente -Z): puertas con tirador, encimera, tabla de picar con cuchillo y verduras, pan."""
    p = Pieza(largo, 1)
    p.f(0.0, 0.125, 0.0625, largo, 1.0625, 1.0, MAD, 2)
    p.f(0.0625, 0.0, 0.125, largo - 0.0625, 0.125, 0.9375, MADO)
    for i in range(largo):
        p.f(i + 0.0625, 0.1875, 0.03, i + 0.9375, 1.0, 0.0625, MADC, 2)
        p.f(i + 0.75, 0.6, 0.0, i + 0.8125, 0.75, 0.03, HIE)
    p.f(-0.0625, 1.0625, -0.0625, largo + 0.0625, 1.1875, 1.0, (190, 186, 176))
    p.f(0.3, 1.1875, 0.2, 1.3, 1.25, 0.8, MADCC, 2)                   # tabla de picar
    p.f(0.5, 1.25, 0.3, 1.05, 1.27, 0.38, ACERO)                      # cuchillo
    p.f(1.05, 1.25, 0.3, 1.25, 1.29, 0.38, MADO)
    for (dx, dz, col, h) in ((0.5, 0.55, (230, 110, 30), 0.08), (0.7, 0.6, (230, 110, 30), 0.08), (0.95, 0.55, (220, 50, 40), 0.12)):
        p.f(dx, 1.25, dz, dx + 0.12, 1.25 + h, dz + 0.12, col)
    if largo >= 3:
        p.f(1.6, 1.1875, 0.3, 2.3, 1.4, 0.7, (200, 150, 80))           # pan
        p.f(1.65, 1.4, 0.35, 2.25, 1.45, 0.65, (220, 172, 100))
        v = Vox(0.0625)                                                # col
        torno(v, 3.0, 3.0, 0, [2.5, 3, 3, 2.5, 1.5], lambda a, t, b: (110, 180, 80) if (int(a * 2) + t) % 2 else (140, 200, 100), hueco=False)
        p.vox(v, largo - 0.7, 1.1875, 0.3)
    p.poner(o, x, y, z, 0)
    o.box(int(x), y, int(z), int(x) + largo - 1, y, int(z), COL_INV)


def repisa_platos(o, cara, u, v, largo=2.0):
    """Repisa de pared con platos de canto, tazas colgadas y tarros."""
    g = _pared(o, cara)
    g(u, v, u + largo, v + 0.125, 0, 0.5, MADC, 2)
    for x in (u + 0.15, u + largo - 0.25):
        g(x, v - 0.3, x + 0.1, v, 0, 0.35, MADO)
    n = int((largo - 0.3) / 0.35)
    for i in range(n):
        uu = u + 0.2 + i * 0.35
        g(uu, v + 0.125, uu + 0.3, v + 0.45, 0.05, 0.1, (226, 222, 210))
        g(uu + 0.06, v + 0.18, uu + 0.24, v + 0.39, 0.1, 0.11, (70, 110, 170))
    g(u + 0.1, v - 0.06, u + largo - 0.1, v - 0.02, 0.4, 0.44, HIE)
    for i in range(int(largo / 0.5)):
        uu = u + 0.25 + i * 0.5
        g(uu - 0.12, v - 0.32, uu + 0.12, v - 0.08, 0.3, 0.5, (210, 206, 196) if i % 2 else (180, 110, 70))


def ollas_colgadas(o, cara, u, v, n=3):
    g = _pared(o, cara)
    g(u, v, u + n * 0.6, v + 0.08, 0.1, 0.18, HIE)
    for i in range(n):
        uu = u + 0.3 + i * 0.6
        g(uu - 0.02, v - 0.25, uu + 0.02, v, 0.12, 0.16, HIE)
        r = 0.2 + (i % 2) * 0.05
        g(uu - r, v - 0.25 - 2 * r, uu + r, v - 0.25, 0.05, 0.05 + 2 * r * 0.7, (70, 70, 80) if i % 2 else (176, 104, 60))
        g(uu - 0.03, v - 0.25 - 2 * r - 0.25, uu + 0.03, v - 0.25 - 2 * r, 0.12, 0.16, MADO)


def ristra(o, cara, u, v, col=(236, 226, 196)):
    g = _pared(o, cara)
    g(u - 0.02, v - 0.9, u + 0.02, v, 0.1, 0.14, (180, 150, 100))
    for i in range(7):
        s = -1 if i % 2 else 1
        vv = v - 0.15 - i * 0.11
        g(u + s * 0.02 - 0.07, vv - 0.1, u + s * 0.02 + 0.07, vv, 0.05, 0.19, col)
        g(u + s * 0.02 - 0.015, vv, u + s * 0.02 + 0.015, vv + 0.04, 0.1, 0.14, (120, 150, 70))
