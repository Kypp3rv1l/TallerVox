# Farlands Taller - piezas de casa estilo Cube World (v0.1.5). Ver docs/reglas_casas.md
# Medidas (bloques de 0,5 m; el personaje mide 2): puerta 2x3, ventana 2x2 con cruz y jardinera,
# muro de 7 por planta, zocalo oscuro, casa 2 bloques sobre la acera, techo bajo escalonado verde azulado.
from cw_lib import Obra, COL_INV, WD, WDD, IRON, _h

H_PISO = 7          # alto libre de una planta (suelo a techo)
SILL = 2            # alfeizar: 2 bloques sobre el suelo
GLASS = (104, 146, 178)
FLOR_CAJA = (226, 214, 186)
TIERRA_M = (74, 52, 36)
HOJA = (64, 150, 54)
HOJA2 = (88, 178, 66)


class Casa:
    """Caja de muros de x0..x1, z0..z1 (celdas de muro incluidas) sobre una acera en y=0."""

    def __init__(self, o: Obra, x0, z0, x1, z1, pisos=1, h=H_PISO, techo=True, muro="muro"):
        self.o, self.x0, self.z0, self.x1, self.z1, self.pisos, self.h = o, x0, z0, x1, z1, pisos, h
        self.s = 3                                     # suelo transitable de la planta baja
        self.suelos = [self.s + k * (h + 1) for k in range(pisos)]
        self.roof_y = self.s + pisos * h + (pisos - 1)
        self.muro = muro
        self.caras = {
            "n": {"O": (x0, z0), "U": (1, 0), "N": (0, -1)},
            "s": {"O": (x0, z1 + 1), "U": (1, 0), "N": (0, 1)},
            "o": {"O": (x0, z0), "U": (0, 1), "N": (-1, 0)},
            "e": {"O": (x1 + 1, z0), "U": (0, 1), "N": (1, 0)},
        }
        self._cuerpo()
        if techo:
            self._techo()

    # celda de muro de una cara en (u, y)
    def celda(self, cara, u, y):
        if cara == "n": return (self.x0 + u, y, self.z0)
        if cara == "s": return (self.x0 + u, y, self.z1)
        if cara == "o": return (self.x0, y, self.z0 + u)
        return (self.x1, y, self.z0 + u)

    def largo(self, cara):
        return (self.x1 - self.x0 + 1) if cara in ("n", "s") else (self.z1 - self.z0 + 1)

    def _cuerpo(self):
        o, x0, z0, x1, z1 = self.o, self.x0, self.z0, self.x1, self.z1
        # zocalo: anillo de 1 por fuera, 2 de alto (y 1..2)
        o.mbox(x0 - 1, 1, z0 - 1, x1 + 1, 2, z1 + 1, "zocalo")
        # losa de la planta baja
        o.mbox(x0 + 1, 1, z0 + 1, x1 - 1, 2, z1 - 1, "piso")
        # muros
        top = self.roof_y - 1
        for y in range(1, top + 1):
            for x in range(x0, x1 + 1):
                o.mat(x, y, z0, self.muro); o.mat(x, y, z1, self.muro)
            for z in range(z0, z1 + 1):
                o.mat(x0, y, z, self.muro); o.mat(x1, y, z, self.muro)
        # entrepisos (madera: por debajo se ve como techo de tablas) y cornisa por fuera
        for k in range(1, self.pisos):
            y = self.suelos[k] - 1
            o.mbox(x0 + 1, y, z0 + 1, x1 - 1, y, z1 - 1, "madera")
            for c in self.caras.values():
                L = self.largo_c(c)
                self.o.fc(c, -0.3, y + 0.55, 0, L + 0.3, y + 1.0, 0.3, (92, 98, 96))

    def largo_c(self, c):
        return (self.x1 - self.x0 + 1) if c["U"] == (1, 0) else (self.z1 - self.z0 + 1)

    def _techo(self):
        o, x0, z0, x1, z1, y = self.o, self.x0, self.z0, self.x1, self.z1, self.roof_y
        k = 0
        while True:
            a0, a1, b0, b1 = x0 - 1 + 2 * k, x1 + 1 - 2 * k, z0 - 1 + 2 * k, z1 + 1 - 2 * k
            if a0 > a1 or b0 > b1:
                break
            if k == 0:
                for xx in range(a0, a1 + 1):
                    for zz in range(b0, b1 + 1):
                        inside = x0 < xx < x1 and z0 < zz < z1
                        o.mat(xx, y, zz, "madera" if inside else "techo")
            else:
                o.mbox(a0, y + k, b0, a1, y + k, b1, "techo")
            k += 1
        self.cumbre = y + k - 1
        # vigas que asoman bajo el alero (lados largos)
        largos = ("n", "s") if (x1 - x0) >= (z1 - z0) else ("o", "e")
        for cn in largos:
            c = self.caras[cn]
            L = self.largo(cn)
            for u in range(2, L - 1, 3):
                o.fc(c, u + 0.25, y - 0.45, -0.2, u + 0.75, y, 0.85, WDD, 2)
        # vigas del techo por dentro
        for p, s in enumerate(self.suelos):
            yc = (self.suelos[p + 1] - 1) if p + 1 < len(self.suelos) else y
            if (x1 - x0) >= (z1 - z0):
                for xx in range(x0 + 3, x1 - 1, 4):
                    o.f(xx, yc - 0.45, z0 + 1, xx + 0.6, yc, z1, WDD, 2)
            else:
                for zz in range(z0 + 3, z1 - 1, 4):
                    o.f(x0 + 1, yc - 0.45, zz, x1, yc, zz + 0.6, WDD, 2)

    # ---- aberturas ----
    def ventana(self, cara, u, piso=0, flores=True, w=2, h=2):
        o, c = self.o, self.caras[cara]
        yb = self.suelos[piso] + SILL
        for du in range(w):
            for dy in range(h):
                x, y, z = self.celda(cara, u + du, yb + dy)
                o.put(x, y, z, COL_INV)
        F = 0.17
        # marco (a media profundidad del muro), cruz y vidrio
        o.fc(c, u, yb, -0.68, u + F, yb + h, -0.3, WDD, 2)
        o.fc(c, u + w - F, yb, -0.68, u + w, yb + h, -0.3, WDD, 2)
        o.fc(c, u, yb + h - F, -0.68, u + w, yb + h, -0.3, WDD, 2)
        o.fc(c, u, yb, -0.68, u + w, yb + F, -0.3, WDD, 2)
        o.fc(c, u + F, yb + F, -0.52, u + w - F, yb + h - F, -0.48, GLASS)
        for k in range(1, w):
            o.fc(c, u + k - 0.06, yb + F, -0.6, u + k + 0.06, yb + h - F, -0.4, WDD)
        o.fc(c, u + F, yb + h / 2 - 0.06, -0.6, u + w - F, yb + h / 2 + 0.06, -0.4, WDD)
        # repisa interior
        o.fc(c, u - 0.1, yb - 0.12, -1.18, u + w + 0.1, yb + 0.02, -0.68, WD, 2)
        if flores:
            self.jardinera(c, u, yb, w)
        else:
            o.fc(c, u - 0.12, yb - 0.16, -0.3, u + w + 0.12, yb + 0.02, 0.25, (150, 148, 140))

    def jardinera(self, c, u, yb, w=2):
        o = self.o
        o.fc(c, u - 0.2, yb - 0.6, 0.0, u + w + 0.2, yb - 0.04, 0.62, FLOR_CAJA)
        o.fc(c, u - 0.08, yb - 0.1, 0.08, u + w + 0.08, yb - 0.02, 0.54, TIERRA_M)
        n = int(w * 3)
        for i in range(n):
            t = (i + 0.5) / n * (w + 0.2) - 0.1
            hh = 0.25 + (_h(c["O"], u, i) % 3) * 0.08
            o.fc(c, u + t - 0.18, yb - 0.04, 0.12, u + t + 0.18, yb + hh * 0.7, 0.5, HOJA if i % 2 else HOJA2)
            col = (206, 44, 56) if (_h(c["O"], u, i, 1) % 3) else (244, 240, 232)
            o.fc(c, u + t - 0.13, yb + hh * 0.7, 0.18, u + t + 0.13, yb + hh * 0.7 + 0.24, 0.44, col)

    def puerta(self, cara, u, piso=0, escalones=True, w=2):
        """Hueco de puerta de w x 3, SIN hoja (para el sistema de abrir y cerrar), con marco, dintel y escalones."""
        o, c = self.o, self.caras[cara]
        yb = self.suelos[piso]
        for du in range(w):
            for dy in range(3):
                o.clear(*self.celda(cara, u + du, yb + dy))
        F = 0.2
        o.fc(c, u, yb, -1.0, u + F, yb + 3, 0.06, WDD, 2)
        o.fc(c, u + w - F, yb, -1.0, u + w, yb + 3, 0.06, WDD, 2)
        o.fc(c, u, yb + 3 - F, -1.0, u + w, yb + 3, 0.06, WDD, 2)
        o.fc(c, u - 0.45, yb + 3, -0.05, u + w + 0.45, yb + 3.4, 0.3, WDD, 2)       # dintel
        o.fc(c, u + F, yb - 0.04, -1.0, u + w - F, yb + 0.02, 0.0, (150, 146, 136))   # umbral
        if escalones and piso == 0:
            # el zocalo (anillo a 1 del muro) hace de primer descanso; un escalon mas a 2 del muro
            for du in range(-1, w + 1):
                (x, _, z) = self.celda(cara, u + du, 0)
                dx, dz = c["N"]
                o.mat(x + dx, 1, z + dz, "zocalo")
                o.mat(x + 2 * dx, 1, z + 2 * dz, "piedra")

    def cartel_colgante(self, cara, u, y, simbolo="jarra"):
        """Cartel redondo colgado de un brazo de hierro, perpendicular a la fachada."""
        o, c = self.o, self.caras[cara]
        (ox, oz), (ux, uz), (nx, nz) = c["O"], c["U"], c["N"]
        o.fc(c, u - 0.06, y + 1.6, 0.0, u + 0.06, y + 1.72, 1.6, IRON)
        # disco hecho de 3 cajas (perpendicular: ancho en w)
        cx = 1.0
        o.fc(c, u - 0.07, y + 0.3, cx - 0.45, u + 0.07, y + 1.5, cx + 0.45, (232, 222, 196))
        o.fc(c, u - 0.07, y + 0.45, cx - 0.6, u + 0.07, y + 1.35, cx + 0.6, (232, 222, 196))
        o.fc(c, u - 0.09, y + 0.4, cx - 0.52, u + 0.09, y + 0.48, cx + 0.52, (150, 60, 40))
        o.fc(c, u - 0.09, y + 1.32, cx - 0.52, u + 0.09, y + 1.4, cx + 0.52, (150, 60, 40))
        for wv in (cx - 0.35, cx + 0.35):
            o.fc(c, u - 0.04, y + 1.5, wv - 0.03, u + 0.04, y + 1.62, wv + 0.03, IRON)
        if simbolo == "jarra":
            o.fc(c, u - 0.11, y + 0.62, cx - 0.22, u + 0.11, y + 1.12, cx + 0.18, (200, 150, 60))
            o.fc(c, u - 0.12, y + 1.08, cx - 0.24, u + 0.12, y + 1.18, cx + 0.2, (250, 250, 240))
            o.fc(c, u - 0.11, y + 0.72, cx + 0.18, u + 0.11, y + 0.98, cx + 0.32, (200, 150, 60))
        elif simbolo == "escudo":
            o.fc(c, u - 0.11, y + 0.62, cx - 0.25, u + 0.11, y + 1.18, cx + 0.25, (60, 90, 150))
            o.fc(c, u - 0.12, y + 0.85, cx - 0.06, u + 0.12, y + 1.1, cx + 0.06, (230, 190, 70))

    def farol_pared(self, cara, u, y, interior=True):
        o, c = self.o, self.caras[cara]
        w0 = -1.0 if interior else 0.0
        sg = -1 if interior else 1
        o.fc(c, u + 0.42, y + 0.9, w0, u + 0.58, y + 1.0, w0 + sg * 0.45, IRON)
        o.fc(c, u + 0.28, y + 0.35, w0 + sg * 0.3, u + 0.72, y + 0.85, w0 + sg * 0.74, (255, 214, 120), 0, 1)
        o.fc(c, u + 0.24, y + 0.85, w0 + sg * 0.26, u + 0.76, y + 0.95, w0 + sg * 0.78, IRON)
        o.fc(c, u + 0.24, y + 0.27, w0 + sg * 0.26, u + 0.76, y + 0.35, w0 + sg * 0.78, IRON)

    def enredadera(self, cara, u, y0, y1):
        o, c = self.o, self.caras[cara]
        y = y0
        k = 0
        while y < y1:
            du = ((_h(cara, u, k) % 7) - 3) * 0.12
            o.fc(c, u + du, y, 0.0, u + du + 0.12, y + 0.7, 0.1, (60, 110, 40))
            for s in (-1, 1):
                if _h(cara, u, k, s) % 3:
                    lx = u + du + s * (0.25 + (_h(k, s) % 3) * 0.1)
                    o.fc(c, lx - 0.22, y + 0.15, 0.02, lx + 0.22, y + 0.55, 0.24, HOJA if (k + s) % 2 else HOJA2)
            y += 0.6
            k += 1

    # ---- chimenea con hogar y conducto cerrado ----
    def chimenea(self, cara, u, w=2):
        """Hogar de w de ancho metido en el muro; el cuerpo de piedra sale 2 por fuera y sube sobre el techo.
        El nicho tiene fondo, lados y techo (campana) de piedra: no se ve ningun hueco hacia arriba."""
        o, c = self.o, self.caras[cara]
        (ox, oz), (ux, uz), (nx, nz) = c["O"], c["U"], c["N"]
        s = self.suelos[0]
        top = self.cumbre + 1
        for du in range(-1, w + 1):
            for dw in (1, 2):
                for y in range(1, top + 1):
                    if y > self.roof_y and (du < 0 or du >= w):
                        continue          # sobre el alero el cuerpo se angosta a w x 2
                    x, _, z = self.celda(cara, u + du, 0)
                    o.mat(x + nx * dw, y, z + nz * dw, "chimenea")
        for du in (-1, w):                # remate del ensanche bajo el alero
            o.fc(c, u + du, self.roof_y - 0.25, 0.0, u + du + 1, self.roof_y, 2.15, (150, 146, 136))
        # boca del hogar: hueco de w x 3 en el muro y 1 hacia el cuerpo
        for du in range(w):
            for y in range(s, s + 3):
                x, _, z = self.celda(cara, u + du, 0)
                o.clear(x, y, z)
                o.clear(x + nx, y, z + nz)
        # remate y boca de humo
        x, _, z = self.celda(cara, u - 1, 0)
        o.fc(c, u - 0.15, top + 1, 0.85, u + w + 0.15, top + 1.3, 3.15, (150, 146, 136))
        o.fc(c, u + 0.25, top + 1.3, 1.25, u + w - 0.25, top + 1.42, 2.75, (34, 30, 28))
        # repisa sobre la boca y piedra del fondo oscurecida (hollin)
        o.fc(c, u - 0.5, s + 3, -1.4, u + w + 0.5, s + 3.3, -0.7, WDD, 2)
        o.fc(c, u + 0.15, s + 0.4, 0.96, u + w - 0.15, s + 2.6, 1.0, (52, 46, 42))
        # hogar con fuego (2x2) centrado en la boca, metido a medias
        hx = u + (w - 2) / 2.0
        if cara == "s":
            o.obj(130, self.x0 + hx, s, self.z1 - 0.5)
        elif cara == "n":
            o.obj(130, self.x0 + hx, s, self.z0 - 0.5)
        elif cara == "e":
            o.obj(130, self.x1 - 0.5, s, self.z0 + hx)
        else:
            o.obj(130, self.x0 - 0.5, s, self.z0 + hx)

    # ---- interior ----
    def alfombra(self, x0, z0, x1, z1, piso, a, b, borde=0.6):
        y = self.suelos[piso]
        o = self.o
        o.f(x0, y, z0, x1, y + 0.05, z1, a)
        o.f(x0 + borde, y + 0.05, z0 + borde, x1 - borde, y + 0.07, z1 - borde, b)
        o.f(x0 + borde + 0.5, y + 0.07, z0 + borde + 0.5, x1 - borde - 0.5, y + 0.09, z1 - borde - 0.5, a)


