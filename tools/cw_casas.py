# Farlands Taller - piezas de casa estilo Cube World (v0.1.6). Ver docs/reglas_casas.md
# Medidas (bloques de 0,5 m; el personaje mide 2): puerta 2x3, ventana 2x2 abierta con cruz y jardinera,
# muro de 7 por planta, zocalo oscuro, casa 2 bloques sobre la acera, techo bajo escalonado verde azulado.
#
# CRITERIO (lo revisa Casa.revisar() al escribir; si algo no cumple, el generador se detiene y dice que):
#   - delante de cada puerta (por dentro y por fuera) queda un paso libre de 3 de fondo y 1 mas de ancho a cada lado
#   - nada inflamable (madera, tela, plantas) a menos de 2,5 bloques del fuego; delante del hogar queda libre
#   - por fuera, nada (carteles, faroles, barriles) tapa una ventana
#   - el pie y la entrada de cada escalera quedan libres
import json as _json, os as _os, math
from cw_lib import Obra, COL_INV, WD, WDD, IRON, _h

H_PISO = 7          # alto libre de una planta (suelo a techo)
SILL = 2            # alfeizar: 2 bloques sobre el suelo
FLOR_CAJA = (226, 214, 186)
TIERRA_M = (74, 52, 36)
HOJA = (64, 150, 54)
HOJA2 = (88, 178, 66)
HIERRO = (34, 34, 40)
HIERRO2 = (56, 56, 64)
LUZ = (255, 206, 112)
LUZ2 = (255, 238, 180)
PIEDRA_F = (150, 146, 136)

# huella (ancho x, fondo z, alto) de los objetos del catalogo con rot = 0
DIMS = {121: (2, 4, 2), 122: (2, 1, 2), 123: (3, 1, 2), 124: (2, 1, 2), 125: (3, 1, 1), 126: (1, 1, 1), 127: (3, 1, 4),
        128: (1, 1, 2), 129: (1, 1, 1), 130: (2, 2, 1), 131: (1, 1, 2), 133: (2, 1, 3), 135: (2, 1, 1), 155: (3, 1, 2),
        159: (1, 1, 1), 161: (2, 1, 1)}
NO_INFLAMABLE = {135, 159}


def _solapa(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3] and a[4] < b[5] and b[4] < a[5]


# ======================================================================== farol detallado
def farol(o, cx, y0, cz, s=1.0, pie=True):
    """Farol de hierro: gota, base, 4 montantes, vidrios que brillan con aro, techito de 3 pisos, remate y argolla.
    (cx, cz) centro; y0 = abajo del farol. Alto ~1,05*s, ancho 0,5*s."""
    def b(x0, y_0, z0, x1, y_1, z1, c, g=0):
        o.f(cx + x0 * s, y0 + y_0 * s, cz + z0 * s, cx + x1 * s, y0 + y_1 * s, cz + z1 * s, c, 0, g)
    if pie:
        b(-0.06, 0.0, -0.06, 0.06, 0.08, 0.06, HIERRO)
    b(-0.15, 0.08, -0.15, 0.15, 0.13, 0.15, HIERRO)
    b(-0.23, 0.13, -0.23, 0.23, 0.21, 0.23, HIERRO2)
    for px in (-0.2, 0.2):
        for pz in (-0.2, 0.2):
            b(px - 0.04, 0.21, pz - 0.04, px + 0.04, 0.72, pz + 0.04, HIERRO)
    b(-0.17, 0.21, -0.17, 0.17, 0.72, 0.17, LUZ, 1)
    b(-0.185, 0.45, -0.185, 0.185, 0.49, 0.185, HIERRO)          # aro a media altura
    b(-0.25, 0.72, -0.25, 0.25, 0.78, 0.25, HIERRO2)
    b(-0.2, 0.78, -0.2, 0.2, 0.86, 0.2, HIERRO)
    b(-0.13, 0.86, -0.13, 0.13, 0.93, 0.13, HIERRO)
    b(-0.06, 0.93, -0.06, 0.06, 1.0, 0.06, HIERRO)
    b(-0.07, 1.0, -0.02, 0.07, 1.04, 0.02, HIERRO2)              # argolla
    b(-0.07, 1.04, -0.02, -0.03, 1.1, 0.02, HIERRO2)
    b(0.03, 1.04, -0.02, 0.07, 1.1, 0.02, HIERRO2)
    b(-0.07, 1.1, -0.02, 0.07, 1.13, 0.02, HIERRO2)


