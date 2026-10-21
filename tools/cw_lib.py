# Farlands Taller - armar creaciones desde Python con el estilo de Cube World (v0.1.5)
#
# Coordenadas LOCALES en bloques: x 0..W-1, y 0.. (0 = primer bloque sobre el suelo plano), z 0..D-1.
# Dos formas de poner materia:
#   - put/box: bloques reales del juego (ids de docs/ids.md).
#   - mat/mbox: "material liso" estilo Cube World: la celda lleva un bloque invisible solido (colision) y,
#     si alguna cara queda a la vista, una caja fina de 1x1x1 con el color del material y una leve variacion
#     de tono por bloque (sin dibujo de ladrillo). Es lo que hace que los muros se vean como en Cube World.
import json, hashlib

COL_INV = 89      # colision invisible (deja pasar la luz: ventanas)
SHELL = 90        # solido invisible que tapa el cielo (muros, techos: el interior queda en penumbra)

# material -> (rgb base, variacion de tono +-, patron del shader (0 liso, 1 piedra, 2 tablas, 4 revoque))
MATS = {
    "muro":     ((186, 176, 140), 7, 0),
    "muro_os":  ((150, 146, 122), 6, 0),
    "zocalo":   ((98, 106, 102), 5, 0),
    "techo":    ((46, 86, 82), 5, 0),
    "piso":     ((156, 152, 138), 5, 0),
    "piedra":   ((128, 124, 116), 6, 0),
    "chimenea": ((118, 112, 104), 6, 0),
    "tierra":   ((156, 104, 64), 6, 0),
    "tierra_os": ((128, 84, 52), 5, 0),
    "pasto":    ((96, 196, 64), 7, 0),
    "pasto_os": ((70, 160, 52), 6, 0),
    "madera":   ((112, 72, 44), 5, 2),
    "acera":    ((196, 194, 184), 6, 0),
    "acera_os": ((172, 170, 160), 6, 0),
    "tronco":   ((112, 80, 50), 6, 0),
    "hoja":     ((74, 178, 62), 8, 0),
    "hoja_os":  ((52, 146, 52), 7, 0),
}

WD = (120, 80, 50)      # madera
WDD = (82, 54, 34)      # madera oscura
IRON = (40, 40, 44)


def _h(*a):
    return int(hashlib.md5(repr(a).encode()).hexdigest()[:8], 16)