def planta(o, x, y, z, grande=False):
    """Planta en maceta de barro (estilo Cube World)."""
    o.f(x + 0.2, y, z + 0.2, x + 0.8, y + 0.55, z + 0.8, (168, 96, 60))
    o.f(x + 0.12, y + 0.5, z + 0.12, x + 0.88, y + 0.62, z + 0.88, (150, 84, 52))
    hs = 1.6 if grande else 0.9
    k = 0
    yy = y + 0.6
    while yy < y + 0.6 + hs:
        r = 0.45 if grande else 0.3
        for (dx, dz) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if _h(x, z, k, dx, dz) % 3:
                cx, cz = x + 0.5 + dx * r * 0.6, z + 0.5 + dz * r * 0.6
                o.f(cx - 0.2, yy, cz - 0.2, cx + 0.2, yy + 0.3, cz + 0.2, HOJA if k % 2 else HOJA2)
        o.f(x + 0.45, yy, z + 0.45, x + 0.55, yy + 0.35, z + 0.55, (60, 110, 40))
        yy += 0.3
        k += 1
    o.f(x + 0.3, yy, z + 0.3, x + 0.7, yy + 0.25, z + 0.7, HOJA2)


def jarron_flores(o, x, y, z):
    o.f(x + 0.3, y, z + 0.3, x + 0.7, y + 0.15, z + 0.7, (200, 196, 188))
    o.f(x + 0.22, y + 0.15, z + 0.22, x + 0.78, y + 0.65, z + 0.78, (210, 206, 198))
    o.f(x + 0.32, y + 0.65, z + 0.32, x + 0.68, y + 0.85, z + 0.68, (200, 196, 188))
    for i in range(6):
        dx, dz = ((i * 37) % 5) * 0.08 - 0.16, ((i * 53) % 5) * 0.08 - 0.16
        hh = 1.0 + (i % 3) * 0.2
        o.f(x + 0.47 + dx, y + 0.85, z + 0.47 + dz, x + 0.53 + dx, y + hh, z + 0.53 + dz, (60, 110, 40))
        o.f(x + 0.4 + dx, y + hh, z + 0.4 + dz, x + 0.6 + dx, y + hh + 0.2, z + 0.6 + dz, (190, 40, 110) if i % 2 else (220, 60, 130))