class Casa:
    """Caja de muros de x0..x1, z0..z1 (celdas de muro incluidas) sobre una acera en y=0."""

    def __init__(self, o: Obra, x0, z0, x1, z1, pisos=1, h=H_PISO, techo=True, muro="muro"):
        self.o, self.x0, self.z0, self.x1, self.z1, self.pisos, self.h = o, x0, z0, x1, z1, pisos, h
        self.s = 3
        self.suelos = [self.s + k * (h + 1) for k in range(pisos)]
        self.roof_y = self.s + pisos * h + (pisos - 1)
        self.muro = muro
        self.techo_on = techo
        self.caras = {
            "n": {"O": (x0, z0), "U": (1, 0), "N": (0, -1)},
            "s": {"O": (x0, z1 + 1), "U": (1, 0), "N": (0, 1)},
            "o": {"O": (x0, z0), "U": (0, 1), "N": (-1, 0)},
            "e": {"O": (x1 + 1, z0), "U": (0, 1), "N": (1, 0)},
        }
        self.huecos = []        # huecos de escalera en entrepisos: (y, xa, xb, za, zb)
        self.zonas = []         # (x0, z0, x1, z1, y0, y1, tipo, nombre)
        self.fuegos = []        # (x, z, y, radio)
        self.problemas = []
        self._cuerpo()
        if techo:
            self._techo()
        o.finales.append(self.terminar)

    # ---------------------------------------------------------------- geometria
    def celda(self, cara, u, y):
        if cara == "n": return (self.x0 + u, y, self.z0)
        if cara == "s": return (self.x0 + u, y, self.z1)
        if cara == "o": return (self.x0, y, self.z0 + u)
        return (self.x1, y, self.z0 + u)

    def punto(self, cara, u, w):
        (ox, oz), (ux, uz), (nx, nz) = self.caras[cara]["O"], self.caras[cara]["U"], self.caras[cara]["N"]
        return ox + ux * u + nx * w, oz + uz * u + nz * w

    def rect(self, cara, u0, w0, u1, w1):
        xa, za = self.punto(cara, u0, w0)
        xb, zb = self.punto(cara, u1, w1)
        return min(xa, xb), min(za, zb), max(xa, xb), max(za, zb)

    def largo(self, cara):
        return (self.x1 - self.x0 + 1) if cara in ("n", "s") else (self.z1 - self.z0 + 1)

    def piso_de(self, y):
        k = 0
        for i, s in enumerate(self.suelos):
            if y >= s - 0.01:
                k = i
        return k

    # ---------------------------------------------------------------- criterio
    def reservar(self, x0, z0, x1, z1, y0, y1, tipo, nombre):
        self.zonas.append((x0, z0, x1, z1, y0, y1, tipo, nombre))

    def ocupa(self, nombre, x0, z0, x1, z1, y0, y1, inflamable=True, exterior=False):
        """Registra un mueble/objeto y revisa que no pise pasos, ventanas ni quede pegado al fuego."""
        a = (x0, z0, x1, z1, y0, y1)
        for (zx0, zz0, zx1, zz1, zy0, zy1, tipo, zn) in self.zonas:
            if tipo == "ventana" and not exterior:
                continue
            if _solapa(a, (zx0, zz0, zx1, zz1, zy0, zy1)):
                self.problemas.append("%s pisa %s (%s)" % (nombre, zn, tipo))
        if inflamable:
            for (fx, fz, fy, r) in self.fuegos:
                if abs(fy - y0) > 3:
                    continue
                dx = max(x0 - fx, 0, fx - x1)
                dz = max(z0 - fz, 0, fz - z1)
                d = math.hypot(dx, dz)
                if d < r:
                    self.problemas.append("%s esta a %.1f del fuego (minimo %.1f)" % (nombre, d, r))

    def mueble(self, cat, x, y, z, rot=0, nombre=None, solid=0):
        w, d, h = DIMS[cat]
        if rot % 2:
            w, d = d, w
        self.ocupa(nombre or ("objeto %d" % cat), x, z, x + w, z + d, y, y + h, cat not in NO_INFLAMABLE)
        self.o.obj(cat, x, y, z, rot, solid)

    def revisar(self):
        if self.problemas:
            raise ValueError("%s: no cumple el criterio:\n  - " % self.o.nombre + "\n  - ".join(self.problemas))

    # ---------------------------------------------------------------- cuerpo y techo
    def _cuerpo(self):
        o, x0, z0, x1, z1 = self.o, self.x0, self.z0, self.x1, self.z1
        o.mbox(x0 - 1, 1, z0 - 1, x1 + 1, 2, z1 + 1, "zocalo")
        o.mbox(x0 + 1, 1, z0 + 1, x1 - 1, 2, z1 - 1, "piso")
        top = self.roof_y - 1
        for y in range(1, top + 1):
            for x in range(x0, x1 + 1):
                o.mat(x, y, z0, self.muro); o.mat(x, y, z1, self.muro)
            for z in range(z0, z1 + 1):
                o.mat(x0, y, z, self.muro); o.mat(x1, y, z, self.muro)
        for k in range(1, self.pisos):
            y = self.suelos[k] - 1
            o.mbox(x0 + 1, y, z0 + 1, x1 - 1, y, z1 - 1, "madera")
            for cn, c in self.caras.items():
                L = self.largo(cn)
                o.fc(c, -0.3, y + 0.55, 0, L + 0.3, y + 1.0, 0.3, (92, 98, 96))

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
        largos = ("n", "s") if (x1 - x0) >= (z1 - z0) else ("o", "e")
        for cn in largos:
            c = self.caras[cn]
            for u in range(2, self.largo(cn) - 1, 3):
                o.fc(c, u + 0.25, y - 0.45, -0.2, u + 0.75, y, 0.85, WDD, 2)

    def terminar(self):
        """Vigas interiores (cortadas en los huecos de escalera, con brochal) y revision del criterio."""
        o, x0, z0, x1, z1 = self.o, self.x0, self.z0, self.x1, self.z1
        for p in range(self.pisos):
            yc = (self.suelos[p + 1] - 1) if p + 1 < self.pisos else self.roof_y
            if p + 1 == self.pisos and not self.techo_on:
                continue
            huecos = [hh for hh in self.huecos if hh[0] == yc]
            por_x = (x1 - x0) >= (z1 - z0)
            for v in range(3, ((x1 - x0) if por_x else (z1 - z0)) - 1, 4):
                pos = (x0 if por_x else z0) + v
                segs = [((z0 if por_x else x0) + 1, (z1 if por_x else x1))]
                for (_, xa, xb, za, zb) in huecos:
                    ca, cb = (xa, xb) if por_x else (za, zb)        # rango del hueco en el eje de la viga
                    la, lb = (za, zb) if por_x else (xa, xb)        # rango a lo largo de la viga
                    if pos + 0.6 > ca and pos < cb:
                        nuevos = []
                        for (a, b) in segs:
                            if lb <= a or la >= b:
                                nuevos.append((a, b))
                                continue
                            if la > a:
                                nuevos.append((a, la - 0.6))
                            if lb < b:
                                nuevos.append((lb + 0.6, b))
                        segs = nuevos
                for (a, b) in segs:
                    if b - a < 0.5:
                        continue
                    if por_x:
                        o.f(pos, yc - 0.45, a, pos + 0.6, yc, b, WDD, 2)
                    else:
                        o.f(a, yc - 0.45, pos, b, yc, pos + 0.6, WDD, 2)
            # brochales: vigas que rodean el hueco (las vigas cortadas descansan en ellas)
            for (_, xa, xb, za, zb) in huecos:
                if por_x:
                    if za > z0 + 1:
                        o.f(xa - 0.6, yc - 0.45, za - 0.6, xb + 0.6, yc, za, WDD, 2)
                    if zb < z1:
                        o.f(xa - 0.6, yc - 0.45, zb, xb + 0.6, yc, zb + 0.6, WDD, 2)
                else:
                    if xa > x0 + 1:
                        o.f(xa - 0.6, yc - 0.45, za - 0.6, xa, yc, zb + 0.6, WDD, 2)
                    if xb < x1:
                        o.f(xb, yc - 0.45, za - 0.6, xb + 0.6, yc, zb + 0.6, WDD, 2)
        self.revisar()

    # ---------------------------------------------------------------- aberturas
    def ventana(self, cara, u, piso=0, flores=True, w=2, h=2):
        """Ventana abierta (se ve a traves): marco y cruz de madera oscura, repisa adentro, jardinera afuera."""
        o, c = self.o, self.caras[cara]
        yb = self.suelos[piso] + SILL
        for du in range(w):
            for dy in range(h):
                x, y, z = self.celda(cara, u + du, yb + dy)
                o.put(x, y, z, COL_INV)
        F = 0.17
        o.fc(c, u, yb, -0.72, u + F, yb + h, -0.28, WDD, 2)
        o.fc(c, u + w - F, yb, -0.72, u + w, yb + h, -0.28, WDD, 2)
        o.fc(c, u, yb + h - F, -0.72, u + w, yb + h, -0.28, WDD, 2)
        o.fc(c, u, yb, -0.72, u + w, yb + F, -0.28, WDD, 2)
        for k in range(1, w):
            o.fc(c, u + k - 0.05, yb + F, -0.56, u + k + 0.05, yb + h - F, -0.44, WDD)
        o.fc(c, u + F, yb + h / 2 - 0.05, -0.56, u + w - F, yb + h / 2 + 0.05, -0.44, WDD)
        o.fc(c, u - 0.1, yb - 0.12, -1.18, u + w + 0.1, yb + 0.02, -0.72, WD, 2)       # repisa interior
        x0, z0, x1, z1 = self.rect(cara, u - 0.4, 0.0, u + w + 0.4, 1.8)
        self.reservar(x0, z0, x1, z1, yb - 0.7, yb + h + 0.4, "ventana", "ventana %s%d" % (cara, u))
        if flores:
            self.jardinera(c, u, yb, w)
        else:
            o.fc(c, u - 0.12, yb - 0.16, -0.28, u + w + 0.12, yb + 0.02, 0.25, PIEDRA_F)

    def jardinera(self, c, u, yb, w=2):
        o = self.o
        o.fc(c, u - 0.2, yb - 0.6, 0.0, u + w + 0.2, yb - 0.04, 0.62, FLOR_CAJA)
        o.fc(c, u - 0.24, yb - 0.66, 0.0, u + w + 0.24, yb - 0.56, 0.66, (204, 192, 166))
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
        o.fc(c, u - 0.45, yb + 3, -0.05, u + w + 0.45, yb + 3.4, 0.3, WDD, 2)
        o.fc(c, u + F, yb - 0.04, -1.0, u + w - F, yb + 0.02, 0.0, PIEDRA_F)
        if escalones and piso == 0:
            for du in range(-1, w + 1):
                (x, _, z) = self.celda(cara, u + du, 0)
                dx, dz = c["N"]
                o.mat(x + dx, 1, z + dz, "zocalo")
                o.mat(x + 2 * dx, 1, z + 2 * dz, "piedra")
        xa, za, xb, zb = self.rect(cara, u - 1, -1, u + w + 1, -4)
        self.reservar(xa, za, xb, zb, yb, yb + 3, "paso", "paso de la puerta %s (dentro)" % cara)
        xa, za, xb, zb = self.rect(cara, u - 1, 0, u + w + 1, 3)
        self.reservar(xa, za, xb, zb, 0, yb + 3, "paso", "paso de la puerta %s (fuera)" % cara)

    # ---------------------------------------------------------------- carteles y faroles
    def cartel_colgante(self, cara, u, y, simbolo="jarra"):
        """Cartel de dos caras colgado con cadenas de un brazo de hierro con voluta, perpendicular a la fachada.
        Tablero de dos tablones con marco, esquineros de hierro y el simbolo pintado en ambas caras."""
        o, c = self.o, self.caras[cara]
        x0, z0, x1, z1 = self.rect(cara, u - 0.3, 0, u + 0.3, 1.7)
        self.ocupa("cartel %s" % simbolo, x0, z0, x1, z1, y, y + 2, False, exterior=True)
        # placa en el muro, brazo y voluta
        o.fc(c, u - 0.2, y + 1.45, 0.0, u + 0.2, y + 2.05, 0.06, HIERRO)
        o.fc(c, u - 0.05, y + 1.82, 0.0, u + 0.05, y + 1.92, 1.7, HIERRO)
        o.fc(c, u - 0.06, y + 1.8, 1.6, u + 0.06, y + 1.94, 1.74, HIERRO2)
        for i, (w0, v0) in enumerate(((0.06, 1.5), (0.22, 1.58), (0.38, 1.66), (0.54, 1.74))):
            o.fc(c, u - 0.04, y + v0, w0, u + 0.04, y + v0 + 0.1, w0 + 0.18, HIERRO)
        o.fc(c, u - 0.04, y + 1.92, 0.25, u + 0.04, y + 2.02, 0.45, HIERRO2)       # rizo arriba
        o.fc(c, u - 0.04, y + 2.02, 0.4, u + 0.04, y + 2.1, 0.5, HIERRO2)
        # cadenas (eslabones alternados)
        for wv in (0.55, 1.45):
            v = y + 1.82
            k = 0
            while v > y + 1.5:
                if k % 2:
                    o.fc(c, u - 0.05, v - 0.09, wv - 0.015, u + 0.05, v, wv + 0.015, HIERRO2)
                else:
                    o.fc(c, u - 0.015, v - 0.09, wv - 0.05, u + 0.015, v, wv + 0.05, HIERRO2)
                v -= 0.08
                k += 1
        # tablero
        A, B, V0, V1 = 0.35, 1.65, y + 0.25, y + 1.5
        o.fc(c, u - 0.06, V0, A, u + 0.06, V1, (A + B) / 2, (156, 110, 66), 2)
        o.fc(c, u - 0.06, V0, (A + B) / 2, u + 0.06, V1, B, (146, 100, 60), 2)
        o.fc(c, u - 0.07, V0 + 0.1, (A + B) / 2 - 0.015, u + 0.07, V1 - 0.1, (A + B) / 2 + 0.015, (90, 58, 36))
        for (a, b, va, vb) in ((A - 0.06, B + 0.06, V1 - 0.04, V1 + 0.08), (A - 0.06, B + 0.06, V0 - 0.08, V0 + 0.04),
                               (A - 0.06, A + 0.06, V0, V1), (B - 0.06, B + 0.06, V0, V1)):
            o.fc(c, u - 0.09, va, a, u + 0.09, vb, b, (92, 60, 38), 2)
        for (a, va) in ((A - 0.08, V1 - 0.06), (B - 0.1, V1 - 0.06), (A - 0.08, V0 - 0.1), (B - 0.1, V0 - 0.1)):
            o.fc(c, u - 0.1, va, a, u + 0.1, va + 0.16, a + 0.18, HIERRO)
        # simbolo en las dos caras
        mid = (A + B) / 2
        vc = (V0 + V1) / 2
        for sg in (-1, 1):
            u0, u1 = (u + 0.09, u + 0.11) if sg > 0 else (u - 0.11, u - 0.09)
            u2, u3 = (u + 0.11, u + 0.13) if sg > 0 else (u - 0.13, u - 0.11)

            def P(w0, v0, w1, v1, col, alto=False):
                a0, a1 = (u2, u3) if alto else (u0, u1)
                o.fc(c, a0, vc + v0, mid + w0, a1, vc + v1, mid + w1, col)
            if simbolo == "jarra":
                P(-0.26, -0.32, 0.14, 0.2, (214, 150, 52))               # cuerpo
                P(-0.26, -0.24, 0.14, -0.18, (150, 96, 34), True)        # aros
                P(-0.26, 0.06, 0.14, 0.12, (150, 96, 34), True)
                P(-0.2, -0.3, -0.13, 0.16, (246, 196, 96), True)          # brillo
                P(0.14, -0.18, 0.2, 0.12, (150, 96, 34))                  # asa
                P(0.2, -0.14, 0.27, 0.08, (150, 96, 34))
                P(-0.3, 0.2, 0.18, 0.32, (250, 248, 240))                 # espuma
                P(-0.24, 0.32, -0.08, 0.38, (250, 248, 240))
                P(-0.02, 0.32, 0.12, 0.37, (250, 248, 240))
                P(0.08, 0.06, 0.14, 0.22, (250, 248, 240), True)          # gota de espuma
            else:   # escudo con espadas cruzadas
                P(-0.3, -0.18, 0.3, 0.36, (220, 180, 70))
                P(-0.22, -0.28, 0.22, -0.18, (220, 180, 70))
                P(-0.12, -0.36, 0.12, -0.28, (220, 180, 70))
                P(-0.24, -0.12, 0.24, 0.3, (52, 84, 150), True)
                P(-0.16, -0.22, 0.16, -0.12, (52, 84, 150), True)
                for i in range(5):
                    t = -0.2 + i * 0.1
                    P(t - 0.03, t - 0.04, t + 0.03, t + 0.04, (232, 232, 240), True)
                    P(-t - 0.03, t - 0.04, -t + 0.03, t + 0.04, (232, 232, 240), True)
                P(-0.06, 0.18, 0.06, 0.26, (220, 180, 70), True)

    def farol_pared(self, cara, u, y, interior=True):
        """Farol de hierro colgado de un brazo con voluta. u = centro a lo largo del muro; y = abajo del farol."""
        o, c = self.o, self.caras[cara]
        sg = -1 if interior else 1
        w0 = -1.0 if interior else 0.0
        top = y + 1.25
        o.fc(c, u - 0.14, top - 0.42, w0, u + 0.14, top + 0.12, w0 + sg * 0.05, HIERRO)          # placa
        o.fc(c, u - 0.1, top - 0.36, w0 + sg * 0.05, u + 0.1, top + 0.06, w0 + sg * 0.07, HIERRO2)
        o.fc(c, u - 0.035, top, w0, u + 0.035, top + 0.07, w0 + sg * 0.62, HIERRO)                # brazo
        for i in range(4):                                                                         # voluta
            o.fc(c, u - 0.03, top - 0.32 + i * 0.08, w0 + sg * (0.05 + i * 0.09), u + 0.03, top - 0.24 + i * 0.08, w0 + sg * (0.15 + i * 0.09), HIERRO)
        o.fc(c, u - 0.03, top + 0.07, w0 + sg * 0.5, u + 0.03, top + 0.14, w0 + sg * 0.62, HIERRO2)
        o.fc(c, u - 0.02, top - 0.1, w0 + sg * 0.47, u + 0.02, top, w0 + sg * 0.51, HIERRO2)       # gancho
        cx, cz = self.punto(cara, u, w0 + sg * 0.49)
        farol(o, cx, top - 1.23, cz, 1.0)
        if not interior:
            x0, z0, x1, z1 = self.rect(cara, u - 0.3, 0, u + 0.3, 0.8)
            self.ocupa("farol de pared", x0, z0, x1, z1, top - 1.3, top + 0.2, False, exterior=True)

    def enredadera(self, cara, u, y0, y1, ancho=0.9):
        """Enredadera fina: tallos delgados que suben con quiebres, ramitas laterales y hojas chicas de 3 verdes."""
        o, c = self.o, self.caras[cara]
        verdes = ((56, 132, 46), (78, 160, 58), (104, 184, 72))
        tallo = (74, 92, 40)
        for t, du0 in enumerate((-ancho * 0.3, ancho * 0.25)):
            uu = u + du0
            y = y0
            k = 0
            top = y1 - (t * 0.9)
            while y < top:
                paso = 0.22
                uu += ((_h(cara, u, t, k) % 5) - 2) * 0.03
                uu = max(u - ancho / 2, min(u + ancho / 2, uu))
                o.fc(c, uu - 0.025, y, 0.0, uu + 0.025, y + paso + 0.02, 0.04, tallo)
                r = _h(cara, u, t, k, 1) % 6
                if r < 4:
                    sgn = -1 if r % 2 else 1
                    lu = uu + sgn * (0.07 + (r % 3) * 0.03)
                    sz = 0.07 + (r % 2) * 0.025
                    o.fc(c, lu - sz, y + 0.04, 0.01, lu + sz, y + 0.04 + sz * 1.6, 0.07, verdes[(k + t) % 3])
                if r == 5 and y < top - 0.5:          # ramita lateral con dos hojas
                    sgn = -1 if k % 2 else 1
                    o.fc(c, min(uu, uu + sgn * 0.3), y + 0.1, 0.0, max(uu, uu + sgn * 0.3), y + 0.13, 0.035, tallo)
                    for j in (0.15, 0.3):
                        lu = uu + sgn * j
                        o.fc(c, lu - 0.06, y + 0.13, 0.01, lu + 0.06, y + 0.25, 0.06, verdes[(k + 2) % 3])
                if (k + t) % 11 == 7:
                    o.fc(c, uu + 0.04, y + 0.12, 0.03, uu + 0.1, y + 0.18, 0.08, (236, 232, 246))
                y += paso
                k += 1

    # ---------------------------------------------------------------- chimenea
    def chimenea(self, cara, u, w=2):
        """Hogar metido en un nicho de piedra de w x 3 x 2 de fondo, con fuego chico al fondo (lenos, morillos,
        brasas, llamas), solera de piedra que entra 0,6 a la sala, marco de piedra y repisa de madera.
        El cuerpo de piedra es de seccion constante (w+2 x 2) desde el zocalo hasta 1 sobre la cumbre, con
        remate centrado y boca de humo; por dentro el nicho es cerrado (fondo, lados y campana)."""
        o, c = self.o, self.caras[cara]
        nx, nz = c["N"]
        s = self.suelos[0]
        top = self.cumbre + 1
        for du in range(-1, w + 1):
            for dw in (1, 2):
                for y in range(1, top + 1):
                    x, _, z = self.celda(cara, u + du, 0)
                    o.mat(x + nx * dw, y, z + nz * dw, "chimenea")
        for du in range(w):
            for y in range(s, s + 3):
                x, _, z = self.celda(cara, u + du, 0)
                o.clear(x, y, z)
                o.clear(x + nx, y, z + nz)
            for y in (s, s + 1):            # no se entra al fuego
                x, _, z = self.celda(cara, u + du, 0)
                o.put(x + nx, y, z + nz, COL_INV)
        # remate centrado sobre el cuerpo (u -1..w+1, w 0..2) y boca de humo
        o.fc(c, u - 1.12, top + 1, -0.12, u + w + 1.12, top + 1.22, 2.12, PIEDRA_F)
        for (a, b, wa, wb) in ((u - 0.9, u + w + 0.9, 0.1, 0.35), (u - 0.9, u + w + 0.9, 1.65, 1.9),
                               (u - 0.9, u - 0.65, 0.35, 1.65), (u + w + 0.65, u + w + 0.9, 0.35, 1.65)):
            o.fc(c, a, top + 1.22, wa, b, top + 1.5, wb, PIEDRA_F)
        o.fc(c, u - 0.65, top + 1.22, 0.35, u + w + 0.65, top + 1.26, 1.65, (30, 26, 24))
        # dentro del nicho: hollin, solera, morillos, lenos, brasas y llamas
        o.fc(c, u + 0.1, s + 0.2, 0.96, u + w - 0.1, s + 2.8, 1.0, (52, 46, 42))
        o.fc(c, u, s, -1.0, u + w, s + 0.12, 1.0, (120, 114, 106))
        o.fc(c, u - 0.5, s, -1.6, u + w + 0.5, s + 0.12, -1.0, (132, 126, 118))
        for a in (u + 0.35, u + w - 0.45):
            o.fc(c, a, s + 0.12, 0.05, a + 0.1, s + 0.4, 0.75, HIERRO)
            o.fc(c, a, s + 0.4, 0.05, a + 0.1, s + 0.55, 0.15, HIERRO)
        for (wa, va, col) in ((0.15, 0.12, (102, 66, 40)), (0.45, 0.12, (92, 60, 36)), (0.3, 0.32, (110, 72, 44))):
            o.fc(c, u + 0.25, s + va, wa, u + w - 0.25, s + va + 0.2, wa + 0.22, col)
            o.fc(c, u + 0.22, s + va + 0.03, wa + 0.03, u + 0.26, s + va + 0.17, wa + 0.19, (196, 160, 110))
        o.fc(c, u + 0.4, s + 0.12, 0.1, u + w - 0.4, s + 0.16, 0.72, (255, 110, 30), 1)
        m = u + w / 2.0
        o.fc(c, m - 0.32, s + 0.5, 0.22, m + 0.32, s + 0.85, 0.6, (255, 128, 36), 1)
        o.fc(c, m - 0.2, s + 0.85, 0.28, m + 0.2, s + 1.15, 0.54, (255, 170, 50), 1)
        o.fc(c, m - 0.1, s + 1.15, 0.33, m + 0.1, s + 1.35, 0.48, (255, 222, 110), 1)
        for sg in (-1, 1):
            o.fc(c, m + sg * 0.45 - 0.1, s + 0.5, 0.3, m + sg * 0.45 + 0.1, s + 0.8, 0.5, (255, 150, 44), 1)
        # marco de piedra y repisa de madera (por dentro de la sala)
        o.fc(c, u - 0.35, s, -1.12, u, s + 3.0, -1.0, PIEDRA_F)
        o.fc(c, u + w, s, -1.12, u + w + 0.35, s + 3.0, -1.0, PIEDRA_F)
        o.fc(c, u - 0.35, s + 3.0, -1.12, u + w + 0.35, s + 3.3, -1.0, PIEDRA_F)
        o.fc(c, u - 0.6, s + 3.3, -1.4, u + w + 0.6, s + 3.5, -1.0, WD, 2)
        for a in (u - 0.5, u + w + 0.3):
            o.fc(c, a, s + 3.1, -1.3, a + 0.2, s + 3.3, -1.0, WDD)
        # criterio: radio de fuego y paso libre delante del hogar
        fx, fz = self.punto(cara, m, 0.4)
        self.fuegos.append((fx, fz, s, 2.5))
        xa, za, xb, zb = self.rect(cara, u - 0.5, -1.0, u + w + 0.5, -2.6)
        self.reservar(xa, za, xb, zb, s, s + 2, "paso", "frente del hogar")

    # ---------------------------------------------------------------- interior
    def alfombra(self, x0, z0, x1, z1, piso, a, b, borde=0.6):
        y = self.suelos[piso]
        o = self.o
        o.f(x0, y, z0, x1, y + 0.05, z1, a)
        o.f(x0 + borde, y + 0.05, z0 + borde, x1 - borde, y + 0.07, z1 - borde, b)
        o.f(x0 + borde + 0.5, y + 0.07, z0 + borde + 0.5, x1 - borde - 0.5, y + 0.09, z1 - borde - 0.5, a)

    def cama_con_cofre(self, x, y, z, rot):
        """Cama (2x4) con el cofre a los pies, pegado y mirando hacia afuera (nunca hacia la cama).
        rot 0: cabecera en +Z; rot 2: cabecera en -Z; rot 1: cabecera en +X... (como el catalogo)."""
        self.mueble(121, x, y, z, rot, "cama")
        o = self.o
        # el cuerpo de la cama ocupa 3,25 de los 4 de la huella; el pie esta del lado opuesto a la cabecera
        if rot == 0:
            o.obj(122, x, y, z + 0.75 - 1.05, 0)
            self.ocupa("cofre", x, z - 0.3, x + 2, z + 0.7, y, y + 2)
        elif rot == 2:
            o.obj(122, x, y, z + 3.25 + 0.05, 2)
            self.ocupa("cofre", x, z + 3.3, x + 2, z + 4.3, y, y + 2)
        elif rot == 1:
            o.obj(122, x + 3.25 + 0.05, y, z, 1)
            self.ocupa("cofre", x + 3.3, z, x + 4.3, z + 2, y, y + 2)
        else:
            o.obj(122, x - 0.3, y, z, 3)
            self.ocupa("cofre", x - 0.3, z, x + 0.7, z + 2, y, y + 2)


