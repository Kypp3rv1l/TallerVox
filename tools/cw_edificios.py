# Farlands Taller v0.1.7 - estructuras nuevas estilo Cube World (pueblo y progreso).
# Las genera tools/cw_propuestas.py junto con las demas. Todas pasan por la revision de criterio de Casa
# (paso de puertas/escaleras libre, nada inflamable junto al fuego, nada tapando ventanas, objetos que no chocan).
import math
from cw_lib import Obra, WD, WDD, COL_INV, _h
from cw_casas import (Casa, planta, jarron_flores, mesa_redonda, escalera, escalera_perimetral, barra, tablero, farol,
                      baranda, pilar_baranda, HOJA, HOJA2, HIERRO, HIERRO2, PIEDRA_F)
from cw_propuestas import acera, afuera, farola, ROJO, ORO, MORADO, AZUL, CELESTE

VIDRIO = (220, 214, 200)
POCIONES = [(200, 50, 60), (60, 120, 210), (90, 190, 80), (170, 80, 210), (240, 180, 50), (60, 200, 200)]
BRONCE = (184, 134, 62)
PAJA = (222, 196, 112)
PAJA2 = (200, 172, 92)
CUERO = (120, 74, 44)


# ======================================================================== objetos sueltos (voxel chico)
def frasco(o, x, y, z, col, alto=0.35, k=0):
    """Frasco de pocion: cuerpo de vidrio con liquido que brilla un poco, cuello y corcho."""
    r = 0.09 + (k % 2) * 0.02
    o.f(x - r, y, z - r, x + r, y + alto * 0.62, z + r, col, 0, 1 if k % 3 == 0 else 0)
    o.f(x - r - 0.015, y + alto * 0.62, z - r - 0.015, x + r + 0.015, y + alto * 0.7, z + r + 0.015, VIDRIO)
    o.f(x - 0.035, y + alto * 0.7, z - 0.035, x + 0.035, y + alto * 0.9, z + 0.035, VIDRIO)
    o.f(x - 0.045, y + alto * 0.9, z - 0.045, x + 0.045, y + alto, z + 0.045, (150, 104, 60))


def estante_pociones(o, c, x0, z, y, largo, frente="n", nombre="estante de pociones"):
    """Estante de pared (fondo 0,5) de 3 tablas con frascos de colores. 'frente' = hacia donde mira."""
    zb = z  # el estante va de z a z+0.5 (frente 'n' => pegado a un muro en +Z)
    c.ocupa(nombre, x0, zb, x0 + largo, zb + 0.5, y, y + 3.0, True)
    o.f(x0, y, zb + 0.44, x0 + largo, y + 3.0, zb + 0.5, WDD, 2)
    o.f(x0, y, zb, x0 + 0.1, y + 3.0, zb + 0.5, WDD, 2)
    o.f(x0 + largo - 0.1, y, zb, x0 + largo, y + 3.0, zb + 0.5, WDD, 2)
    for i, yy in enumerate((0.0, 0.9, 1.8, 2.7)):
        o.f(x0, y + yy, zb, x0 + largo, y + yy + 0.1, zb + 0.5, WD, 2)
        if yy < 2.7:
            n = int((largo - 0.3) / 0.32)
            for j in range(n):
                k = _h(x0, z, i, j)
                if k % 5 == 0:
                    continue
                frasco(o, x0 + 0.25 + j * 0.32, y + yy + 0.1, zb + 0.25, POCIONES[k % len(POCIONES)], 0.3 + (k % 3) * 0.08, k)


def hierbas_colgadas(o, x, y, z, n=3):
    """Ramilletes de hierbas secas colgando de una viga (y = abajo de la viga)."""
    cols = [(110, 150, 70), (150, 140, 70), (120, 90, 140), (90, 130, 80)]
    for i in range(n):           # a lo largo de la viga (eje z)
        zz = z + i * 0.45
        o.f(x - 0.01, y - 0.35, zz - 0.01, x + 0.01, y, zz + 0.01, (200, 180, 140))
        o.f(x - 0.06, y - 0.45, zz - 0.06, x + 0.06, y - 0.35, zz + 0.06, (190, 60, 50))
        for j in range(3):
            o.f(x - 0.08, y - 0.9 + j * 0.05, zz - 0.12 + j * 0.06, x + 0.08, y - 0.45, zz - 0.06 + j * 0.06, cols[(i + j) % 4])


def caldero_burbujas(o, c, x, y, z, col=(100, 220, 90)):
    c.ocupa("caldero", x, z, x + 1.2, z + 1.2, y, y + 1.2, False)
    cx, cz = x + 0.6, z + 0.6
    o.f(cx - 0.5, y + 0.15, cz - 0.5, cx + 0.5, y + 0.85, cz + 0.5, (44, 44, 50))
    o.f(cx - 0.56, y + 0.75, cz - 0.56, cx + 0.56, y + 0.88, cz + 0.56, (60, 60, 68))
    o.f(cx - 0.42, y + 0.86, cz - 0.42, cx + 0.42, y + 0.9, cz + 0.42, col, 0, 1)
    for (dx, dz, h) in ((-0.15, 0.1, 0.06), (0.18, -0.12, 0.1), (0.05, 0.2, 0.04)):
        o.f(cx + dx - 0.06, y + 0.9, cz + dz - 0.06, cx + dx + 0.06, y + 0.9 + h, cz + dz + 0.06, col, 0, 1)
    for (dx, dz) in ((-0.38, -0.38), (0.28, -0.38), (-0.38, 0.28), (0.28, 0.28)):
        o.f(cx + dx, y, cz + dz, cx + dx + 0.1, y + 0.18, cz + dz + 0.1, HIERRO)
    o.put(int(x), y, int(z), COL_INV)


def alambique(o, x, y, z):
    """Juego de alquimia sobre una mesa (y = tapa de la mesa)."""
    o.f(x + 0.2, y, z + 0.3, x + 0.6, y + 0.08, z + 0.7, HIERRO)
    o.f(x + 0.36, y + 0.08, z + 0.46, x + 0.44, y + 0.3, z + 0.54, HIERRO)
    o.f(x + 0.24, y + 0.3, z + 0.34, x + 0.56, y + 0.62, z + 0.66, VIDRIO)
    o.f(x + 0.27, y + 0.32, z + 0.37, x + 0.53, y + 0.5, z + 0.63, (90, 200, 120), 0, 1)
    o.f(x + 0.36, y + 0.62, z + 0.46, x + 0.44, y + 0.8, z + 0.54, VIDRIO)
    for i in range(5):
        o.f(x + 0.44 + i * 0.12, y + 0.78 - i * 0.07, z + 0.47, x + 0.56 + i * 0.12, y + 0.84 - i * 0.07, z + 0.53, VIDRIO)
    frasco(o, x + 1.2, y, z + 0.5, (90, 200, 120), 0.4, 3)
    frasco(o, x + 1.55, y, z + 0.3, POCIONES[3], 0.32, 1)
    o.f(x + 1.6, y, z + 0.6, x + 1.85, y + 0.12, z + 0.85, (210, 200, 180))      # mortero
    o.f(x + 1.7, y + 0.1, z + 0.68, x + 1.76, y + 0.3, z + 0.74, (160, 150, 130))