# ---- piezas extra ----
import json as _json, os as _os
_PL = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "plantillas.json"), encoding="utf-8"))


def mesa_redonda(o, cx, y, cz):
    """Mesa redonda con pedestal de la Taberna de Ivan (2,5 de diametro, 1,5 de alto), centrada en (cx, cz)."""
    for u0, u1, y0, y1, w0, w1, r, g, b, pat, glow in _PL["mesa_redonda"]:
        o.f(cx + u0, y + y0, cz + w0, cx + u1, y + y1, cz + w1, (r, g, b), pat, glow)
    o.put(int(cx - 0.5), y, int(cz - 0.5), COL_INV)


def escalera(c: "Casa", x0, z0, z1, piso=0, dx=1):
    """Escalera recta de bloques de madera (1 de huella x 1 de contrahuella) que sube en +X (dx=1) o -X (dx=-1)
    desde el suelo de 'piso' hasta el siguiente; abre el hueco en el entrepiso y pone baranda alrededor."""
    o = c.o
    s = c.suelos[piso]
    n = c.suelos[piso + 1] - s
    for k in range(1, n + 1):
        x = x0 + (k - 1) * dx
        o.mbox(x, s, z0, x, s + k - 1, z1, "madera")
    # hueco en el entrepiso: sobre los peldanos donde la cabeza no pasa
    yl = c.suelos[piso + 1] - 1
    hx = [x0 + (k - 1) * dx for k in range(1, n)]
    for x in hx:
        for z in range(z0, z1 + 1):
            o.clear(x, yl, z)
    # baranda en el piso de arriba (lado abierto del hueco y el extremo inicial)
    ya = c.suelos[piso + 1]
    xa, xb = min(hx), max(hx) + 1
    zf = z0 if z0 > c.z0 + 1 else z1 + 1     # el lado abierto (no pegado al muro)
    zr = z0 - 0.15 if zf == z0 else z1 + 1
    o.f(xa, ya + 1.1, zr, xb, ya + 1.25, zr + 0.15, WD, 2)
    for x in range(xa, xb + 1, 2):
        o.f(x - 0.07 if x == xb else x, ya, zr, (x - 0.07 if x == xb else x) + 0.14, ya + 1.1, zr + 0.15, WDD)
    xe = xa - 0.15 if dx == 1 else xb
    o.f(xe, ya + 1.1, z0, xe + 0.15, ya + 1.25, z1 + 1, WD, 2)
    o.f(xe, ya, z0, xe + 0.15, ya + 1.1, z0 + 0.15, WDD)
    # colision de la baranda
    zc = z0 - 1 if zf == z0 else z1 + 1
    for x in range(xa, xb):
        o.put(x, ya, zc, COL_INV)
    for z in range(z0, z1 + 1):
        o.put(xa - 1 if dx == 1 else xb, ya, z, COL_INV)