def planta(o, x, y, z, grande=False, casa=None):
    """Planta en maceta de barro (estilo Cube World)."""
    if casa:
        casa.ocupa("planta", x, z, x + 1, z + 1, y, y + 2)
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


def jarron_flores(o, x, y, z, casa=None):
    if casa:
        casa.ocupa("jarron", x, z, x + 1, z + 1, y, y + 1)
    o.f(x + 0.3, y, z + 0.3, x + 0.7, y + 0.15, z + 0.7, (200, 196, 188))
    o.f(x + 0.22, y + 0.15, z + 0.22, x + 0.78, y + 0.65, z + 0.78, (210, 206, 198))
    o.f(x + 0.32, y + 0.65, z + 0.32, x + 0.68, y + 0.85, z + 0.68, (200, 196, 188))
    for i in range(6):
        dx, dz = ((i * 37) % 5) * 0.08 - 0.16, ((i * 53) % 5) * 0.08 - 0.16
        hh = 1.0 + (i % 3) * 0.2
        o.f(x + 0.47 + dx, y + 0.85, z + 0.47 + dz, x + 0.53 + dx, y + hh, z + 0.53 + dz, (60, 110, 40))
        o.f(x + 0.4 + dx, y + hh, z + 0.4 + dz, x + 0.6 + dx, y + hh + 0.2, z + 0.6 + dz, (190, 40, 110) if i % 2 else (220, 60, 130))


