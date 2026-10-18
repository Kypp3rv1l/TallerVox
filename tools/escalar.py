#!/usr/bin/env python3
"""Estira una estructura del Taller x2 (interior, techo y muebles), dejando los muros con su grosor de 1 bloque.
Uso: escalar.py origen.json destino.json [kx [kz [ky]]]   (por defecto 2 2 2; casas del catalogo: 3 3 2)
Cada rebanada de bloques (por eje X, Z, Y) se duplica salvo las que son muros o suelos (las mas densas) y los bordes."""
import json, sys, statistics, math

def classify(counts, edge_thin, ratio, k=2):
    n = len(counts)
    inner = [c for i, c in enumerate(counts) if c > 0 and not (edge_thin and i in (0, n - 1))]
    med = statistics.median(inner) if inner else 1
    w = []
    for i, c in enumerate(counts):
        thin = c == 0 or (edge_thin and i in (0, n - 1)) or c > ratio * med
        w.append(1 if thin else k)
    return w

def build_map(w):
    N = [0]
    for x in w:
        N.append(N[-1] + x)
    def f(u):
        n = len(w)
        if u <= 0:
            return N[0] + u * 1.0
        if u >= n:
            return N[n] + (u - n)
        c = int(math.floor(u + 1e-9))
        if c >= n:
            c = n - 1
        return N[c] + (u - c) * w[c]
    return N, f

def stretch(src, dst, kx=2, kz=2, ky=2):
    d = json.load(open(src, encoding='utf-8'))
    W, H, D = d['size']
    oy = d['origin'][1]
    e = d['edits']
    # quitar las capas de abajo casi vacias (pilotes, aire bajo la casa): la casa debe apoyarse en el suelo
    cy0 = [0] * H
    for c in e['cubes']:
        if int(c[3]) != 0:
            cy0[int(c[1]) - oy] += 1
    mxc = max(cy0)
    trim = 0
    while trim < H - 1 and cy0[trim] < 0.6 * mxc:
        trim += 1
    if trim:
        e = dict(e)
        e['cubes'] = [[c[0], int(c[1]) - trim, c[2], c[3]] for c in e['cubes'] if int(c[1]) - oy >= trim]
        fn = []
        for f in e['fine']:
            if f[5] - oy <= trim + 0.01:
                continue
            g = list(f); g[2] = max(oy, f[2] - trim); g[5] = f[5] - trim
            fn.append(g)
        e['fine'] = fn
        e['placed'] = [[*p[:3], p[3] - trim, *p[4:]] for p in e['placed'] if p[3] - oy >= trim]
        H -= trim
    pts = [(int(c[0]), int(c[1]) - oy, int(c[2])) for c in e['cubes'] if int(c[3]) != 0]
    cx = [0] * W; cy = [0] * H; cz = [0] * D
    for x, y, z in pts:
        cx[x] += 1; cy[y] += 1; cz[z] += 1
    wx = classify(cx, True, 1.3, kx); wz = classify(cz, True, 1.3, kz); wy = classify(cy, False, 1.45, ky)
    Nx, fx = build_map(wx); Ny, fy = build_map(wy); Nz, fz = build_map(wz)
    cubes = []
    for c in e['cubes']:
        x, y, z, b = int(c[0]), int(c[1]) - oy, int(c[2]), int(c[3])
        for i in range(wx[x]):
            for j in range(wy[y]):
                for k in range(wz[z]):
                    cubes.append([Nx[x] + i, Ny[y] + j + oy, Nz[z] + k, b])
    fine = []
    for f in e['fine']:
        fine.append([f[0], round(fx(f[1]), 4), round(fy(f[2] - oy) + oy, 4), round(fz(f[3]), 4), round(fx(f[4]), 4), round(fy(f[5] - oy) + oy, 4), round(fz(f[6]), 4)] + f[7:])
    placed = []
    for p in e['placed']:
        q = list(p)
        q[2] = float(math.floor(fx(p[2]) + 1e-6)); q[3] = float(math.floor(fy(p[3] - oy) + 1e-6) + oy); q[4] = float(math.floor(fz(p[4]) + 1e-6))
        placed.append(q)
    e2 = dict(e); e2['cubes'] = cubes; e2['fine'] = fine; e2['placed'] = placed
    nW, nH, nD = Nx[-1], Ny[-1], Nz[-1]
    d['size'] = [nW, nH, nD]
    d['bbox_max'] = [d['bbox_min'][0] + nW - 1, d['bbox_min'][1] + nH - 1, d['bbox_min'][2] + nD - 1] if 'bbox_min' in d else d.get('bbox_max')
    ent = d['entry']
    ent = dict(ent); ent['x'] = Nx[ent['x']] + wx[ent['x']] // 2 if ent['x'] < W else ent['x']; ent['z'] = Nz[ent['z']] if ent['z'] < D else ent['z']
    d['entry'] = ent
    d['counts'] = {'cubes': len(cubes), 'fine': len(fine), 'placed': len(placed), 'dropped_outside_frame': 0}
    d['edits'] = e2
    d['description'] = (d.get('description', '') + ' (ensanchada: interior x%d en X/Z y x%d en altura; muros de 1 bloque)' % (kx, ky) + '').strip()
    json.dump(d, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    return (W, H + 0, D), (nW, nH, nD), (wx, wy, wz)

if __name__ == '__main__':
    kx = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    kz = int(sys.argv[4]) if len(sys.argv) > 4 else kx
    ky = int(sys.argv[5]) if len(sys.argv) > 5 else 2
    a, b, w = stretch(sys.argv[1], sys.argv[2], kx, kz, ky)
    print(sys.argv[1], a, '->', b)