def barra(o, x0, z0, x1, z1, y, frente="n"):
    """Mostrador de madera de 1,25 de alto (celdas x0..x1, z0..z1) con tapa oscura y vuelo hacia el cliente."""
    o.f(x0, y, z0, x1 + 1, y + 1.1, z1 + 1, (124, 80, 50), 2)
    for x in range(x0, x1 + 1, 2):
        if frente in ("n", "s"):
            zz = z0 - 0.04 if frente == "n" else z1 + 1
            o.f(x + 0.85, y, zz, x + 1.15, y + 1.1, zz + 0.04, (92, 58, 36))
    ov = 0.25
    a0 = (z0 - ov) if frente == "n" else z0
    a1 = (z1 + 1 + ov) if frente == "s" else z1 + 1
    o.f(x0 - 0.1, y + 1.1, a0, x1 + 1.1, y + 1.3, a1, (70, 44, 28), 2)
    o.box(x0, y, z0, x1, y + 1, z1, COL_INV)


def tablero(o, cara_casa, c, u, y, ancho=3):
    """Tablero de misiones colgado en el muro (cara interior): marco de madera, corcho y papeles."""
    cara = c.caras[cara_casa]
    o.fc(cara, u, y, -1.0, u + ancho, y + 2.2, -1.12, WDD, 2)
    o.fc(cara, u + 0.15, y + 0.15, -1.12, u + ancho - 0.15, y + 2.05, -1.16, (176, 132, 84))
    papeles = [(0.3, 1.3, 0.7, 0.6), (1.2, 1.4, 0.6, 0.5), (2.0, 1.1, 0.7, 0.75), (0.5, 0.35, 0.8, 0.6), (1.6, 0.3, 0.7, 0.6)]
    for i, (pu, pv, pw, ph) in enumerate(papeles):
        if pu + pw > ancho - 0.15:
            continue
        col = (238, 230, 206) if i % 2 == 0 else (226, 214, 176)
        o.fc(cara, u + pu, y + pv, -1.16, u + pu + pw, y + pv + ph, -1.19, col)
        o.fc(cara, u + pu + pw / 2 - 0.05, y + pv + ph - 0.12, -1.19, u + pu + pw / 2 + 0.05, y + pv + ph - 0.02, -1.22, (180, 40, 40))