# ======================================================================== piezas extra
_PL = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "plantillas.json"), encoding="utf-8"))


def mesa_redonda(o, cx, y, cz, casa=None):
    """Mesa redonda con pedestal de la Taberna de Ivan (2,5 de diametro, 1,5 de alto), centrada en (cx, cz)."""
    if casa:
        casa.ocupa("mesa redonda", cx - 1.25, cz - 1.25, cx + 1.25, cz + 1.25, y, y + 1.5)
    for u0, u1, y0, y1, w0, w1, r, g, b, pat, glow in _PL["mesa_redonda"]:
        o.f(cx + u0, y + y0, cz + w0, cx + u1, y + y1, cz + w1, (r, g, b), pat, glow)
    o.put(int(math.floor(cx)), y, int(math.floor(cz)), COL_INV)


def escalera(c: Casa, x0, z0, z1, piso=0, dx=1):
    """Escalera recta de bloques de madera (1 de huella x 1 de contrahuella) que sube en +X (dx=1) o -X (dx=-1).
    Abre el hueco en el entrepiso (las vigas se cortan ahi y descansan en brochales) y pone una baranda robusta:
    pilares de 0,26 con capitel en las esquinas, pasamanos ancho, zocalo y balaustres cada 0,5."""
    o = c.o
    s = c.suelos[piso]
    n = c.suelos[piso + 1] - s
    for k in range(1, n + 1):
        x = x0 + (k - 1) * dx
        o.mbox(x, s, z0, x, s + k - 1, z1, "madera")
        # canto de cada peldano mas claro (se lee la escalera)
        xe = x if dx == 1 else x + 1
        o.f(xe - 0.02 if dx == 1 else xe - 0.02, s + k - 0.1, z0, xe + 0.02, s + k, z1 + 1, (150, 104, 64))
    yl = c.suelos[piso + 1] - 1
    hx = [x0 + (k - 1) * dx for k in range(1, n)]
    for x in hx:
        for z in range(z0, z1 + 1):
            o.clear(x, yl, z)
    xa, xb = min(hx), max(hx) + 1
    c.huecos.append((yl, xa, xb, z0, z1 + 1))
    # pie de la escalera libre (abajo) y llegada libre (arriba)
    pie = x0 - 2 if dx == 1 else x0 + 1
    c.reservar(pie, z0, pie + 2, z1 + 1, s, s + 3, "paso", "pie de la escalera")
    c.reservar(x0, z0 - 0.0, x0 + (n if dx == 1 else 1), z1 + 1, s, s + n, "paso", "escalera")
    lleg = xb if dx == 1 else xa - 2
    c.reservar(lleg, z0, lleg + 2, z1 + 1, s + n, s + n + 3, "paso", "llegada de la escalera")
    # baranda arriba: lado abierto (largo) + extremo bajo
    ya = c.suelos[piso + 1]
    abierto_z0 = z0 > c.z0 + 1
    zr = (z0 - 0.26) if abierto_z0 else (z1 + 1)
    xe = (xa - 0.26) if dx == 1 else xb
    H = 1.15
    MAD, MADO, MADC = (124, 82, 50), (84, 54, 34), (146, 100, 62)

    def pilar(px, pz):
        o.f(px, ya, pz, px + 0.26, ya + H + 0.15, pz + 0.26, MADO, 2)
        o.f(px - 0.04, ya + H + 0.15, pz - 0.04, px + 0.3, ya + H + 0.25, pz + 0.3, MADC, 2)
        o.f(px + 0.06, ya + H + 0.25, pz + 0.06, px + 0.2, ya + H + 0.33, pz + 0.2, MADC)
    # lado largo
    pilar(xa - 0.26, zr)
    pilar(xb - 0.26 if dx == 1 else xb, zr)
    xm = (xa + xb) / 2.0 - 0.13
    pilar(xm, zr)
    o.f(xa - 0.26, ya + H - 0.12, zr - 0.03, xb, ya + H + 0.04, zr + 0.29, MAD, 2)      # pasamanos
    o.f(xa - 0.26, ya, zr + 0.03, xb, ya + 0.16, zr + 0.23, MADO, 2)                  # zocalo
    xx = xa + 0.25
    while xx < xb - 0.3:
        if abs(xx - (xm + 0.13)) > 0.25:
            o.f(xx - 0.05, ya + 0.16, zr + 0.08, xx + 0.05, ya + H - 0.12, zr + 0.18, MADO)
        xx += 0.5
    # extremo bajo (del pilar de la esquina hasta el muro)
    zw0, zw1 = (z0 - 0.26, z1 + 1) if abierto_z0 else (z0, z1 + 1.26)
    o.f(xe, ya + H - 0.12, zw0, xe + 0.26, ya + H + 0.04, zw1, MAD, 2)
    o.f(xe, ya, zw0, xe + 0.26, ya + 0.16, zw1, MADO, 2)
    zz = zw0 + 0.4
    while zz < zw1 - 0.2:
        o.f(xe + 0.08, ya + 0.16, zz - 0.05, xe + 0.18, ya + H - 0.12, zz + 0.05, MADO)
        zz += 0.5
    if dx != 1:
        pilar(xe, zr)
    # colision de la baranda
    zc = z0 - 1 if abierto_z0 else z1 + 1
    for x in range(xa, xb):
        o.put(x, ya, zc, COL_INV); o.put(x, ya + 1, zc, COL_INV)
    for z in range(z0, z1 + 1):
        xc = xa - 1 if dx == 1 else xb
        o.put(xc, ya, z, COL_INV); o.put(xc, ya + 1, z, COL_INV)