def muneco(o, x, y, z, rot=0):
    """Muneco de entrenamiento: poste, cuerpo de paja con cuerdas, brazos de madera, cabeza de saco y diana en el pecho."""
    cx, cz = x + 0.5, z + 0.5
    o.f(cx - 0.32, y, cz - 0.32, cx + 0.32, y + 0.12, cz + 0.32, WDD, 2)
    o.f(cx - 0.07, y + 0.12, cz - 0.07, cx + 0.07, y + 1.0, cz + 0.07, WDD)
    o.f(cx - 0.3, y + 1.0, cz - 0.22, cx + 0.3, y + 1.8, cz + 0.22, PAJA)
    for yy in (1.15, 1.45, 1.7):
        o.f(cx - 0.31, yy + y, cz - 0.23, cx + 0.31, yy + y + 0.05, cz + 0.23, (150, 110, 70))
    if rot % 2 == 0:
        o.f(cx - 0.75, y + 1.55, cz - 0.05, cx + 0.75, y + 1.65, cz + 0.05, WD)
        zf = cz - 0.23 if rot == 0 else cz + 0.23
        sg = -1 if rot == 0 else 1
        o.f(cx - 0.17, y + 1.25, zf + sg * 0.02, cx + 0.17, y + 1.55, zf, (240, 236, 220))
        o.f(cx - 0.1, y + 1.32, zf + sg * 0.035, cx + 0.1, y + 1.48, zf + sg * 0.02, (200, 50, 50))
        o.f(cx - 0.04, y + 1.37, zf + sg * 0.05, cx + 0.04, y + 1.43, zf + sg * 0.035, (240, 236, 220))
    else:
        o.f(cx - 0.05, y + 1.55, cz - 0.75, cx + 0.05, y + 1.65, cz + 0.75, WD)
    o.f(cx - 0.2, y + 1.8, cz - 0.2, cx + 0.2, y + 2.2, cz + 0.2, (196, 168, 120))
    o.f(cx - 0.21, y + 1.85, cz - 0.21, cx + 0.21, y + 1.9, cz + 0.21, (150, 110, 70))
    o.put(x, y, z, COL_INV); o.put(x, y + 1, z, COL_INV)


def armero(o, x0, y, z, largo=3, frente="s"):
    """Estante de armas apoyado en el piso: dos patas, travesanos y espadas/lanzas verticales."""
    zf = z
    o.f(x0, y, zf, x0 + 0.15, y + 1.8, zf + 0.5, WDD, 2)
    o.f(x0 + largo - 0.15, y, zf, x0 + largo, y + 1.8, zf + 0.5, WDD, 2)
    o.f(x0, y + 0.2, zf + 0.1, x0 + largo, y + 0.32, zf + 0.4, WD, 2)
    o.f(x0, y + 1.4, zf + 0.1, x0 + largo, y + 1.52, zf + 0.4, WD, 2)
    t = x0 + 0.45
    i = 0
    while t < x0 + largo - 0.3:
        if i % 3 == 2:   # lanza
            o.f(t - 0.03, y + 0.32, zf + 0.22, t + 0.03, y + 2.3, zf + 0.28, WD)
            o.f(t - 0.06, y + 2.3, zf + 0.2, t + 0.06, y + 2.6, zf + 0.3, (200, 204, 214))
        else:            # espada
            o.f(t - 0.05, y + 0.32, zf + 0.2, t + 0.05, y + 1.55, zf + 0.3, (200, 204, 214))
            o.f(t - 0.15, y + 1.55, zf + 0.18, t + 0.15, y + 1.62, zf + 0.32, BRONCE)
            o.f(t - 0.04, y + 1.62, zf + 0.21, t + 0.04, y + 1.9, zf + 0.29, CUERO)
            o.f(t - 0.06, y + 1.9, zf + 0.19, t + 0.06, y + 1.97, zf + 0.31, BRONCE)
        t += 0.42
        i += 1


def fardo_paja(o, x, y, z, rot=0):
    w, d = (1.3, 0.8) if rot % 2 == 0 else (0.8, 1.3)
    o.f(x, y, z, x + w, y + 0.7, z + d, PAJA)
    if rot % 2 == 0:
        for t in (0.3, 0.95):
            o.f(x + t, y - 0.01, z - 0.01, x + t + 0.05, y + 0.71, z + d + 0.01, (160, 110, 60))
    else:
        for t in (0.3, 0.95):
            o.f(x - 0.01, y - 0.01, z + t, x + w + 0.01, y + 0.71, z + t + 0.05, (160, 110, 60))


def mesa_trabajo(o, c, x0, z0, y, largo=4):
    """Banco de carpintero 4x1: tapa gruesa, patas, tornillo de banco, herramientas y virutas."""
    c.ocupa("banco de carpintero", x0, z0, x0 + largo, z0 + 1, y, y + 1.4)
    o.f(x0, y + 1.0, z0, x0 + largo, y + 1.25, z0 + 1, (150, 104, 62), 2)
    for xx in (x0 + 0.15, x0 + largo - 0.35):
        for zz in (z0 + 0.1, z0 + 0.7):
            o.f(xx, y, zz, xx + 0.2, y + 1.0, zz + 0.2, WDD)
    o.f(x0 + 0.15, y + 0.3, z0 + 0.15, x0 + largo - 0.15, y + 0.4, z0 + 0.85, WDD, 2)
    o.f(x0 - 0.1, y + 0.75, z0 + 0.3, x0 + 0.05, y + 1.25, z0 + 0.7, WD)               # tornillo
    o.f(x0 - 0.18, y + 0.95, z0 + 0.46, x0 - 0.1, y + 1.05, z0 + 0.54, HIERRO)
    o.f(x0 + 1.0, y + 1.25, z0 + 0.3, x0 + 1.5, y + 1.32, z0 + 0.4, (200, 204, 214))  # formon
    o.f(x0 + 1.5, y + 1.25, z0 + 0.32, x0 + 1.75, y + 1.32, z0 + 0.38, CUERO)
    o.f(x0 + 2.2, y + 1.25, z0 + 0.55, x0 + 2.35, y + 1.42, z0 + 0.8, WD)              # cepillo
    o.f(x0 + 2.0, y + 1.25, z0 + 0.5, x0 + 2.8, y + 1.33, z0 + 0.85, (170, 120, 70))
    for i in range(5):
        o.f(x0 + 0.5 + i * 0.6, y + 0.01, z0 + 1.1 + (i % 2) * 0.2, x0 + 0.75 + i * 0.6, y + 0.03, z0 + 1.3 + (i % 2) * 0.2, (226, 200, 150))
    o.box(int(x0), y, int(z0), int(x0 + largo) - 1, y, int(z0), COL_INV)


def caballete_tronco(o, c, x0, z0, y):
    """Dos caballetes con un tronco encima y una sierra apoyada."""
    c.ocupa("caballete con tronco", x0, z0, x0 + 3, z0 + 1, y, y + 1.4)
    for xx in (x0 + 0.3, x0 + 2.4):
        o.f(xx, y + 0.8, z0 + 0.1, xx + 0.3, y + 0.95, z0 + 0.9, WD)
        for zz in (z0 + 0.1, z0 + 0.75):
            o.f(xx + 0.08, y, zz, xx + 0.22, y + 0.8, zz + 0.15, WDD)
    o.f(x0, y + 0.95, z0 + 0.2, x0 + 3, y + 1.45, z0 + 0.8, (112, 76, 44), 5)
    o.f(x0 - 0.02, y + 1.0, z0 + 0.25, x0, y + 1.4, z0 + 0.75, (200, 170, 120))
    o.f(x0 + 1.4, y + 1.0, z0 + 0.15, x0 + 1.47, y + 1.6, z0 + 0.85, (196, 200, 210))
    o.put(int(x0), y, int(z0), COL_INV); o.put(int(x0) + 2, y, int(z0), COL_INV)


def pila_tablas(o, c, x0, z0, y, alto=6):
    c.ocupa("pila de tablas", x0, z0, x0 + 3, z0 + 1, y, y + alto * 0.18 + 0.2)
    for i in range(alto):
        sh = 0.05 if i % 2 else -0.05
        o.f(x0 + sh, y + 0.12 + i * 0.18, z0 + 0.1, x0 + 3 + sh, y + 0.28 + i * 0.18, z0 + 0.9, (176, 126, 76) if i % 2 else (160, 112, 66), 2)
    for xx in (x0 + 0.3, x0 + 2.5):
        o.f(xx, y, z0 + 0.05, xx + 0.2, y + 0.12, z0 + 0.95, WDD)
    o.put(int(x0), y, int(z0), COL_INV)


