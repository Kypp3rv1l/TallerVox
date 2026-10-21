#!/usr/bin/env python3
"""Re-edita las casas del catalogo con las reglas de la Taberna v1 (ver docs/reglas_casas.md).
Uso: reeditar.py ORIGEN.json DESTINO.json [--diag]
Trabaja en coordenadas locales (x, y-200, z). Cada casa es un anillo de muros de 1 bloque."""
import json, sys, os, collections, math
HERE = os.path.dirname(os.path.abspath(__file__))
PL = json.load(open(os.path.join(HERE, 'plantillas.json')))

WALL_OPEN = (0, 89)
WIN_W = 6          # hueco de 6 de ancho
WIN_H = 6          # y 6 de alto
SILL = 2           # el alfeizar queda 2 bloques sobre el suelo transitable (1 m)
CHIM_ID = 53       # adoquin


class Casa:
    def __init__(self, d):
        self.d = d
        e = d['edits']
        self.G = {(x, y - 200, z): b for x, y, z, b in e['cubes']}
        self.fines = [list(f) for f in e['fine']]
        self.placed = e['placed']
        self.next_id = int(max([f[0] for f in self.fines] + [0])) + 1
        self.log = []

    # ---------------------------------------------------------------- geometria
    def geom(self, ring_y=10):
        G = self.G
        ring = [(x, z) for (x, y, z), b in G.items() if y == ring_y and b not in (0, CHIM_ID)]
        xs = [a for a, b in ring]; zs = [b for a, b in ring]
        self.x0, self.x1, self.z0, self.z1 = min(xs), max(xs), min(zs), max(zs)
        A = (self.x1 - self.x0 + 1) * (self.z1 - self.z0 + 1)
        per = 2 * ((self.x1 - self.x0 + 1) + (self.z1 - self.z0 + 1)) - 4
        cnt = collections.Counter()
        over = collections.Counter()
        for (x, y, z), b in G.items():
            if b == 0:
                continue
            if self.x0 <= x <= self.x1 and self.z0 <= z <= self.z1:
                cnt[y] += 1
            elif b != CHIM_ID:
                over[y] += 1
        self.cnt = cnt; self.A = A; self.per = per
        roof = None
        for y in range(12, 80):
            if over[y] >= 20:
                roof = y; break
        self.roof = roof
        # losas (grupos consecutivos con >= 50% del area)
        ys = [y for y in range(0, (roof or 40)) if cnt[y] >= 0.5 * A]
        grp = []
        for y in ys:
            if grp and y == grp[-1][-1] + 1:
                grp[-1].append(y)
            else:
                grp.append([y])
        slabs = [g[-1] for g in grp]
        # una losa es un suelo si encima hay muros (>= 60% del perimetro) 3 bloques mas arriba
        floors = []
        for s in slabs:
            if sum(1 for k in range(s + 3, s + 6) if cnt[k] >= 0.6 * per) >= 2 or s == slabs[0]:
                floors.append(s)
        tops = []
        for i, s in enumerate(floors):
            if i + 1 < len(floors):
                t = floors[i + 1] - 1
                # losa de 2 de grosor: t es la primera celda de la losa de arriba
                t = min(g[0] for g in grp if g[-1] == floors[i + 1])
            else:
                t = roof if roof else (max(y for y in cnt if cnt[y] >= 0.5 * per) + 1)
                # techo plano: la losa de arriba
                for g in grp:
                    if g[-1] > s and g[-1] not in floors:
                        t = g[0]; break
            tops.append(t)
        self.storeys = [(s + 1, t) for s, t in zip(floors, tops)]   # (suelo transitable, techo/losa de arriba)
        return self

    # ---------------------------------------------------------------- caras
    def faces(self):
        # nombre: (eje de la longitud, celda fija, recorrido, plano exterior, dir exterior)
        return {
            'N': ('x', self.z0, (self.x0, self.x1), self.z0, -1),
            'S': ('x', self.z1, (self.x0, self.x1), self.z1 + 1, +1),
            'W': ('z', self.x0, (self.z0, self.z1), self.x0, -1),
            'E': ('z', self.x1, (self.z0, self.z1), self.x1 + 1, +1),
        }

    def cell(self, face, u, y):
        ax, fix, rng, P, dr = self.faces()[face]
        return (u, y, fix) if ax == 'x' else (fix, y, u)

    def fine_uw(self, face, f):
        """caja fina -> (u0,u1,y0,y1,w0,w1) con w = distancia hacia fuera desde el plano exterior"""
        ax, fix, rng, P, dr = self.faces()[face]
        if ax == 'x':
            u0, u1 = f[1], f[4]; a0, a1 = f[3], f[6]
        else:
            u0, u1 = f[3], f[6]; a0, a1 = f[1], f[4]
        if dr > 0:
            w0, w1 = a0 - P, a1 - P
        else:
            w0, w1 = P - a1, P - a0
        return u0, u1, f[2] - 200, f[5] - 200, w0, w1

    def mk_fine(self, face, uc, yb, t, extra_dw=0.0):
        """crea una caja fina desde una plantilla (u rel. al centro uc, y rel. a yb, w hacia fuera)"""
        ax, fix, rng, P, dr = self.faces()[face]
        u0, u1, y0, y1, w0, w1, r, g, b, pat, glow = t
        U0, U1 = uc + u0, uc + u1
        if dr > 0:
            A0, A1 = P + w0, P + w1
        else:
            A0, A1 = P - w1, P - w0
        if ax == 'x':
            box = [self.next_id, U0, 200 + yb + y0, A0, U1, 200 + yb + y1, A1, r, g, b, pat, glow]
        else:
            box = [self.next_id, A0, 200 + yb + y0, U0, A1, 200 + yb + y1, U1, r, g, b, pat, glow]
        self.next_id += 1
        return [round(v, 4) if isinstance(v, float) else v for v in box]

    # ---------------------------------------------------------------- aperturas actuales
    def wall_id(self, s, t):
        c = collections.Counter()
        for face, (ax, fix, rng, P, dr) in self.faces().items():
            for u in range(rng[0], rng[1] + 1):
                for y in range(s, t):
                    b = self.G.get(self.cell(face, u, y), 0)
                    if b not in WALL_OPEN and b != CHIM_ID:
                        c[b] += 1
        return c.most_common(1)[0][0] if c else 95

    def openings(self, face, s, t):
        """componentes conectados de celdas abiertas (0/89/ausente) en la cara, entre s y t-1"""
        ax, fix, rng, P, dr = self.faces()[face]
        cells = set()
        for u in range(rng[0] + 1, rng[1]):          # sin las esquinas
            for y in range(s, t):
                if self.G.get(self.cell(face, u, y), 0) in WALL_OPEN:
                    cells.add((u, y))
        out = []
        while cells:
            c0 = cells.pop(); st = [c0]; comp = [c0]
            while st:
                a, b = st.pop()
                for n in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                    if n in cells:
                        cells.remove(n); st.append(n); comp.append(n)
            us = [a for a, _ in comp]; ys = [b for _, b in comp]
            out.append((min(us), max(us), min(ys), max(ys), len(comp)))
        return out

    # ---------------------------------------------------------------- chimenea
    def find_chimney(self):
        pts = [(x, y, z) for (x, y, z), b in self.G.items() if b == CHIM_ID and y == 10]
        if len(pts) < 4:
            return None
        xs = [p[0] for p in pts]; zs = [p[2] for p in pts]
        if min(zs) > self.z1:
            face = 'S'; us = xs
        elif max(zs) < self.z0:
            face = 'N'; us = xs
        elif min(xs) > self.x1:
            face = 'E'; us = zs
        elif max(xs) < self.x0:
            face = 'W'; us = zs
        else:
            return None
        u0 = min(us)
        ys = [y for (x, y, z), b in self.G.items() if b == CHIM_ID and (min(xs) <= x <= max(xs)) and (min(zs) <= z <= max(zs))]
        return dict(face=face, u0=u0, u1=max(us), ytop=max(ys))

    # ---------------------------------------------------------------- ventanas
    def plan_windows(self, s, t, face, skip):
        ax, fix, rng, P, dr = self.faces()[face]
        L = rng[1] - rng[0] + 1
        if t - s < SILL + WIN_H + 2:
            return []
        if L < 20:
            return []
        if L < 44:
            cs = [rng[0] + L // 2 + (0 if L % 2 == 0 else 0)]
            # centro en frontera entera: L par -> centro entero; L impar -> media celda, se redondea
            cs = [int(round(rng[0] + L / 2.0 + 0.001))]
        elif L < 64:
            c1 = int(round(rng[0] + 0.27 * L)); cs = [c1, rng[0] + L - (c1 - rng[0])]
        else:
            c1 = int(round(rng[0] + 0.18 * L)); cs = [c1, int(round(rng[0] + L / 2.0)), rng[0] + L - (c1 - rng[0])]
        out = []
        for c in cs:
            lo, hi = c - 6, c + 6           # ventana + postigos
            if lo < rng[0] + 1 or hi > rng[1] + 1:
                continue
            if any(not (hi <= a - 1 or lo >= b + 2) for a, b in skip):
                continue
            out.append(c)
        return out


def hogar_boxes(x, y, z):
    """Hogar con fuego (prefab 130 del catalogo, 2x2x1) con la esquina minima en (x,y,z) absolutos"""
    out = []
    STN = (128, 124, 118)
    for k in range(8):
        a = k * 0.785
        px = 1.0 + math.cos(a) * 0.85; pz = 1.0 + math.sin(a) * 0.85
        out.append((px - 0.2, 0, pz - 0.2, px + 0.2, 0.25, pz + 0.2, STN, 1, 0))
    out.append((0.35, 0, 0.35, 1.65, 0.06, 1.65, (60, 54, 50), 0, 0))
    out.append((0.65, 0.06, 0.65, 1.35, 0.16, 1.35, (200, 60, 20), 0, 1))
    out.append((0.82, 0.16, 0.82, 1.18, 0.5, 1.18, (255, 150, 40), 0, 1))
    out.append((0.9, 0.5, 0.9, 1.1, 0.75, 1.1, (255, 220, 90), 0, 1))
    return [(x + a, y + b, z + c_, x + d_, y + e_, z + f_, col, pat, gl) for a, b, c_, d_, e_, f_, col, pat, gl in out]


def rebuild_chimney(c, chim):
    """Chimenea de la Taberna: caja hueca de adoquin pegada al hastial, 3 de fondo x 6 de ancho, con la boca abierta
    (4 de ancho) hasta arriba; el hogar queda dentro."""
    face = chim['face']; u0 = chim['u0']; ytop = chim['ytop']
    ax, fix, rng, P, dr = c.faces()[face]
    s = c.storeys[0][0]
    U = list(range(u0, u0 + 6))
    mid = U[1:5]
    def cell(u, k, y):
        a = fix + dr * k
        return (u, y, a) if ax == 'x' else (a, y, u)
    for y in range(0, ytop + 1):
        for u in U:
            for k in range(1, 4):
                cc = cell(u, k, y)
                if y < s or k == 3 or u in (U[0], U[-1]):
                    c.G[cc] = CHIM_ID
                else:
                    c.G.pop(cc, None)
        for u in mid:
            if y >= s:
                c.G[cell(u, 0, y)] = 0
    # cajas finas viejas del hogar / remate
    keep = []
    for f in c.fines:
        a0, a1, b0, b1, w0, w1 = c.fine_uw(face, f)
        en_u = a1 > u0 - 1.2 and a0 < u0 + 7.2
        dentro = w1 <= 0.3 and w0 > -3.6 and b0 >= s - 1 and b0 < s + 8
        remate = en_u and w1 > -1.5 and w0 < 5 and b1 > ytop - 3
        if en_u and (dentro or remate):
            continue
        keep.append(f)
    c.fines = keep
    # hogar con fuego en el centro de la boca
    uc = u0 + 3
    if ax == 'z':
        pass
    if dr > 0:
        A0 = P
    else:
        A0 = P - 2
    for (x0_, y0_, z0_, x1_, y1_, z1_, col, pat, gl) in hogar_boxes(0, 200 + s, 0):
        # (x ancho, z fondo) -> (u, a); el prefab es simetrico: u -> x0_, a -> z0_
        if ax == 'x':
            box = [c.next_id, uc - 1 + x0_, y0_, A0 + z0_, uc - 1 + x1_, y1_, A0 + z1_, col[0], col[1], col[2], pat, gl]
        else:
            box = [c.next_id, A0 + z0_, y0_, uc - 1 + x0_, A0 + z1_, y1_, uc - 1 + x1_, col[0], col[1], col[2], pat, gl]
        c.next_id += 1
        c.fines.append([round(v, 4) if isinstance(v, float) else v for v in box])


# ------------------------------------------------------------------------------------------------ muebles
import muebles as M


def tipo_de(nombre):
    n = nombre.lower()
    if n.startswith(('posada', 'salon', 'edificio')):
        return 'taberna'
    if n.startswith('tienda'):
        return 'tienda'
    if n.startswith('fragua'):
        return 'fragua'
    return 'casa'


class Ocupacion:
    def __init__(self, c, s, t):
        self.c = c; self.s = s; self.t = t
        self.xa, self.xb, self.za, self.zb = c.x0 + 1, c.x1 - 1, c.z0 + 1, c.z1 - 1
        self.occ = set()
        for f in c.fines:
            if f[2] - 200 < s + 4 and f[5] - 200 > s + 0.1:
                for x in range(int(math.floor(f[1] + 0.001)), int(math.ceil(f[4] - 0.001))):
                    for z in range(int(math.floor(f[3] + 0.001)), int(math.ceil(f[6] - 0.001))):
                        self.occ.add((x, z))
        for (x, y, z), b in c.G.items():
            if s <= y < s + 4 and b != 0 and self.xa <= x <= self.xb and self.za <= z <= self.zb:
                self.occ.add((x, z))

    def reservar(self, x0, x1, z0, z1):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                self.occ.add((x, z))

    def libre(self, x, z, w, d, m=0):
        if x - m < self.xa or z - m < self.za or x + w - 1 + m > self.xb or z + d - 1 + m > self.zb:
            return False
        for a in range(x - m, x + w + m):
            for b in range(z - m, z + d + m):
                if (a, b) in self.occ:
                    return False
        return True

    def poner(self, pieza, x, z, rot=0, m=0):
        boxes, w, d = pieza
        boxes, w, d = M.rotar(boxes, w, d, rot)
        if not self.libre(x, z, w, d, m):
            return False
        for a in range(x, x + w):
            for b in range(z, z + d):
                self.occ.add((a, b))
        for (x0, y0, z0, x1, y1, z1, col, pat, gl) in boxes:
            box = [self.c.next_id, x + x0, 200 + self.s + y0, z + z0, x + x1, 200 + self.s + y1, z + z1, col[0], col[1], col[2], pat, gl]
            self.c.next_id += 1
            self.c.fines.append([round(v, 4) if isinstance(v, float) else v for v in box])
        return True


def amueblar(c, nombre, puertas, chim):
    tipo = tipo_de(nombre)
    s, t = c.storeys[0]
    o = Ocupacion(c, s, t)
    msgs = []
    # zonas reservadas: delante de las puertas y de la chimenea
    for (face, u0, u1) in puertas:
        ax, fix, rng, P, dr = c.faces()[face]
        a = [fix - dr * k for k in range(1, 7)]
        for k in a:
            for u in range(u0 - 2, u1 + 3):
                o.occ.add((u, k) if ax == 'x' else (k, u))
    if chim:
        face = chim['face']; ax, fix, rng, P, dr = c.faces()[face]
        for k in range(1, 6):
            for u in range(chim['u0'] - 2, chim['u0'] + 8):
                a = fix - dr * k
                o.occ.add((u, a) if ax == 'x' else (a, u))
    W = c.x1 - c.x0 - 1; D = c.z1 - c.z0 - 1
    n_mesas = 0
    # --- mostrador / barra (taberna y tienda)
    if tipo in ('taberna', 'tienda') and W >= 20 and D >= 14:
        larga = 'x' if W >= D else 'z'
        puertas_caras = set(f for f, _, _ in puertas)
        cand = ['S', 'N'] if larga == 'x' else ['W', 'E']
        cara = None
        for f in cand:
            if f not in puertas_caras and not (chim and chim['face'] == f):
                cara = f; break
        if cara:
            ax, fix, rng, P, dr = c.faces()[cara]
            L = rng[1] - rng[0] - 1
            largo = max(8, min(21, int(L * 0.35)))
            inner = fix - dr                       # celda interior pegada al muro
            f_cl = inner - dr * 5                  # fila delantera del mostrador (lado cliente)
            f_tr = inner - dr * 6 if False else f_cl - dr * 1
            # el mostrador ocupa dos filas: f_cl y f_cl - dr (hacia el muro)
            rows = sorted([f_cl, f_cl + dr])
            # extremo pegado al muro lateral opuesto a la chimenea
            u_fin = rng[1] - 1
            u_ini = u_fin - largo + 1
            ok = True
            cells = []
            for u in range(u_ini, u_fin + 1):
                for r in rows:
                    cells.append((u, r) if ax == 'x' else (r, u))
            if all(o.libre(a, b, 1, 1) for a, b in cells):
                for a, b in cells:
                    c.G[(a, s, b)] = 76; c.G[(a, s + 1, b)] = 76
                    o.occ.add((a, b))
                # tapa oscura (vuelo 0,2 hacia el cliente)
                lado_cliente = -dr
                if ax == 'x':
                    z_lo = min(rows) - (0.2 if lado_cliente < 0 else 0); z_hi = max(rows) + 1 + (0.2 if lado_cliente > 0 else 0)
                    box = [c.next_id, u_ini, 200 + s + 2.0, z_lo, u_fin + 1, 200 + s + 2.2, z_hi, 45, 30, 24, 0, 0]
                else:
                    x_lo = min(rows) - (0.2 if lado_cliente < 0 else 0); x_hi = max(rows) + 1 + (0.2 if lado_cliente > 0 else 0)
                    box = [c.next_id, x_lo, 200 + s + 2.0, u_ini, x_hi, 200 + s + 2.2, u_fin + 1, 45, 30, 24, 0, 0]
                c.next_id += 1
                c.fines.append(box)
                # estanterias detras
                rot = {'S': 0, 'N': 2, 'W': 1, 'E': 3}[cara]
                u = u_ini
                while u + 2 <= u_fin:
                    pos = (u, inner) if ax == 'x' else (inner, u)
                    # la estanteria mira hacia el interior: ajustar la fila segun la cara
                    if cara == 'N': pos = (u, inner)
                    if cara in ('W', 'E'):
                        pos = (inner, u)
                    o.occ.discard(pos)
                    if o.poner(M.estanteria(), pos[0], pos[1], rot):
                        pass
                    u += 4
                msgs.append(f"mostrador {largo} en cara {cara}")
                # reserva del pasillo del tendero y del cliente
                for u in range(u_ini - 1, u_fin + 2):
                    for k in range(1, 4):
                        a = f_cl - dr * 0 + (-dr) * k
                        o.occ.add((u, a) if ax == 'x' else (a, u))
    # --- mesas redondas
    area = max(0, (W * D) - len(o.occ))
    if tipo == 'taberna':
        n_mesas = max(2, min(8, area // 90))
    elif tipo == 'casa':
        n_mesas = 1 if area > 250 else 0
    elif tipo == 'tienda':
        n_mesas = 0
    elif tipo == 'fragua':
        n_mesas = 0
    colocadas = 0
    paso = 8
    for z in range(o.za + 2, o.zb - 3, paso):
        for x in range(o.xa + 2, o.xb - 3, paso):
            if colocadas >= n_mesas:
                break
            if o.libre(x, z, 3, 3, 2):
                if o.poner(M.mesa_redonda(), x, z, 0, 0):
                    colocadas += 1
                    # dos taburetes enfrentados
                    o.poner(M.taburete(), x - 2, z + 1, 0, 0)
                    o.poner(M.taburete(), x + 4, z + 1, 0, 0)
    if colocadas:
        msgs.append(f"{colocadas} mesas redondas")
    return msgs


def procesar(d, nombre, diag=False):
    c = Casa(d).geom()
    rep = [f"{nombre}: anillo x{c.x0}..{c.x1} z{c.z0}..{c.z1} techo={c.roof} pisos={c.storeys}"]
    chim = c.find_chimney()
    if chim:
        rep.append(f"  chimenea {chim}")
    new_fines = []
    removed = 0
    n_win = 0
    kept_doors = {}
    puertas_pl = []
    for face in 'NSWE':
        ax, fix, rng, P, dr = c.faces()[face]
        for (s, t) in c.storeys:
            wid = c.wall_id(s, t)
            ops = c.openings(face, s, t)
            skip = []
            for (u0, u1, y0, y1, n) in ops:
                es_puerta = (y0 <= s + 1)
                if es_puerta:
                    skip.append((u0, u1))
                    if (s, t) == c.storeys[0]:
                        puertas_pl.append((face, u0, u1))
                    continue
                # ventana vieja: rellenar con muro y borrar sus cajas finas
                for u in range(u0, u1 + 1):
                    for y in range(y0, y1 + 1):
                        if c.G.get(c.cell(face, u, y), 0) in WALL_OPEN:
                            c.G[c.cell(face, u, y)] = wid
                keep = []
                for f in c.fines:
                    a0, a1, b0, b1, w0, w1 = c.fine_uw(face, f)
                    if a1 > u0 - 3.2 and a0 < u1 + 4.2 and b1 > y0 - 2.5 and b0 < y1 + 2.5 and w1 > -2.2 and w0 < 2.5:
                        removed += 1
                    else:
                        keep.append(f)
                c.fines = keep
            if chim and chim['face'] == face and s == c.storeys[0][0]:
                skip.append((chim['u0'], chim['u1']))
            if chim and chim['face'] == face:
                skip.append((chim['u0'], chim['u1']))
            kept_doors[(face, s)] = skip
    # ---- ventanas nuevas (despues de limpiar todo)
    for face in 'NSWE':
        ax, fix, rng, P, dr = c.faces()[face]
        for (s, t) in c.storeys:
            skip = kept_doors[(face, s)]
            for uc in c.plan_windows(s, t, face, skip):
                yb = s + SILL
                for u in range(uc - 3, uc + 3):
                    for y in range(yb, yb + WIN_H):
                        c.G[c.cell(face, u, y)] = 89
                for tpl in PL['ventana']:
                    c.fines.append(c.mk_fine(face, float(uc), yb, tpl))
                n_win += 1
    if chim:
        rebuild_chimney(c, chim)
    msgs = amueblar(c, nombre, puertas_pl, chim)
    rep.append('  muebles: ' + ', '.join(msgs))
    rep.append(f"  ventanas nuevas: {n_win}; cajas finas viejas quitadas: {removed}")
    return c, rep


def escribir(c, d, destino):
    e = d['edits']
    cubes = sorted([[x, y + 200, z, b] for (x, y, z), b in c.G.items()])
    e['cubes'] = cubes
    e['fine'] = c.fines
    d['counts'] = {'cubes': len(cubes), 'fine': len(c.fines), 'placed': len(e['placed']), 'dropped_outside_frame': 0}
    json.dump(d, open(destino, 'w'), ensure_ascii=False, separators=(',', ':'))


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    d = json.load(open(src))
    c, rep = procesar(d, os.path.basename(src))
    print('\n'.join(rep))
    escribir(c, d, dst)