def barra(o, x0, z0, x1, z1, y, frente="n", casa=None, nombre="mostrador"):
    """Mostrador de madera de 1,3 de alto (celdas x0..x1, z0..z1): cuerpo con paneles enmarcados del lado del cliente,
    zocalo oscuro metido, tapa con vuelo parejo de 0,08 en los extremos y 0,18 hacia el cliente (nada mas)."""
    if casa:
        casa.ocupa(nombre, x0, z0, x1 + 1, z1 + 1, y, y + 1.3)
    X0, X1, Z0, Z1 = x0, x1 + 1, z0, z1 + 1
    CU, CUO, TAPA = (128, 84, 52), (96, 62, 38), (78, 50, 32)
    o.f(X0 + 0.06, y, Z0 + 0.06, X1 - 0.06, y + 0.15, Z1 - 0.06, (70, 46, 30))           # zocalo metido
    o.f(X0, y + 0.15, Z0, X1, y + 1.15, Z1, CU, 2)
    # paneles del frente: marco (montantes y travesanos) en relieve
    if frente in ("n", "s"):
        zf = Z0 - 0.04 if frente == "n" else Z1
        L = X1 - X0
        n = max(1, int(round(L / 1.6)))
        pw = L / n
        for i in range(n + 1):
            xx = X0 + i * pw
            o.f(max(X0, xx - 0.07), y + 0.15, zf, min(X1, xx + 0.07), y + 1.15, zf + 0.04, CUO, 2)
        o.f(X0, y + 0.15, zf, X1, y + 0.27, zf + 0.04, CUO, 2)
        o.f(X0, y + 1.03, zf, X1, y + 1.15, zf + 0.04, CUO, 2)
        a0 = Z0 - 0.18 if frente == "n" else Z0 - 0.04
        a1 = Z1 + 0.04 if frente == "n" else Z1 + 0.18
        o.f(X0 - 0.08, y + 1.15, a0, X1 + 0.08, y + 1.3, a1, TAPA, 2)
    else:
        xf = X0 - 0.04 if frente == "o" else X1
        L = Z1 - Z0
        n = max(1, int(round(L / 1.6)))
        pw = L / n
        for i in range(n + 1):
            zz = Z0 + i * pw
            o.f(xf, y + 0.15, max(Z0, zz - 0.07), xf + 0.04, y + 1.15, min(Z1, zz + 0.07), CUO, 2)
        o.f(xf, y + 0.15, Z0, xf + 0.04, y + 0.27, Z1, CUO, 2)
        o.f(xf, y + 1.03, Z0, xf + 0.04, y + 1.15, Z1, CUO, 2)
        a0 = X0 - 0.18 if frente == "o" else X0 - 0.04
        a1 = X1 + 0.04 if frente == "o" else X1 + 0.18
        o.f(a0, y + 1.15, Z0 - 0.08, a1, y + 1.3, Z1 + 0.08, TAPA, 2)
    o.box(x0, y, z0, x1, y + 1, z1, COL_INV)


