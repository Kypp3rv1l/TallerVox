# Farlands Taller v0.1.8 - ayudas para modelar con voxeles en rejilla (como Cube World).
#   Pieza: objeto armado en su marco local (frente a -Z con rot 0) y girado igual que el catalogo del juego.
#   Vox:   rejilla de voxeles de tamano fijo que se funde en cajas grandes (pocas cajas, sin solapes).
#   torno: solido de revolucion en rejilla (barriles, ollas, sacos, frascos...).
import math


def _rot(px, pz, W, D, rot):
    r = rot % 4
    if r == 0:
        return px, pz
    if r == 1:
        return D - pz, px
    if r == 2:
        return W - px, D - pz
    return pz, W - px


class Pieza:
    def __init__(self, W, D):
        self.W, self.D, self.b = W, D, []

    def f(self, x0, y0, z0, x1, y1, z1, col, pat=0, glow=0):
        self.b.append((min(x0, x1), min(y0, y1), min(z0, z1), max(x0, x1), max(y0, y1), max(z0, z1), col, pat, glow))

    def vox(self, v, ox=0.0, oy=0.0, oz=0.0, pat=0):
        for (x0, y0, z0, x1, y1, z1, col, glow) in v.cajas(ox, oy, oz):
            self.f(x0, y0, z0, x1, y1, z1, col, pat, glow)

    def poner(self, o, x, y, z, rot=0):
        for (x0, y0, z0, x1, y1, z1, col, pat, glow) in self.b:
            ax, az = _rot(x0, z0, self.W, self.D, rot)
            bx, bz = _rot(x1, z1, self.W, self.D, rot)
            o.f(x + min(ax, bx), y + y0, z + min(az, bz), x + max(ax, bx), y + y1, z + max(az, bz), col, pat, glow)


class Vox:
    """Rejilla de voxeles de lado 'c'. Clave (i, j, k) = (x, y, z) en celdas."""

    def __init__(self, c=0.125):
        self.c, self.v = c, {}

    def set(self, i, j, k, col, glow=0, pisar=True):
        if not pisar and (i, j, k) in self.v:
            return
        self.v[(i, j, k)] = (tuple(int(max(0, min(255, q))) for q in col), glow)

    def caja(self, i0, j0, k0, i1, j1, k1, col, glow=0, pisar=True):   # extremos exclusivos
        for i in range(i0, i1):
            for j in range(j0, j1):
                for k in range(k0, k1):
                    self.set(i, j, k, col, glow, pisar)

    def get(self, i, j, k):
        return self.v.get((i, j, k))

    def cajas(self, ox=0.0, oy=0.0, oz=0.0):
        """Funde voxeles iguales en cajas (primero en x, luego en y, luego en z)."""
        c = self.c
        left = dict(self.v)
        out = []
        for key in sorted(self.v, key=lambda t: (t[2], t[1], t[0])):
            if key not in left:
                continue
            col = left[key]
            i, j, k = key
            i1 = i + 1
            while left.get((i1, j, k)) == col:
                i1 += 1
            j1 = j + 1
            while all(left.get((ii, j1, k)) == col for ii in range(i, i1)):
                j1 += 1
            k1 = k + 1
            while all(left.get((ii, jj, k1)) == col for ii in range(i, i1) for jj in range(j, j1)):
                k1 += 1
            for ii in range(i, i1):
                for jj in range(j, j1):
                    for kk in range(k, k1):
                        del left[(ii, jj, kk)]
            out.append((ox + i * c, oy + j * c, oz + k * c, ox + i1 * c, oy + j1 * c, oz + k1 * c, col[0], col[1]))
        return out

    def poner(self, o, ox, oy, oz, pat=0):
        for (x0, y0, z0, x1, y1, z1, col, glow) in self.cajas(ox, oy, oz):
            o.f(x0, y0, z0, x1, y1, z1, col, pat, glow)


def torno(v, ci, ck, j0, perfil, color, hueco=True):
    """Solido de revolucion: centro (ci, ck) en celdas (puede ser x.5), perfil = lista de radios (celdas) por capa desde j0.
    color(ang, capa, borde) -> rgb.  Si hueco, solo la cascara (y la tapa de la ultima capa)."""
    n = len(perfil)
    R = int(math.ceil(max(perfil))) + 1
    for t, r in enumerate(perfil):
        for di in range(-R, R + 1):
            for dk in range(-R, R + 1):
                x, z = di + 0.5 + math.floor(ci) - ci, dk + 0.5 + math.floor(ck) - ck
                d = math.hypot(x, z)
                if d > r:
                    continue
                borde = d > r - 1.0
                tapa = t == n - 1 or t == 0
                if hueco and not borde and not tapa:
                    continue
                ang = math.atan2(z, x)
                v.set(int(math.floor(ci)) + di, j0 + t, int(math.floor(ck)) + dk, color(ang, t, borde))