class Obra:
    def __init__(self, nombre, W, H, D, desc="", entry=(0, 0, "norte")):
        self.nombre, self.W, self.H, self.D, self.desc, self.entry = nombre, W, H, D, desc, entry
        self.cubes = {}          # (x,y,z) -> id de bloque real
        self.mats = {}           # (x,y,z) -> nombre de material liso
        self.fine = []           # [x0,y0,z0,x1,y1,z1,r,g,b,pat,glow]
        self.placed = []         # [cat,x,y,z,rot,solid]
        self.finales = []        # funciones que se llaman antes de escribir (vigas, revision de criterio...)

    def inside(self, x, y, z):
        return 0 <= x < self.W and 0 <= y < self.H and 0 <= z < self.D

    # ---- bloques reales ----
    def put(self, x, y, z, b):
        if not self.inside(x, y, z):
            return
        self.mats.pop((x, y, z), None)
        if b == 0:
            self.cubes.pop((x, y, z), None)
        else:
            self.cubes[(x, y, z)] = b

    def box(self, x0, y0, z0, x1, y1, z1, b):          # incluye ambos extremos
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    self.put(x, y, z, b)

    # ---- material liso ----
    def mat(self, x, y, z, m):
        if not self.inside(x, y, z):
            return
        self.cubes.pop((x, y, z), None)
        self.mats[(x, y, z)] = m

    def mbox(self, x0, y0, z0, x1, y1, z1, m):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    self.mat(x, y, z, m)

    def clear(self, x0, y0, z0, x1=None, y1=None, z1=None):
        if x1 is None:
            x1, y1, z1 = x0, y0, z0
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    self.cubes.pop((x, y, z), None)
                    self.mats.pop((x, y, z), None)

    def solid(self, x, y, z):
        if (x, y, z) in self.mats:
            return True
        b = self.cubes.get((x, y, z), 0)
        return b != 0 and b != COL_INV

    # ---- cajas finas ----
    def f(self, x0, y0, z0, x1, y1, z1, rgb, pat=0, glow=0):
        a = (min(x0, x1), min(y0, y1), min(z0, z1), max(x0, x1), max(y0, y1), max(z0, z1))
        if a[3] - a[0] < 1e-4 or a[4] - a[1] < 1e-4 or a[5] - a[2] < 1e-4:
            return
        self.fine.append([round(v, 4) for v in a] + [int(max(0, min(255, rgb[0]))), int(max(0, min(255, rgb[1]))), int(max(0, min(255, rgb[2]))), pat, glow])

    # caja fina en el marco de una cara de muro.
    # cara: dict con O (x, z) en la superficie EXTERIOR, U (dx, dz) a lo largo del muro, N (dx, dz) hacia afuera.
    # u a lo largo, v = y absoluto, w hacia afuera (0 = cara exterior del muro, -1 = cara interior).
    def fc(self, cara, u0, v0, w0, u1, v1, w1, rgb, pat=0, glow=0):
        (ox, oz), (ux, uz), (nx, nz) = cara["O"], cara["U"], cara["N"]
        xa, za = ox + ux * u0 + nx * w0, oz + uz * u0 + nz * w0
        xb, zb = ox + ux * u1 + nx * w1, oz + uz * u1 + nz * w1
        self.f(xa, v0, za, xb, v1, zb, rgb, pat, glow)

    # ---- objetos del catalogo (101-163, 1001+) ----
    def obj(self, cat, x, y, z, rot=0, solid=0):
        self.placed.append([cat, x, y, z, rot, solid])

    # ---- piel de los materiales lisos ----
    def piel(self):
        n = 0
        for (x, y, z), m in self.mats.items():
            vis = False
            for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                q = (x + dx, y + dy, z + dz)
                if y + dy < 0:
                    continue          # el suelo plano tapa la cara de abajo
                if not self.solid(*q):
                    vis = True
                    break
            if not vis:
                continue
            rgb, j, pat = MATS[m]
            k = _h(x, y, z) % 1000 / 1000.0
            d = (k * 2 - 1) * j
            if _h(x, y, z, 7) % 9 == 0:
                d -= j * 0.8          # algunos bloques un poco mas oscuros (como en Cube World)
            self.f(x, y, z, x + 1, y + 1, z + 1, (rgb[0] + d, rgb[1] + d, rgb[2] + d * 0.9), pat)
            n += 1
        return n

    # ---- salida ----
    def escribir(self, ruta, taller="0.1.6"):
        for fn in self.finales:
            fn()
        self.finales = []
        self.piel()
        allc = dict(self.cubes)
        for p in self.mats:
            allc[p] = SHELL
        cubes = [[x, y + 200, z, b] for (x, y, z), b in sorted(allc.items(), key=lambda kv: (kv[0][1], kv[0][2], kv[0][0]))]
        fine = [[i + 1, a[0], a[1] + 200, a[2], a[3], a[4] + 200, a[5]] + a[6:] for i, a in enumerate(self.fine)]
        placed = [[i + 1, p[0], float(p[1]), float(p[2] + 200), float(p[3]), p[4], 0, 0, p[5]] for i, p in enumerate(self.placed)]
        d = {
            "format": "farlands-taller", "version": 1, "taller": taller,
            "name": self.nombre, "kind": "estructura", "description": self.desc,
            "size": [self.W, self.H, self.D], "origin": [0, 200, 0],
            "bbox_min": [0, 200, 0], "bbox_max": [self.W - 1, 200 + self.H - 1, self.D - 1],
            "coords": "Bloques de 0,5 m. x,y,z absolutos de este archivo. Posicion local = (x, y-200, z). El marco ocupa x 0..%d, z 0..%d, y 200..%d. y=200 es el primer bloque sobre el suelo plano." % (self.W - 1, self.D - 1, 200 + self.H - 1),
            "entry": {"x": self.entry[0], "z": self.entry[1], "facing": self.entry[2]},
            "stamps": [],
            "counts": {"cubes": len(cubes), "fine": len(fine), "placed": len(placed), "dropped_outside_frame": 0},
            "edits": {"format": "farlands-edits", "version": 1, "game": "taller-" + taller, "seed": 7777,
                      "cubes": cubes, "fine": fine, "erase": [], "placed": placed, "pieces": []},
        }
        with open(ruta, "w", encoding="utf-8") as fh:
            json.dump(d, fh, ensure_ascii=False, separators=(",", ":"))
        return d["counts"]