def tablero(o, cara_casa, c, u, y, ancho=3):
    """Tablero de misiones colgado en el muro (cara interior): marco de madera, corcho y papeles con chinche."""
    cara = c.caras[cara_casa]
    o.fc(cara, u, y, -1.0, u + ancho, y + 2.2, -1.12, WDD, 2)
    o.fc(cara, u + 0.15, y + 0.15, -1.12, u + ancho - 0.15, y + 2.05, -1.16, (176, 132, 84))
    papeles = [(0.3, 1.3, 0.7, 0.6), (1.2, 1.4, 0.6, 0.5), (2.0, 1.1, 0.7, 0.75), (0.5, 0.35, 0.8, 0.6), (1.6, 0.3, 0.7, 0.6)]
    for i, (pu, pv, pw, ph) in enumerate(papeles):
        if pu + pw > ancho - 0.15:
            continue
        col = (238, 230, 206) if i % 2 == 0 else (226, 214, 176)
        o.fc(cara, u + pu, y + pv, -1.16, u + pu + pw, y + pv + ph, -1.19, col)
        for j in range(3):
            o.fc(cara, u + pu + 0.1, y + pv + ph - 0.22 - j * 0.12, -1.19, u + pu + pw - 0.12 - (j % 2) * 0.15, y + pv + ph - 0.19 - j * 0.12, -1.2, (120, 110, 100))
        o.fc(cara, u + pu + pw / 2 - 0.05, y + pv + ph - 0.1, -1.19, u + pu + pw / 2 + 0.05, y + pv + ph, -1.23, (180, 40, 40))
    xa, za, xb, zb = c.rect(cara_casa, u, -1.0, u + ancho, -2.5)
    c.reservar(xa, za, xb, zb, y - 1.5, y + 1, "paso", "frente del tablero")