# ======================================================================== 1. tienda de pociones
def tienda_pociones():
    W, D = 20, 18
    o = Obra("cw_tienda_pociones", W, 24, D,
             "Tienda de pociones (progreso: comprar y mejorar pociones). Mostrador con frascos, estantes de pociones en el fondo, "
             "caldero burbujeante, mesa de alquimia con alambique, hierbas colgando de las vigas. Techo morado, cartel con frasco.",
             entry=(10, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    c = Casa(o, 3, 4, 16, 13, muro="muro_blanco", teja="techo_morado")     # interior x 4..15, z 5..12
    s = c.suelos[0]
    c.puerta("n", 6)                                                       # x 9..10
    c.ventana("n", 2); c.ventana("n", 10)
    c.ventana("o", 3); c.ventana("e", 3)
    c.cartel_colgante("n", 4.7, s + 3, "pocion")
    c.enredadera("n", 13.4, s - 1, s + 5)
    barra(o, 6, 9, 12, 9, s, "n", casa=c, nombre="mostrador")
    for i, xx in enumerate((6.5, 7.4, 10.8, 11.6)):
        frasco(o, xx, s + 1.3, 9.45, POCIONES[i + 1], 0.38, i)
    estante_pociones(o, c, 4.2, 12.5, s, 4.0)
    estante_pociones(o, c, 9.8, 12.5, s, 4.0)
    caldero_burbujas(o, c, 13.8, s, 5.4)
    c.mueble(124, 4, s, 6, 0, "mesa de alquimia")
    alambique(o, 4.05, s + 1.3, 6.1)
    planta(o, 15, s, 9, casa=c)
    for xx, zz in ((6.3, 7.0), (6.3, 10.6), (10.3, 10.6)):
        hierbas_colgadas(o, xx, c.roof_y - 0.45, zz)
    c.farol_pared("e", 6.5, s + 3.5); c.farol_pared("o", 6.5, s + 3.5)
    return o


# ======================================================================== 2. herreria semiabierta
def herreria():
    W, D = 22, 18
    o = Obra("cw_herreria", W, 26, D,
             "Herreria semiabierta (progreso: forjar y mejorar armas). Frente y lado este abiertos con pilares de piedra. "
             "Fragua de piedra con brasas, campana y chimenea, fuelle, yunque, pila de temple con agua, piedra de afilar, "
             "herramientas colgadas y armero. Techo oscuro, cartel con yunque.",
             entry=(10, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    c = Casa(o, 3, 4, 18, 13, teja="techo_oscuro")      # interior x 4..17, z 5..12
    s = c.suelos[0]
    c.abrir("n", 1, 15, 0, cada=5)
    c.abrir("e", 1, 9, 0, cada=4)
    # fragua: cuerpo de piedra 3x2 contra el fondo oeste, brasas encima, campana y chimenea que atraviesa el techo
    o.mbox(4, s, 11, 6, s, 12, "chimenea")
    o.f(3.9, s + 1, 10.9, 7.1, s + 1.25, 13, PIEDRA_F)
    o.f(4.2, s + 1.0, 11.2, 6.8, s + 1.1, 12.6, (255, 110, 30), 0, 1)
    for i in range(7):
        xx, zz = 4.3 + (i % 4) * 0.6, 11.3 + (i // 4) * 0.6
        o.f(xx, s + 1.05, zz, xx + 0.35, s + 1.2, zz + 0.35, (255, 150 + (i % 3) * 30, 50), 0, 1)
    for y in range(s + 3, c.cumbre + 2):
        o.mbox(4, y, 11, 6, y, 12, "chimenea")
    o.mbox(4, s + 3, 10, 6, s + 3, 10, "chimenea")
    o.f(3.8, c.cumbre + 2, 10.8, 7.2, c.cumbre + 2.22, 13.2, PIEDRA_F)
    o.f(4.4, c.cumbre + 2.22, 11.4, 6.6, c.cumbre + 2.26, 12.6, (30, 26, 24))
    c.fuegos.append((5.5, 11.8, s, 2.5))
    c.reservar(4, 8.5, 7, 11, s, s + 2, "paso", "frente de la fragua")
    # fuelle de cuero (junto a la fragua a proposito; no es madera seca)
    c.ocupa("fuelle", 7.1, 11.2, 8.3, 12.6, s, s + 1.3, False)
    o.f(7.2, s, 11.4, 8.2, s + 0.5, 12.4, WDD, 2)
    o.f(7.25, s + 0.5, 11.45, 8.15, s + 0.8, 12.35, CUERO)
    o.f(7.2, s + 0.8, 11.4, 8.2, s + 0.9, 12.4, WD, 2)
    o.f(7.0, s + 0.6, 11.85, 7.2, s + 0.7, 11.95, HIERRO)
    c.mueble(135, 8, s, 8, 0, "yunque")
    c.ocupa("pila de temple", 10, 11.4, 12.6, 12.9, s, s + 0.9, False)
    o.f(10, s, 11.4, 12.6, s + 0.9, 12.9, (110, 106, 100))
    o.f(10.15, s + 0.75, 11.55, 12.45, s + 0.82, 12.75, (60, 110, 160))
    o.box(10, s, 11, 12, s, 12, COL_INV)
    # piedra de afilar
    c.ocupa("piedra de afilar", 14, 11, 15.6, 12.6, s, s + 1.4)
    o.f(14.1, s, 11.2, 14.3, s + 0.9, 12.4, WDD); o.f(15.3, s, 11.2, 15.5, s + 0.9, 12.4, WDD)
    o.f(14.3, s + 0.5, 11.3, 15.3, s + 1.4, 12.3, (150, 146, 140))
    o.f(14.6, s + 0.8, 11.6, 15.0, s + 1.1, 12.0, (110, 106, 100))
    o.f(15.5, s + 0.88, 11.75, 15.85, s + 0.96, 11.85, HIERRO)
    # herramientas en el muro del fondo
    sc = c.caras["s"]
    for i, col in enumerate(((160, 162, 172), (140, 142, 150), (160, 162, 172), (120, 122, 130))):
        u = 9.4 + i * 0.7
        o.fc(sc, u, s + 2.2, -1.0, u + 0.06, s + 3.4, -1.08, WD)
        o.fc(sc, u - 0.15, s + 3.2, -1.0, u + 0.21, s + 3.4, -1.12, col)
    o.fc(sc, 9.0, s + 3.5, -1.0, 12.4, s + 3.62, -1.14, WDD, 2)
    armero(o, 14, s, 5.1, 3)
    c.ocupa("armero", 14, 5.1, 17, 5.6, s, s + 2.6)
    c.mueble(129, 4, s, 6, 0, "saco de carbon")
    o.f(4.2, s + 0.65, 6.2, 4.8, s + 0.8, 6.8, (30, 30, 34))
    c.cartel_colgante("o", 2.5, s + 3, "yunque")
    c.farol_pared("o", 3.5, s + 3.5)
    return o


# ======================================================================== 3. carpinteria semiabierta
def carpinteria():
    W, D = 22, 18
    o = Obra("cw_carpinteria", W, 26, D,
             "Carpinteria semiabierta (progreso: muebles, arcos, mejoras de casa). Frente abierto con pilares; banco de carpintero "
             "con tornillo y herramientas, caballetes con tronco y sierra, pilas de tablas, troncos afuera, virutas. Cartel con sierra.",
             entry=(10, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    c = Casa(o, 3, 4, 18, 13, muro="muro_ocre", teja="techo_rojo")
    s = c.suelos[0]
    c.abrir("n", 1, 15, 0, cada=5)
    c.ventana("e", 3); c.ventana("o", 5)
    mesa_trabajo(o, c, 5, 11.6, s, 4)
    caballete_tronco(o, c, 11, 8, s)
    pila_tablas(o, c, 13.6, 11.8, s, 7)
    pila_tablas(o, c, 4.2, 6.2, s, 4)
    sc = c.caras["s"]
    for i in range(4):   # sierras y escuadras colgadas
        u = 2.4 + i * 0.8
        o.fc(sc, u, s + 2.4, -1.0, u + 0.5, s + 2.9, -1.04, (196, 200, 210))
        o.fc(sc, u + 0.4, s + 2.5, -1.04, u + 0.6, s + 2.9, -1.08, WD)
    c.mueble(128, 16.5, s, 6, 0, "barril de clavos")
    for (xx, zz) in ((20.1, 6), (20.9, 6)):          # troncos afuera, a lo largo del muro este
        o.f(xx, 1, zz, xx + 0.6, 1.6, zz + 2.6, (112, 76, 44), 5)
        o.f(xx + 0.05, 1.05, zz - 0.02, xx + 0.55, 1.55, zz, (200, 170, 120))
    c.cartel_colgante("o", 2.5, s + 3, "sierra")
    c.farol_pared("e", 7.0, s + 3.5); c.farol_pared("o", 7.6, s + 3.5)
    return o


# ======================================================================== 4. pabellon de entrenamiento
def _laberinto(nx, nz, semilla=7):
    """Laberinto por recorrido en profundidad; devuelve el set de paredes abiertas ((a),(b))."""
    import random
    r = random.Random(semilla)
    vis, abiertos, pila = {(0, 0)}, set(), [(0, 0)]
    while pila:
        x, z = pila[-1]
        vec = [(x + dx, z + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < nx and 0 <= z + dz < nz and (x + dx, z + dz) not in vis]
        if not vec:
            pila.pop()
            continue
        n = r.choice(vec)
        abiertos.add(frozenset(((x, z), n)))
        vis.add(n)
        pila.append(n)
    return abiertos


def diana(o, x, y, z):
    """Diana de tiro con arco sobre tripode, mirando a -Z."""
    cx = x + 0.5
    for dx in (-0.5, 0.5):
        o.f(cx + dx - 0.06, y, z + 0.5, cx + dx + 0.06, y + 1.8, z + 0.62, WDD)
    o.f(cx - 0.06, y, z + 0.9, cx + 0.06, y + 1.6, z + 1.0, WDD)
    for i, (r, col) in enumerate(((0.75, (240, 236, 220)), (0.58, (60, 110, 190)), (0.42, (200, 50, 50)), (0.24, (240, 200, 60)))):
        o.f(cx - r, y + 1.6 - r, z + 0.4 - i * 0.02, cx + r, y + 1.6 + r, z + 0.5 - i * 0.02, col)
    o.f(cx - 0.5, y + 1.0, z + 0.48, cx - 0.42, y + 2.2, z + 0.56, PAJA2)
    o.put(x, y, z, COL_INV)


def pabellon_entrenamiento():
    W, D = 28, 24
    o = Obra("cw_pabellon_entrenamiento", W, 20, D,
             "Pabellon de entrenamiento (progreso: probar habilidades y armas). Plataforma de piedra con suelo de laberinto morado "
             "y crema, 8 columnas de piedra con capitel, arquitrabe de madera y techo de losas escalonado. Munecos de practica, "
             "dianas de tiro, armero y faroles colgantes.",
             entry=(13, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    o.mbox(2, 1, 3, 25, 2, 20, "zocalo")
    o.mbox(3, 2, 4, 24, 2, 19, "acera")
    o.mbox(10, 1, 2, 17, 1, 2, "piedra")
    y = 3
    # suelo de laberinto: fondo morado y muros crema de 0,5 sobre celdas de 2
    X0, Z0, NX, NZ = 4, 5, 10, 7
    o.f(X0, y, Z0, X0 + NX * 2, y + 0.02, Z0 + NZ * 2, (86, 40, 132))
    ab = _laberinto(NX, NZ)
    CR = (232, 220, 190)
    for i in range(NX):
        for j in range(NZ):
            x0, z0 = X0 + i * 2, Z0 + j * 2
            if i + 1 < NX and frozenset(((i, j), (i + 1, j))) not in ab:
                o.f(x0 + 1.75, y + 0.02, z0 - 0.25, x0 + 2.25, y + 0.04, z0 + 2.25, CR)
            if j + 1 < NZ and frozenset(((i, j), (i, j + 1))) not in ab:
                o.f(x0 - 0.25, y + 0.04, z0 + 1.75, x0 + 2.25, y + 0.06, z0 + 2.25, CR)
    o.f(X0 - 0.5, y + 0.06, Z0 - 0.5, X0 + NX * 2 + 0.5, y + 0.08, Z0, CR)
    o.f(X0 - 0.5, y + 0.06, Z0 + NZ * 2, X0 + NX * 2 + 0.5, y + 0.08, Z0 + NZ * 2 + 0.5, CR)
    o.f(X0 - 0.5, y + 0.08, Z0, X0, y + 0.1, Z0 + NZ * 2, CR)
    o.f(X0 + NX * 2, y + 0.08, Z0, X0 + NX * 2 + 0.5, y + 0.1, Z0 + NZ * 2, CR)
    # columnas 2x2 con basa y capitel
    cols = [(3, 4), (9, 4), (17, 4), (23, 4), (3, 18), (9, 18), (17, 18), (23, 18), (3, 11), (23, 11)]
    for (cx, cz) in cols:
        o.mbox(cx, y, cz, cx + 1, y + 6, cz + 1, "pilar")
        o.f(cx - 0.2, y, cz - 0.2, cx + 2.2, y + 0.3, cz + 2.2, PIEDRA_F)
        o.f(cx - 0.25, y + 6.6, cz - 0.25, cx + 2.25, y + 7.0, cz + 2.25, PIEDRA_F)
    # arquitrabe de madera sobre las columnas y vigas transversales
    yt = y + 7
    o.f(2.8, yt, 3.8, 25.2, yt + 0.8, 4.0 + 2.2, WDD, 2)
    o.f(2.8, yt, 17.8, 25.2, yt + 0.8, 20.2, WDD, 2)
    o.f(2.8, yt, 6.0, 5.2, yt + 0.8, 17.8, WDD, 2)
    o.f(22.8, yt, 6.0, 25.2, yt + 0.8, 17.8, WDD, 2)
    for xx in range(7, 23, 4):
        o.f(xx, yt + 0.2, 6.0, xx + 0.6, yt + 0.8, 17.8, WD, 2)
    # techo de losas escalonado
    yr = yt + 1
    o.f(5.2, yr - 0.03, 6.0, 22.8, yr, 17.8, (110, 76, 50), 2)
    for k, (a0, a1, b0, b1) in enumerate(((2, 25, 3, 20), (4, 23, 5, 18), (6, 21, 7, 16), (8, 19, 9, 14))):
        o.mbox(a0, yr + k, b0, a1, yr + k, b1, "techo")
    # munecos, dianas, armero, faroles colgantes
    for (mx, mz) in ((7, 8), (12, 8), (15, 8), (20, 8)):
        muneco(o, mx, y, mz, 0)
    diana(o, 11, y, 16); diana(o, 15, y, 16)
    armero(o, 5, y, 18.3, 3)
    armero(o, 19.5, y, 18.3, 3)
    for (fx, fz) in ((8.0, 11.5), (19.9, 11.5)):
        o.f(fx - 0.02, yt - 1.4, fz - 0.02, fx + 0.02, yt, fz + 0.02, HIERRO2)
        farol(o, fx, yt - 2.55, fz, 1.0)
    for (px, pz) in ((1, 1), (25, 1)):
        farola(o, px, 1, pz)
    return o


# ======================================================================== 5. casas en hilera
def _casa_hilera(o, x0, muro, teja, pisos, esquinas, cornisa, ventana_lado, chim_lado, idx):
    c = Casa(o, x0, 4, x0 + 13, 15, pisos=pisos, muro=muro, teja=teja, esquinas=esquinas, cornisa=cornisa)
    s = c.suelos[0]
    c.puerta("n", 6)
    for p in range(pisos):
        c.ventana("n", 1, p); c.ventana("n", 11, p)
    if pisos > 1:
        c.ventana("s", 6, 1)
    if ventana_lado:
        for p in range(pisos):
            if chim_lado == ventana_lado and p == 0:
                continue
            c.ventana(ventana_lado, 2 if chim_lado == ventana_lado else 5, p)
    if chim_lado:
        c.chimenea(chim_lado, 5)
    c.farol_pared("n", 4.4, s + 1, interior=False); c.farol_pared("n", 9.6, s + 1, interior=False)
    X = x0
    if pisos > 1:
        escalera(c, X + 3, 13, 14, 0, 1)
        c.mueble(124, X + 7, s, 9, 0, "mesa"); c.mueble(131, X + 7.5, s, 8, 2, "silla"); c.mueble(131, X + 7.5, s, 10, 0, "silla")
        c.mueble(128, X + 12, s, 11, 0, "barril")
        planta(o, X + 12, s, 5, casa=c)
        s2 = c.suelos[1]
        c.cama_con_cofre(X + 1.5, s2, 5, 2)
        c.mueble(133, X + 12, s2, 7, 3, "armario")
        c.alfombra(X + 5, 6, X + 10, 10.5, 1, (AZUL, ROJO, MORADO)[idx % 3], ORO, 0.5)
        c.farol_pared("e" if chim_lado != "e" else "o", 6.5, s + 3.5)
        c.farol_pared("o" if chim_lado != "o" else "e", 6.5, s2 + 3.5)
    else:
        c.cama_con_cofre(X + 2.5, s, 11, 0)
        c.mueble(124, X + 7, s, 9, 0, "mesa"); c.mueble(131, X + 7.5, s, 8, 2, "silla"); c.mueble(131, X + 7.5, s, 10, 0, "silla")
        c.mueble(133, X + 1, s, 12, 1, "armario")
        c.alfombra(X + 3, 7.5, X + 8, 11.5, 0, ROJO, ORO, 0.5)
        c.farol_pared("s", 4.5, s + 3.5)
    if idx == 2:
        c.enredadera("n", 12.6, s - 1, c.roof_y - 0.5, 1.4)
    return c


def casas_hilera():
    W, D = 44, 19
    o = Obra("cw_casas_hilera", W, 30, D,
             "Tres casas en hilera que comparten muro (para armar calles): ocre de 2 plantas, rosa de 2 plantas con techo rojo y "
             "una de 1 planta. Cada una con su puerta, faroles, escalera o chimenea; sillares solo en las esquinas de la hilera.",
             entry=(9, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    A = _casa_hilera(o, 2, "muro_ocre", "techo", 2, ["no", "so"], ["n", "s", "o"], "o", "o", 0)
    B = _casa_hilera(o, 15, "muro_rosa", "techo_rojo", 2, [], ["n", "s"], None, None, 1)
    C = _casa_hilera(o, 28, "muro", "techo", 1, ["ne", "se"], ["n", "s", "e"], "e", "e", 2)
    for c in (A, B, C):     # suelos repintados: el zocalo de la vecina no entra a la casa
        o.mbox(c.x0 + 1, 1, c.z0 + 1, c.x1 - 1, 2, c.z1 - 1, "piso")
    return o


# ======================================================================== 6. posada con balcon y escalera exterior
def posada_balcon():
    W, D = 26, 22
    o = Obra("cw_posada_balcon", W, 30, D,
             "Posada de 2 plantas como el INN de Thalmor: balcon de madera corrido en el frente con baranda y postes, "
             "escalera exterior de piedra con pretil que sube por el lado este a la puerta del piso alto. Abajo comedor con "
             "hogar, mesas y barra; arriba cuatro camas con cofre. Cartel con cama.",
             entry=(12, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    c = Casa(o, 3, 6, 20, 17, pisos=2)             # interior x 4..19, z 7..16
    s, s2 = c.suelos
    c.puerta("n", 8)                               # x 11..12
    c.puerta("n", 8, piso=1, escalones=False)      # al balcon
    c.puerta("e", 2, piso=1, escalones=False)      # a la escalera exterior (z 8..9)
    for p in (0, 1):
        c.ventana("n", 3, p); c.ventana("n", 13, p)
        c.ventana("o", 5, p)
    c.ventana("s", 8, 1)
    c.chimenea("o", 8)                             # hogar en z 14..15
    c.cartel_colgante("n", 5.75, s + 3, "cama")
    c.enredadera("n", 16.6, s - 1, s + 6, 1.2)
    # balcon: tablado (y = s2-1) de 2 de fondo, postes al suelo, baranda
    yb = s2 - 1
    o.mbox(3, yb, 4, 20, yb, 5, "madera")
    for px in (3, 7, 16, 20):
        o.f(px + 0.2, 1, 4.1, px + 0.6, yb, 4.5, WDD, 2)
        for yy in range(1, yb):
            o.put(px, yy, 4, COL_INV)
        o.f(px + 0.1, yb - 0.5, 4.5, px + 0.7, yb - 0.3, 6.0, WD, 2)       # jabalcon
    baranda(o, 3, 21, 4.0, s2, "x")
    baranda(o, 4.26, 6, 3.0, s2, "z", pilares=False)
    baranda(o, 4.26, 6, 20.74, s2, "z", pilares=False)
    jarron_flores(o, 4.2, s2, 4.3); jarron_flores(o, 19.0, s2, 4.3)
    # escalera exterior de piedra por el este (sube hacia el frente) con pretil
    for k in range(1, 11):
        z = 20 - k
        o.mbox(21, 1, z, 22, k, z, "piedra")
        o.mat(23, k + 1, z, "piedra"); o.mbox(23, 1, z, 23, k, z, "piedra")
    o.mbox(21, 1, 8, 22, 10, 9, "piedra")          # descanso frente a la puerta alta
    o.mbox(23, 1, 8, 23, 11, 9, "piedra")
    o.mbox(21, 1, 7, 23, 11, 7, "piedra")
    # planta baja: comedor
    barra(o, 14, 13, 18, 13, s, "n", casa=c, nombre="barra")
    for x in (14, 15, 16, 17):
        c.mueble(128, x, s, 16, 0, "barril")
    c.mueble(123, 7, s, 9, 0, "mesa larga"); c.mueble(125, 7, s, 8, 0, "banco"); c.mueble(125, 7, s, 10, 2, "banco")
    mesa_redonda(o, 16.5, s, 9.5, casa=c)
    c.mueble(126, 14.1, s, 9, 0, "taburete"); c.mueble(126, 17.9, s, 9, 0, "taburete")
    c.farol_pared("s", 4.0, s + 3.5); c.farol_pared("e", 6.0, s + 3.5)
    # planta alta: cuartos
    for x in (4.5, 7.5, 14.5):
        c.cama_con_cofre(x, s2, 12, 0)
    c.mueble(133, 4, s2, 8, 1, "armario")
    c.alfombra(8, 8, 15, 11, 1, AZUL, CELESTE, 0.5)
    c.farol_pared("o", 3.0, s2 + 3.5); c.farol_pared("s", 13.5, s2 + 3.5)
    return o


# ======================================================================== 7. pozo con techito
def pozo():
    W, D = 12, 12
    o = Obra("cw_pozo", W, 10, D,
             "Pozo de plaza: brocal redondo de piedra con agua al fondo, dos postes, travesano con manivela, cuerda y balde, "
             "techito a dos aguas. Losas alrededor y macetas.",
             entry=(6, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    cx = cz = 6.0
    for x in range(W):
        for z in range(D):
            d = math.hypot(x + 0.5 - cx, z + 0.5 - cz)
            if 1.6 <= d < 2.8:
                o.mbox(x, 1, z, x, 2, z, "piedra")
    for x in range(W):
        for z in range(D):
            if math.hypot(x + 0.5 - cx, z + 0.5 - cz) < 1.6:
                o.clear(x, 0, z)
    o.f(cx - 1.8, 0.0, cz - 1.8, cx + 1.8, 0.12, cz + 1.8, (34, 58, 92))
    o.f(cx - 0.8, 0.12, cz - 0.5, cx - 0.4, 0.14, cz - 0.4, (90, 150, 200))
    o.f(cx + 0.2, 0.12, cz + 0.3, cx + 0.7, 0.14, cz + 0.4, (90, 150, 200))
    for x in range(W):          # remate claro del brocal
        for z in range(D):
            d = math.hypot(x + 0.5 - cx, z + 0.5 - cz)
            if 1.6 <= d < 2.8:
                o.f(x - 0.04, 3.0, z - 0.04, x + 1.04, 3.12, z + 1.04, PIEDRA_F) if (x + z) % 2 == 0 else o.f(x, 3.0, z, x + 1, 3.1, z + 1, (162, 158, 148))
    for px in (cx - 2.6, cx + 2.2):
        o.f(px, 3.0, cz - 0.2, px + 0.4, 6.3, cz + 0.2, WDD, 2)
    o.f(cx - 2.8, 5.6, cz - 0.12, cx + 2.8, 5.85, cz + 0.12, WD, 5)
    o.f(cx + 2.6, 5.62, cz - 0.04, cx + 3.0, 5.7, cz + 0.04, HIERRO)          # manivela
    o.f(cx + 2.95, 5.3, cz - 0.04, cx + 3.03, 5.7, cz + 0.04, HIERRO)
    o.f(cx + 2.9, 5.24, cz - 0.07, cx + 3.1, 5.32, cz + 0.07, WD)
    o.f(cx - 0.4, 5.55, cz - 0.16, cx + 0.4, 5.9, cz + 0.16, (176, 150, 100))   # cuerda enrollada
    o.f(cx - 0.02, 4.0, cz - 0.02, cx + 0.02, 5.6, cz + 0.02, (176, 150, 100))
    o.f(cx - 0.28, 3.5, cz - 0.28, cx + 0.28, 4.0, cz + 0.28, (130, 90, 56), 2)  # balde
    o.f(cx - 0.3, 3.62, cz - 0.3, cx + 0.3, 3.68, cz + 0.3, HIERRO)
    o.f(cx - 0.3, 3.88, cz - 0.3, cx + 0.3, 3.94, cz + 0.3, HIERRO)
    o.f(cx - 0.3, 4.0, cz - 0.02, cx + 0.3, 4.04, cz + 0.02, HIERRO)
    for k in range(4):          # techito a dos aguas (escalones finos)
        h = 6.3 + k * 0.25
        o.f(cx - 3.2, h, cz - 1.9 + k * 0.45, cx + 3.2, h + 0.25, cz + 1.9 - k * 0.45, (46, 86, 82))
    o.f(cx - 3.3, 7.3, cz - 0.15, cx + 3.3, 7.45, cz + 0.15, WDD, 2)
    for (x, z) in ((1, 1), (10, 10)):
        o.obj(159, x, 1, z)
    o.put(int(cx - 2.6), 3, int(cz), COL_INV); o.put(int(cx + 2.2), 3, int(cz), COL_INV)
    return o


# ======================================================================== 8. torre de vigia / campanario
def campana(o, cx, ytop, cz):
    o.f(cx - 0.12, ytop - 0.25, cz - 0.12, cx + 0.12, ytop, cz + 0.12, HIERRO)
    for i, (r, h) in enumerate(((0.38, 0.25), (0.48, 0.3), (0.58, 0.35), (0.7, 0.3), (0.82, 0.15))):
        y0 = ytop - 0.25 - sum(hh for _, hh in ((0.38, 0.25), (0.48, 0.3), (0.58, 0.35), (0.7, 0.3), (0.82, 0.15))[:i + 1])
        o.f(cx - r, y0, cz - r, cx + r, y0 + h, cz + r, BRONCE if i % 2 == 0 else (164, 116, 52))
    yb = ytop - 1.6
    o.f(cx - 0.04, yb - 0.3, cz - 0.04, cx + 0.04, yb + 0.6, cz + 0.04, HIERRO)
    o.f(cx - 0.12, yb - 0.45, cz - 0.12, cx + 0.12, yb - 0.25, cz + 0.12, HIERRO)


def torre_vigia():
    W, D = 14, 14
    o = Obra("cw_torre_vigia", W, 40, D,
             "Torre de vigia / campanario de 3 plantas (8x8). Escalera de piedra pegada a los muros en cada planta, ventanas "
             "angostas, ultima planta abierta con pilares y pretil, campana de bronce, techo con aguja y veleta.",
             entry=(6, 13, "sur"))
    acera(o, 0, 0, W - 1, D - 1)
    c = Casa(o, 3, 3, 10, 10, pisos=3)              # interior x 4..9, z 4..9
    s0, s1, s2 = c.suelos
    c.puerta("s", 3)                                # x 6..7
    for p in (0, 1):
        for cn in ("n", "e", "o"):
            c.ventana(cn, 3, p, flores=False, w=1)
    c.ventana("s", 3, 1, flores=False, w=1)
    escalera_perimetral(c, [(4, 8), (4, 7), (4, 6), (4, 5), (4, 4), (5, 4), (6, 4), (7, 4)], 0, "piedra")
    escalera_perimetral(c, [(8, 4), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (8, 9)], 1, "piedra")
    for cn in ("n", "s", "e", "o"):
        c.abrir(cn, 1, 7, 2, cada=5, viga=False)
        for u in range(2, 6):
            x, y, z = c.celda(cn, u, s2)
            o.mat(x, y, z, c.muro)
    # aguja y veleta sobre el techo
    for y in range(c.cumbre + 1, c.cumbre + 4):
        o.mbox(6, y, 6, 7, y, 7, "techo")
    t = c.cumbre + 4
    o.f(6.85, t, 6.85, 7.15, t + 1.4, 7.15, BRONCE)
    o.f(6.2, t + 1.0, 6.95, 7.8, t + 1.1, 7.05, BRONCE)
    o.f(7.4, t + 0.8, 6.98, 7.9, t + 1.2, 7.02, BRONCE)
    # viga y campana
    o.f(3.5, c.roof_y - 0.7, 6.7, 10.5, c.roof_y - 0.2, 7.3, WDD, 2)
    campana(o, 7.0, c.roof_y - 0.7, 7.0)
    c.farol_pared("e", 1.5, s0 + 3.5)
    return o


# ======================================================================== 9. granero y establo
def montura(o, cara, c, u, y):
    """Silla de montar en una percha de pared (cara interior)."""
    o.fc(cara, u + 0.35, y + 0.4, -1.0, u + 0.65, y + 0.5, -1.7, WDD)
    o.fc(cara, u + 0.05, y + 0.5, -1.15, u + 0.95, y + 0.75, -1.65, CUERO)
    o.fc(cara, u, y + 0.75, -1.2, u + 0.2, y + 0.95, -1.6, CUERO)
    o.fc(cara, u + 0.8, y + 0.75, -1.2, u + 1.0, y + 0.9, -1.6, CUERO)
    o.fc(cara, u + 0.1, y - 0.2, -1.6, u + 0.2, y + 0.5, -1.66, (90, 60, 40))
    o.fc(cara, u + 0.05, y - 0.3, -1.6, u + 0.25, y - 0.2, -1.68, HIERRO2)


def granero_establo():
    W, D = 28, 22
    o = Obra("cw_granero_establo", W, 26, D,
             "Granero y establo (progreso: monturas). Muros de tablas con sillares, porton de 4x4, cinco boxes con divisiones, "
             "comedero y balde, paja en el suelo, fardos apilados, sillas de montar colgadas, horquilla, carreta afuera.",
             entry=(14, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    c = Casa(o, 3, 4, 24, 17, pisos=1, h=8, muro="madera_pared", teja="techo_rojo")   # interior x 4..23, z 5..16
    s = c.suelos[0]
    c.puerta("n", 9, w=4, h=4)                      # x 12..15
    c.ventana("n", 3, flores=False); c.ventana("n", 17, flores=False)
    c.ventana("o", 3, flores=False); c.ventana("e", 3, flores=False)
    # boxes: x 4..23 en 5 de 4, fondo z 12..16
    for b in (8, 12, 16, 20):
        o.f(b - 0.1, s, 12, b + 0.1, s + 1.6, 17, (150, 104, 62), 2)
        o.f(b - 0.15, s + 1.6, 12, b + 0.15, s + 1.75, 17, WDD, 2)
    for i, b in enumerate((4, 8, 12, 16, 20)):
        c.ocupa("box %d" % (i + 1), b, 12, b + 4, 17, s, s + 1.8, True, choca=False)
        x0 = b + 0.1 if b > 4 else b
        x1 = b + 3.9 if b < 20 else b + 4
        for yy in (0.6, 1.25):
            o.f(x0, s + yy, 11.9, x0 + 1.2, s + yy + 0.15, 12.1, WD, 2)
            o.f(x1 - 1.2, s + yy, 11.9, x1, s + yy + 0.15, 12.1, WD, 2)
        o.f(x0 + 1.2, s, 11.85, x0 + 1.4, s + 1.6, 12.15, WDD)
        o.f(x1 - 1.4, s, 11.85, x1 - 1.2, s + 1.6, 12.15, WDD)
        for xx in (x0, x1 - 1):
            o.put(int(xx), s, 12, COL_INV); o.put(int(xx), s + 1, 12, COL_INV)
        # paja del suelo, comedero y balde
        for k in range(6):
            px, pz = b + 0.3 + (_h(b, k) % 30) / 10.0, 12.4 + (_h(b, k, 1) % 40) / 10.0
            o.f(px, s, pz, px + 0.6, s + 0.04, pz + 0.4, PAJA if k % 2 else PAJA2)
        o.f(b + 0.8, s, 16.3, b + 3.2, s + 0.8, 16.95, (124, 84, 52), 2)
        o.f(b + 0.9, s + 0.65, 16.4, b + 3.1, s + 0.75, 16.85, (120, 160, 70))
        o.f(b + 3.3, s, 13.0, b + 3.75, s + 0.45, 13.45, (130, 90, 56), 2)
        o.f(b + 3.35, s + 0.38, 13.05, b + 3.7, s + 0.42, 13.4, (70, 120, 170))
    # fardos y horquilla
    for (x, z, y) in ((4.2, 5.2, s), (4.2, 6.1, s), (4.2, 5.6, s + 0.7)):
        fardo_paja(o, x, y, z, 0)
    c.ocupa("fardos", 4.2, 5.2, 5.5, 6.9, s, s + 1.4, True)
    for (x, z, y) in ((21.8, 5.2, s), (21.8, 6.1, s)):
        fardo_paja(o, x, y, z, 0)
    c.ocupa("fardos", 21.8, 5.2, 23.1, 6.9, s, s + 0.7, True)
    o.f(16.25, s, 11.6, 16.32, s + 2.0, 11.68, WD)
    for dx in (-0.12, 0.0, 0.12):
        o.f(16.26 + dx, s + 2.0, 11.6, 16.3 + dx, s + 2.35, 11.66, HIERRO2)
    o.f(16.14, s + 1.98, 11.6, 16.44, s + 2.03, 11.66, HIERRO2)
    ce = c.caras["e"]
    montura(o, ce, c, 2.5, s + 2.2); montura(o, ce, c, 4.5, s + 2.2)
    c.ocupa("sillas de montar", 22, 6.5, 23.0, 9.5, s + 1.8, s + 3.2, True)
    c.farol_pared("o", 8.0, s + 4); c.farol_pared("s", 10.5, s + 4.5)
    # afuera: carreta y fardos
    o.obj(1016, 26, 1, 8, 1)
    for (x, z, y) in ((25.6, 11.0, 1), (25.6, 11.9, 1)):
        fardo_paja(o, x, y, z, 1)
    return o


# ======================================================================== 10. muro de ciudad con porton
def muro_porton():
    W, D = 48, 16
    o = Obra("cw_muro_porton", W, 22, D,
             "Tramo de muralla con porton (3 de grueso, 10 de alto, adarve con almenas) y casa de guardia de dos torres de 6x7 "
             "con almenas, saeteras y estandartes. Porton de 4x6 con arco, rastrillo levantado y hojas abiertas hacia adentro. "
             "Escaleras de piedra al adarve por dentro y faroles a los lados del paso.",
             entry=(23, 0, "norte"))
    for x in range(W):
        for z in range(D):
            o.mat(x, 0, z, "acera_os" if (_h(x // 2, z // 2) % 4 == 0) else "acera")
    o.mbox(0, 0, 6, W - 1, 9, 8, "piedra_muralla")
    for x in range(W):
        if x % 3 != 2:
            o.mbox(x, 10, 6, x, 11, 6, "piedra_muralla")
    for (a, b) in ((16, 21), (26, 31)):
        o.mbox(a, 0, 4, b, 13, 10, "piedra_muralla")
        for x in range(a, b + 1):
            for z in range(4, 11):
                if (x in (a, b) or z in (4, 10)) and (x + z) % 2 == 0:
                    o.mbox(x, 14, z, x, 15, z, "piedra_muralla")
        for xx in (a + 1.7, b - 0.7):                 # saeteras
            for yy in (4.5, 9.5):
                o.f(xx, yy, 3.96, xx + 0.3, yy + 1.6, 4.0, (34, 30, 30))
        o.f(a + 0.8, 7, 3.9, b + 0.2, 7.2, 4.0, WDD)   # estandarte
        o.f(a + 1.4, 3.2, 3.88, b - 0.4, 7.0, 3.95, (150, 34, 44))
        o.f(a + 2.2, 4.4, 3.84, b - 1.2, 6.0, 3.88, (206, 168, 72))
        o.f(a + 2.6, 4.0, 3.84, b - 1.6, 4.4, 3.88, (206, 168, 72))
    o.clear(22, 0, 6, 25, 5, 8)
    for (x, y) in ((22, 5), (25, 5)):
        o.mat(x, y, 6, "piedra_muralla"); o.mat(x, y, 7, "piedra_muralla"); o.mat(x, y, 8, "piedra_muralla")
    o.mbox(22, 0, 4, 25, 0, 10, "acera")
    # rastrillo levantado
    for xx in range(22, 26):
        for k in range(2):
            o.f(xx + 0.15 + k * 0.5, 4.0, 6.45, xx + 0.25 + k * 0.5, 5.0, 6.55, HIERRO)
    for yy in (4.2, 4.6):
        o.f(22, yy, 6.42, 26, yy + 0.1, 6.58, HIERRO)
    for xx in range(22, 26):
        for k in range(2):
            o.f(xx + 0.15 + k * 0.5, 3.75, 6.47, xx + 0.25 + k * 0.5, 4.0, 6.53, HIERRO2)
    # hojas abiertas hacia adentro, pegadas a las torres
    for (xa, xb) in ((22.0, 22.25), (25.75, 26.0)):
        o.f(xa, 0, 9, xb, 5.0, 11.0, (124, 82, 50), 2)
        for yy in (1.0, 3.8):
            o.f(xa - 0.03, yy, 9.1, xb + 0.03, yy + 0.18, 10.9, HIERRO)
    # escaleras al adarve por dentro
    for k in range(1, 11):
        o.mbox(1 + k, 0, 9, 1 + k, k - 1, 10, "piedra_muralla")
        o.mbox(46 - k, 0, 9, 46 - k, k - 1, 10, "piedra_muralla")
    # faroles a los lados del paso (por fuera)
    for fx in (21.5, 26.5):
        o.f(fx - 0.05, 5.2, 3.6, fx + 0.05, 5.3, 4.0, HIERRO)
        farol(o, fx, 4.0, 3.55, 1.0)
    return o


# ======================================================================== 11. puente de piedra
def puente_piedra():
    W, D = 40, 16
    o = Obra("cw_puente_piedra", W, 16, D,
             "Puente de piedra de un arco (luz 16) sobre un rio entre dos orillas de pasto. Tablero empedrado con pretiles, "
             "farolas en los extremos y en el centro, juncos en las orillas.",
             entry=(2, 7, "oeste"))
    for x in list(range(0, 12)) + list(range(28, 40)):
        for z in range(D):
            o.mbox(x, 0, z, x, 2, z, "pasto_os")
            o.mat(x, 3, z, "pasto" if _h(x, z) % 5 else "pasto_os")
    for z in range(D):
        o.mbox(11, 0, z, 11, 3, z, "piedra"); o.mbox(28, 0, z, 28, 3, z, "piedra")
        for x in range(12, 28):
            o.mat(x, 0, z, "tierra_os")
    o.f(12, 1.0, 0, 28, 1.08, D, (60, 116, 176))
    for i in range(10):
        x = 12.5 + (_h(i) % 140) / 10.0
        z = 0.5 + (_h(i, 2) % 140) / 10.0
        o.f(x, 1.08, z, x + 0.8, 1.1, z + 0.15, (130, 180, 220))
    def h(x):
        return 3 + int(round(2.2 * math.sin(math.pi * (x + 0.5 - 8) / 24.0)))
    for x in range(8, 32):
        top = h(x)
        a = 0 if not (12 <= x <= 27) else int(math.ceil(0.4 + 3.4 * math.sin(math.pi * (x + 0.5 - 12) / 16.0)))
        for z in range(5, 11):
            for y in range(a, top + 1):
                o.mat(x, y, z, "acera" if y == top and 6 <= z <= 9 else "piedra_muralla")
            o.mat(x, top + 1, 5, "piedra_muralla"); o.mat(x, top + 1, 10, "piedra_muralla")
        o.f(x - 0.02, top + 2, 4.9, x + 1.02, top + 2.12, 6.1, PIEDRA_F)
        o.f(x - 0.02, top + 2, 9.9, x + 1.02, top + 2.12, 11.1, PIEDRA_F)
    for x in (8, 19, 31):
        for z in (5, 10):
            farol(o, x + 0.5, h(x) + 2.12, z + 0.5, 1.0)
    for (x, z) in ((10, 2), (10, 13), (29, 3), (29, 12), (9, 4)):
        o.obj(1006, x, 4, z)
    return o


# ======================================================================== 12. torre arcana
def mesa_encantar(o, c, cx, y, cz):
    c.ocupa("mesa de encantamientos", cx - 0.8, cz - 0.8, cx + 0.8, cz + 0.8, y, y + 2.6, True)
    o.f(cx - 0.75, y, cz - 0.75, cx + 0.75, y + 0.25, cz + 0.75, (90, 86, 100))
    o.f(cx - 0.5, y + 0.25, cz - 0.5, cx + 0.5, y + 1.0, cz + 0.5, (110, 104, 124))
    o.f(cx - 0.7, y + 1.0, cz - 0.7, cx + 0.7, y + 1.2, cz + 0.7, (70, 40, 100))
    o.f(cx - 0.45, y + 1.2, cz - 0.3, cx - 0.02, y + 1.3, cz + 0.3, (240, 234, 214))
    o.f(cx + 0.02, y + 1.2, cz - 0.3, cx + 0.45, y + 1.3, cz + 0.3, (240, 234, 214))
    o.f(cx - 0.02, y + 1.2, cz - 0.32, cx + 0.02, y + 1.32, cz + 0.32, (90, 50, 120))
    o.f(cx - 0.2, y + 1.3, cz - 0.15, cx + 0.2, y + 1.34, cz + 0.15, (200, 150, 255), 0, 1)
    for i in range(3):
        a = i * 2.1
        x, z = cx + math.cos(a) * 0.9, cz + math.sin(a) * 0.9
        yy = y + 1.8 + i * 0.25
        o.f(x - 0.08, yy, z - 0.08, x + 0.08, yy + 0.35, z + 0.08, (120, 230, 255), 0, 1)
        o.f(x - 0.04, yy + 0.35, z - 0.04, x + 0.04, yy + 0.45, z + 0.04, (190, 250, 255), 0, 1)
    o.put(int(math.floor(cx)), y, int(math.floor(cz)), COL_INV)


def circulo_runas(o, cx, y, cz, r=2.3):
    n = 28
    for i in range(n):
        a = 2 * math.pi * i / n
        x, z = cx + math.cos(a) * r, cz + math.sin(a) * r
        o.f(x - 0.14, y, z - 0.14, x + 0.14, y + 0.03, z + 0.14, (170, 100, 240), 0, 1)
        if i % 4 == 0:
            x2, z2 = cx + math.cos(a) * (r - 0.5), cz + math.sin(a) * (r - 0.5)
            o.f(x2 - 0.1, y, z2 - 0.1, x2 + 0.1, y + 0.03, z2 + 0.1, (210, 160, 255), 0, 1)


def cristales(o, x, y, z):
    for (dx, dz, h, w) in ((0.3, 0.3, 0.9, 0.18), (0.6, 0.5, 0.6, 0.14), (0.2, 0.65, 0.5, 0.12), (0.55, 0.2, 0.4, 0.1)):
        o.f(x + dx - w, y, z + dz - w, x + dx + w, y + h, z + dz + w, (110, 220, 250), 0, 1)
        o.f(x + dx - w * 0.5, y + h, z + dz - w * 0.5, x + dx + w * 0.5, y + h + 0.15, z + dz + w * 0.5, (180, 245, 255), 0, 1)


def telescopio(o, x, y, z):
    """Telescopio de laton en tripode apuntando a -Z y hacia arriba."""
    for (dx, dz) in ((-0.4, 0.3), (0.4, 0.3), (0.0, -0.4)):
        o.f(x + dx - 0.04, y, z + dz - 0.04, x + dx + 0.04, y + 1.3, z + dz + 0.04, WDD)
    o.f(x - 0.12, y + 1.3, z - 0.12, x + 0.12, y + 1.42, z + 0.12, BRONCE)
    for i in range(5):
        r = 0.16 - i * 0.015
        o.f(x - r, y + 1.42 + i * 0.16, z + 0.2 - i * 0.28, x + r, y + 1.6 + i * 0.16, z + 0.5 - i * 0.28, BRONCE if i % 2 else (210, 170, 90))


def torre_arcana():
    W, D = 16, 16
    o = Obra("cw_torre_arcana", W, 46, D,
             "Torre arcana de 3 plantas (progreso: encantar equipo). Planta baja con circulo de runas y mesa de encantamientos "
             "(libro abierto y cristales flotantes), estanterias y cristales; primera planta biblioteca; ultima observatorio con "
             "telescopio. Escalera de piedra pegada a los muros, techo morado con aguja y orbe brillante.",
             entry=(7, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    c = Casa(o, 3, 3, 12, 12, pisos=3, muro="muro_blanco", teja="techo_morado")   # interior x 4..11, z 4..11
    s0, s1, s2 = c.suelos
    c.puerta("n", 4)                               # x 7..8
    for p in (1, 2):
        c.ventana("n", 4, p, flores=False)
    for p in (0, 1, 2):
        c.ventana("o", 4, p, flores=False)
        c.ventana("s", 4, p, flores=False)
    for p in (1, 2):
        c.ventana("e", 4, p, flores=False)
    c.cartel_colgante("n", 1.6, s0 + 3, "libro")
    escalera_perimetral(c, [(11, 5), (11, 6), (11, 7), (11, 8), (11, 9), (11, 10), (11, 11), (10, 11)], 0, "piedra")
    escalera_perimetral(c, [(9, 11), (8, 11), (7, 11), (6, 11), (5, 11), (4, 11), (4, 10), (4, 9)], 1, "piedra")
    # planta baja
    circulo_runas(o, 7.5, s0 + 0.01, 8.6, 2.1)
    mesa_encantar(o, c, 7.5, s0, 8.6)
    c.mueble(127, 4, s0, 4, 1, "estanteria")
    cristales(o, 4.1, s0, 10.0); c.ocupa("cristales", 4.1, 10.0, 5.0, 11.0, s0, s0 + 1, False)
    c.farol_pared("o", 7.6, s0 + 3.5)
    # biblioteca
    c.mueble(127, 4, s1, 4, 1, "estanteria")
    c.mueble(124, 6, s1, 7, 0, "mesa de lectura")
    c.mueble(131, 6.5, s1, 6, 2, "silla")
    c.mueble(138, 9, s1, 7, 0, "candelabro")
    o.f(6.3, s1 + 1.3, 7.2, 6.9, s1 + 1.45, 7.7, (90, 50, 120)); o.f(7.0, s1 + 1.3, 7.3, 7.6, s1 + 1.4, 7.8, (40, 90, 70))
    c.farol_pared("e", 3.5, s1 + 3.5)
    # observatorio
    telescopio(o, 7.5, s2, 5.5); c.ocupa("telescopio", 7.0, 5.0, 8.0, 6.0, s2, s2 + 2.4, True)
    c.mueble(124, 6, s2, 8, 0, "mesa de cartas")
    o.f(6.1, s2 + 1.3, 8.1, 7.9, s2 + 1.32, 8.9, (30, 40, 80))
    for i in range(6):
        o.f(6.3 + (i * 0.27) % 1.5, s2 + 1.32, 8.25 + (i * 0.19) % 0.55, 6.36 + (i * 0.27) % 1.5, s2 + 1.34, 8.31 + (i * 0.19) % 0.55, (250, 240, 170))
    # aguja y orbe
    for y in range(c.cumbre + 1, c.cumbre + 5):
        o.mbox(7, y, 7, 8, y, 8, "techo_morado")
    t = c.cumbre + 5
    o.f(7.85, t, 7.85, 8.15, t + 0.8, 8.15, BRONCE)
    o.f(7.65, t + 0.8, 7.65, 8.35, t + 1.5, 8.35, (180, 120, 255), 0, 1)
    return o


TODOS = [tienda_pociones, herreria, carpinteria, pabellon_entrenamiento, casas_hilera, posada_balcon, pozo,
         torre_vigia, granero_establo, muro_porton, puente_piedra, torre_arcana]
