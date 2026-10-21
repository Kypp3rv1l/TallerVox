# Farlands Taller v0.1.8 - estructuras nuevas estilo Cube World (pueblo y progreso).
# Las genera tools/cw_propuestas.py junto con las demas. Todas pasan por la revision de criterio de Casa
# (paso de puertas/escaleras libre, nada inflamable junto al fuego, nada tapando ventanas, objetos que no chocan).
import math
from cw_lib import Obra, WD, WDD, COL_INV, _h
from cw_casas import (Casa, planta, jarron_flores, mesa_redonda, escalera, escalera_perimetral, escalera_mano, barra, tablero,
                      farol, baranda, pilar_baranda, HOJA, HOJA2, HIERRO, HIERRO2, PIEDRA_F)
from cw_vox import Pieza, Vox, torno
import cw_muebles as M
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


# ======================================================================== 9. granero y establo
def montura(o, cara, c, u, y):
    """Silla de montar en una percha de pared (cara interior)."""
    o.fc(cara, u + 0.35, y + 0.4, -1.0, u + 0.65, y + 0.5, -1.7, WDD)
    o.fc(cara, u + 0.05, y + 0.5, -1.15, u + 0.95, y + 0.75, -1.65, CUERO)
    o.fc(cara, u, y + 0.75, -1.2, u + 0.2, y + 0.95, -1.6, CUERO)
    o.fc(cara, u + 0.8, y + 0.75, -1.2, u + 1.0, y + 0.9, -1.6, CUERO)
    o.fc(cara, u + 0.1, y - 0.2, -1.6, u + 0.2, y + 0.5, -1.66, (90, 60, 40))
    o.fc(cara, u + 0.05, y - 0.3, -1.6, u + 0.25, y - 0.2, -1.68, HIERRO2)


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


# ======================================================================== piezas detalladas (v0.1.8)
def muneco(o, x, y, z, rot=0, casco=False, escudo=False, k=0):
    """Muneco de practica (1x1, mira a -Z): base de piedra, poste, torso de paja atado, brazos de madera con paja,
    cabeza de saco cosida con ojos de boton, parche-diana en el pecho; opcional casco abollado y escudo en el brazo."""
    p = Pieza(1, 1)
    v = Vox(0.125)
    torno(v, 4.0, 4.0, 0, [3.6], lambda a, t, b: (110, 106, 100) if b else (130, 126, 118), hueco=False)
    pj = (PAJA, PAJA2, (236, 214, 140))

    # torso de paja (caja de 6x7x4 voxeles, hombros mas anchos, cintura atada) con pajas sueltas
    for j in range(9, 16):
        ancho = 3 if j >= 13 else (2 if j in (9, 10) else 3)
        for i in range(4 - ancho, 4 + ancho):
            for kk in range(2, 6):
                cuerda = j in (10, 14)
                v.set(i, j, kk, (150, 108, 60) if cuerda else pj[_h(i, j, kk) % 3])
    for (i, j, kk) in ((0, 13, 3), (7, 14, 4), (1, 9, 4), (6, 11, 2), (3, 16, 3), (5, 16, 4), (2, 12, 1), (5, 13, 6)):
        v.set(i, j, kk, (240, 220, 150))
    p.vox(v)
    p.f(0.4375, 0.125, 0.4375, 0.5625, 1.125, 0.5625, M.MADO)
    p.f(-0.25, 1.5, 0.4375, 1.25, 1.625, 0.5625, M.MAD, 2)
    for xa in (-0.25, 1.0625):
        p.f(xa, 1.4375, 0.375, xa + 0.1875, 1.6875, 0.625, PAJA2)
        p.f(xa + 0.0625, 1.42, 0.36, xa + 0.125, 1.705, 0.64, (150, 108, 60))
    p.f(0.3125, 1.1875, 0.1, 0.6875, 1.5625, 0.12, (236, 230, 214))     # parche
    p.f(0.375, 1.25, 0.08, 0.625, 1.5, 0.1, (190, 46, 46))
    p.f(0.4375, 1.3125, 0.06, 0.5625, 1.4375, 0.08, (236, 230, 214))
    p.f(0.375, 1.875, 0.375, 0.625, 1.9375, 0.625, (150, 108, 60))       # cuello atado
    p.f(0.3125, 1.9375, 0.3125, 0.6875, 2.3125, 0.6875, (198, 170, 122))  # cabeza
    p.f(0.375, 2.125, 0.29, 0.4375, 2.1875, 0.3125, (30, 30, 34))
    p.f(0.5625, 2.125, 0.29, 0.625, 2.1875, 0.3125, (30, 30, 34))
    p.f(0.375, 2.0, 0.3, 0.625, 2.03, 0.3125, (110, 80, 50))
    for xx in (0.4, 0.48, 0.56):
        p.f(xx, 1.98, 0.29, xx + 0.025, 2.05, 0.3, (110, 80, 50))
    if casco:
        p.f(0.28, 2.25, 0.28, 0.72, 2.4375, 0.72, (120, 124, 134))
        p.f(0.25, 2.22, 0.25, 0.75, 2.27, 0.75, (96, 100, 110))
        p.f(0.47, 2.0, 0.24, 0.53, 2.25, 0.29, (96, 100, 110))
        p.f(0.6, 2.36, 0.27, 0.68, 2.42, 0.28, (80, 84, 94))
    else:
        p.f(0.4375, 2.3125, 0.4375, 0.5625, 2.4375, 0.5625, PAJA)
        p.f(0.375, 2.3125, 0.5, 0.4375, 2.375, 0.5625, PAJA2)
    if escudo:
        p.f(-0.3, 1.1, 0.25, 0.0, 1.9, 0.33, (140, 92, 54), 2)
        p.f(-0.35, 1.2, 0.25, -0.3, 1.8, 0.33, (140, 92, 54), 2)
        p.f(-0.3, 1.45, 0.21, 0.0, 1.55, 0.25, M.HIE2)
        p.f(-0.2, 1.4, 0.19, -0.1, 1.6, 0.21, M.HIE)
    p.poner(o, x, y, z, rot)
    o.put(int(x), y, int(z), COL_INV); o.put(int(x), y + 1, int(z), COL_INV)


def espada(p, x, y, z, alto=1.3, guarda=M.ORO):
    """Espada vertical (punta abajo) en el marco de una Pieza; (x, z) = centro, y = punta."""
    hoja = alto * 0.68
    p.f(x - 0.04, y, z - 0.02, x + 0.04, y + 0.08, z + 0.02, M.ACERO2)
    p.f(x - 0.06, y + 0.08, z - 0.025, x + 0.06, y + hoja, z + 0.025, M.ACERO)
    p.f(x - 0.012, y + 0.15, z - 0.03, x + 0.012, y + hoja - 0.05, z + 0.03, M.ACERO2)
    p.f(x - 0.18, y + hoja, z - 0.05, x + 0.18, y + hoja + 0.06, z + 0.05, guarda)
    p.f(x - 0.21, y + hoja + 0.005, z - 0.035, x - 0.18, y + hoja + 0.09, z + 0.035, guarda)
    p.f(x + 0.18, y + hoja + 0.005, z - 0.035, x + 0.21, y + hoja + 0.09, z + 0.035, guarda)
    g0 = y + hoja + 0.06
    for i in range(4):
        p.f(x - 0.035, g0 + i * 0.07, z - 0.035, x + 0.035, g0 + i * 0.07 + 0.07, z + 0.035, M.CUERO if i % 2 else M.CUERO2)
    p.f(x - 0.055, g0 + 0.28, z - 0.055, x + 0.055, g0 + 0.36, z + 0.055, guarda)


def armero(o, x, y, z, rot=0):
    """Armero 3x1 (mira a -Z): largueros con capitel, travesano ranurado, espadas, hacha, lanza y maza; escudo arriba."""
    p = Pieza(3, 1)
    for xa in (0.0, 2.875):
        p.f(xa, 0, 0.0625, xa + 0.125, 1.9375, 0.5, M.MADO, 2)
        p.f(xa - 0.03, 1.9375, 0.03, xa + 0.155, 2.0, 0.53, M.MADC)
    p.f(0.125, 0, 0.0625, 2.875, 0.125, 0.5, M.MADO, 2)
    p.f(0.125, 0.125, 0.4375, 2.875, 1.75, 0.5, M.MAD, 2)
    p.f(0.125, 0.25, 0.125, 2.875, 0.375, 0.4375, M.MADC, 2)
    p.f(0.125, 1.25, 0.125, 2.875, 1.375, 0.4375, M.MADC, 2)
    for i, xx in enumerate((0.45, 0.85, 1.65, 2.05)):
        espada(p, xx, 0.375, 0.25, 1.3 if i % 2 else 1.4, M.ORO if i % 2 else M.HIE2)
    # lanza
    p.f(1.22, 0.375, 0.22, 1.28, 2.3, 0.28, M.MADC)
    p.f(1.21, 2.3, 0.21, 1.29, 2.36, 0.29, M.HIE2)
    p.f(1.19, 2.36, 0.235, 1.31, 2.6, 0.265, M.ACERO)
    p.f(1.22, 2.6, 0.24, 1.28, 2.7, 0.26, M.ACERO2)
    # hacha
    p.f(2.42, 0.375, 0.22, 2.48, 1.6, 0.28, M.MADC)
    p.f(2.4, 1.4, 0.2, 2.5, 1.58, 0.3, M.HIE2)
    p.f(2.5, 1.33, 0.235, 2.68, 1.62, 0.265, M.ACERO2)
    p.f(2.68, 1.28, 0.235, 2.74, 1.68, 0.265, M.ACERO)
    # escudo redondo arriba al centro
    v = Vox(0.0625)
    for j in range(-6, 6):
        for i in range(-6, 6):
            d = math.hypot(i + 0.5, j + 0.5)
            if d < 6:
                col = M.HIE2 if d > 5 or d < 1.4 else ((150, 40, 44) if (i + j) % 2 == 0 and d < 3.6 else (176, 120, 70))
                v.set(i + 6, j + 6, 0, col)
                if d > 5 or d < 1.4:
                    v.set(i + 6, j + 6, -1, col)
    p.vox(v, 1.125, 1.95, 0.4375)
    p.poner(o, x, y, z, rot)


def diana(o, x, y, z, rot=0, k=0):
    """Diana de tiro 2x1 (mira a -Z): caballete de 3 patas, disco de paja con borde y aros pintados, flechas clavadas."""
    p = Pieza(2, 1)
    for (xx, zz) in ((0.25, 0.6), (1.6875, 0.6)):
        p.f(xx, 0, zz, xx + 0.125, 2.4, zz + 0.125, M.MADO)
    p.f(0.9375, 0, 0.9, 1.0625, 2.0, 1.0, M.MADO)
    p.f(0.25, 0.75, 0.6, 1.8125, 0.875, 0.725, M.MAD)
    v = Vox(0.0625)
    aros = [(15.5, (196, 168, 110)), (14.5, (236, 230, 214)), (11.5, (40, 40, 44)), (8.5, (52, 92, 170)), (5.5, (190, 46, 46)), (2.5, (240, 200, 60))]
    for j in range(-16, 16):
        for i in range(-16, 16):
            d = math.hypot(i + 0.5, j + 0.5)
            if d >= 15.5:
                continue
            col = aros[0][1]
            for (r, c2) in aros:
                if d < r:
                    col = c2
            v.set(i + 16, j + 16, 0, col)
            if d < 14.5:
                v.set(i + 16, j + 16, 1, PAJA2)
            v.set(i + 16, j + 16, 2, PAJA2 if d < 13 else (180, 150, 90))
    p.vox(v, 0.0, 0.5, 0.4)
    for n in range(3):
        a = (k * 3 + n) * 2.2
        r = 0.15 + ((k + n) % 3) * 0.22
        cx, cy = 1.0 + math.cos(a) * r, 1.5 + math.sin(a) * r
        p.f(cx - 0.02, cy - 0.02, -0.5, cx + 0.02, cy + 0.02, 0.4, (176, 140, 90))
        p.f(cx - 0.06, cy - 0.005, -0.5, cx + 0.06, cy + 0.005, -0.32, (230, 230, 230) if n % 2 else (200, 60, 60))
        p.f(cx - 0.005, cy - 0.06, -0.5, cx + 0.005, cy + 0.06, -0.32, (230, 230, 230) if n % 2 else (200, 60, 60))
    p.poner(o, x, y, z, rot)
    o.put(int(x), y, int(z), COL_INV); o.put(int(x) + (1 if rot % 2 == 0 else 0), y, int(z) + (0 if rot % 2 == 0 else 1), COL_INV)


def carcaj_barril(o, x, y, z, k=0):
    """Barril con flechas (para el puesto de tiro)."""
    o.obj(128, x, y, z)
    for n in range(9):
        dx, dz = 0.25 + (n % 3) * 0.25, 0.25 + (n // 3) * 0.25
        h = 1.3 + 0.55 + ((n * 7 + k) % 3) * 0.06
        o.f(x + dx - 0.02, y + 1.0, z + dz - 0.02, x + dx + 0.02, y + h, z + dz + 0.02, (176, 140, 90))
        col = ((230, 230, 230), (200, 60, 60), (60, 110, 190))[n % 3]
        o.f(x + dx - 0.05, y + h - 0.2, z + dz - 0.005, x + dx + 0.05, y + h, z + dz + 0.005, col)
        o.f(x + dx - 0.005, y + h - 0.2, z + dz - 0.05, x + dx + 0.005, y + h, z + dz + 0.05, col)


def arco_colgado(o, cara, c, u, v):
    """Arco largo colgado de dos clavijas (en la cara interior del muro)."""
    g = M._pared(o, cara)
    for i in range(12):
        t = (i - 5.5) / 5.5
        du = 0.28 * (1 - t * t)
        g(u + du - 0.03, v + i * 0.16, u + du + 0.03, v + i * 0.16 + 0.16, 0.08, 0.13, M.MADC if 3 < i < 8 else M.MAD)
    g(u + 0.0, v + 0.86, u + 0.06, v + 1.06, 0.07, 0.14, M.CUERO)
    g(u - 0.01, v + 0.05, u + 0.01, v + 1.87, 0.095, 0.105, (230, 226, 210))
    for vv in (v + 0.4, v + 1.5):
        g(u + 0.15, vv, u + 0.22, vv + 0.07, 0.0, 0.2, M.MADO)


# ---------------------------------------------------------------- herreria
def fuelle(o, x, y, z):
    """Fuelle de cuero 1,25 x 1 (a lo largo de x, boquilla hacia -x), sobre un caballete."""
    for xx in (x + 0.1, x + 1.0):
        for zz in (z + 0.15, z + 0.75):
            o.f(xx, y, zz, xx + 0.1, y + 0.5, zz + 0.1, M.MADO)
    o.f(x + 0.1, y + 0.5, z + 0.1, x + 1.25, y + 0.5625, z + 0.9, M.MAD, 2)
    for i, (a, b) in enumerate(((0.15, 0.85), (0.1, 0.9), (0.15, 0.85))):
        o.f(x + 0.3, y + 0.5625 + i * 0.09, z + a, x + 1.2, y + 0.5625 + i * 0.09 + 0.09, z + b, M.CUERO if i % 2 else M.CUERO2)
    o.f(x + 0.1, y + 0.83, z + 0.1, x + 1.25, y + 0.89, z + 0.9, M.MAD, 2)
    o.f(x + 1.25, y + 0.85, z + 0.45, x + 1.6, y + 0.9, z + 0.55, M.MADO)
    o.f(x + 1.55, y + 0.8, z + 0.42, x + 1.62, y + 0.95, z + 0.58, M.MADO)
    o.f(x - 0.35, y + 0.6, z + 0.44, x + 0.3, y + 0.72, z + 0.56, M.HIE2)


def piedra_afilar(o, c, x, y, z):
    """Piedra de afilar (rueda vertical en un bastidor de madera, manivela y artesa con agua). Ocupa 2x1 a lo largo de x."""
    c.ocupa("piedra de afilar", x, z, x + 2, z + 1, y, y + 1.8)
    for xx in (x + 0.3, x + 1.55):
        o.f(xx, y, z + 0.1, xx + 0.15, y + 1.0, z + 0.25, M.MADO)
        o.f(xx, y, z + 0.75, xx + 0.15, y + 1.0, z + 0.9, M.MADO)
        o.f(xx, y + 1.0, z + 0.1, xx + 0.15, y + 1.1, z + 0.9, M.MAD)
    o.f(x + 0.3, y + 0.2, z + 0.25, x + 1.7, y + 0.6, z + 0.75, M.MAD, 2)
    o.f(x + 0.4, y + 0.6, z + 0.3, x + 1.6, y + 0.62, z + 0.7, (70, 110, 150))
    v = Vox(0.0625)
    for j in range(-9, 9):
        for i in range(-9, 9):
            d = math.hypot(i + 0.5, j + 0.5)
            if d < 9:
                v.set(i + 9, j + 9, 0, (150, 146, 140) if d > 1.6 else M.HIE2)
    for (x0, y0, z0, x1, y1, z1, col, g) in v.cajas():
        o.f(x + 0.4375 + x0, y + 0.55 + y0, z + 0.44, x + 0.4375 + x1, y + 0.55 + y1, z + 0.56, col)
    o.f(x + 0.3, y + 1.08, z + 0.47, x + 1.85, y + 1.14, z + 0.53, M.HIE2)
    o.f(x + 1.85, y + 0.9, z + 0.47, x + 1.91, y + 1.14, z + 0.53, M.HIE2)
    o.f(x + 1.85, y + 0.85, z + 0.4, x + 1.91, y + 0.92, z + 0.6, M.MADC)
    o.put(int(x), y, int(z), COL_INV); o.put(int(x) + 1, y, int(z), COL_INV)


def tina_temple(o, c, x, y, z):
    """Tina de temple: medio barril con agua y una hoja enfriandose."""
    c.ocupa("tina de temple", x, z, x + 1, z + 1, y, y + 0.9, False)
    v = Vox(0.125)
    perf = [3.4, 3.7, 3.85, 3.9, 3.9, 3.9, 3.9]

    def col(a, t, b):
        if t == 6 and not b:
            return (70, 120, 170)
        if t in (1, 5) and b:
            return M.HIE2
        return M.MAD if int((a + math.pi) * 14 / (2 * math.pi)) % 2 else (126, 84, 50)
    torno(v, 4.0, 4.0, 0, perf, col)
    v.poner(o, x, y, z, 2)
    o.f(x + 0.45, y + 0.82, z + 0.3, x + 0.5, y + 1.4, z + 0.36, M.ACERO)
    o.f(x + 0.38, y + 1.4, z + 0.28, x + 0.57, y + 1.45, z + 0.38, M.HIE2)
    o.f(x + 0.6, y + 0.875, z + 0.55, x + 0.75, y + 0.89, z + 0.7, (230, 236, 240))
    o.put(int(x), y, int(z), COL_INV)


def carbonera(o, c, x, y, z):
    """Cajon de madera 1,5 x 1 lleno de carbon (montoncito en rejilla) con una pala."""
    c.ocupa("carbonera", x, z, x + 1.5, z + 1, y, y + 1.1, False)
    o.f(x, y, z, x + 1.5, y + 0.0625, z + 1, M.MADO)
    for (a, b, c2, d) in ((0, 1.5, 0, 0.0625), (0, 1.5, 0.9375, 1), (0, 0.0625, 0, 1), (1.4375, 1.5, 0, 1)):
        o.f(x + a, y, z + c2, x + b, y + 0.6, z + d, M.MAD, 2)
    v = Vox(0.125)
    for i in range(11):
        for k in range(7):
            h = 3 + int(2.2 * math.sin((i + 0.5) / 11 * math.pi) * math.sin((k + 0.5) / 7 * math.pi)) + (_h(i, k) % 2)
            for j in range(h):
                v.set(i, j, k, (30, 30, 34) if (_h(i, j, k) % 3) else (52, 52, 58))
    v.poner(o, x + 0.0625, y + 0.0625, z + 0.0625)
    o.f(x + 1.1, y + 0.6, z + 0.45, x + 1.16, y + 1.4, z + 0.51, M.MADC)
    o.f(x + 1.02, y + 0.5, z + 0.36, x + 1.24, y + 0.6, z + 0.6, M.HIE2)


def lingotes(o, x, y, z):
    for i in range(3):
        for j in range(3 - i):
            xx = x + 0.08 + j * 0.28 + i * 0.14
            o.f(xx, y + i * 0.1, z + 0.1, xx + 0.24, y + i * 0.1 + 0.1, z + 0.5, (170, 120, 90) if (i + j) % 2 else (150, 154, 166))


def herreria():
    W, D = 22, 18
    o = Obra("cw_herreria", W, 26, D,
             "Herreria semiabierta (progreso: forjar y mejorar armas). Frente y lado este abiertos con pilares; fragua de piedra "
             "con brasas, campana y chimenea, fuelle de cuero, yunque sobre tocon con martillo, tina de temple, piedra de afilar, "
             "carbonera, lingotes, tabla de herramientas (martillos, tenazas, lima, atizador, herraduras) y armero. Cartel con yunque "
             "colgado del pilar de la entrada.",
             entry=(10, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    c = Casa(o, 3, 4, 18, 13, teja="techo_oscuro")      # interior x 4..17, z 5..12
    s = c.suelos[0]
    c.abrir("n", 1, 15, 0, cada=5)
    c.abrir("e", 1, 9, 0, cada=4)
    c.cartel_colgante("n", 1.5, s + 3, "yunque")
    # fragua contra el fondo oeste
    o.mbox(4, s, 11, 6, s, 12, "chimenea")
    o.f(3.9, s + 1, 10.85, 7.1, s + 1.25, 13, PIEDRA_F)
    for i in range(12):
        xx, zz = 4.2 + (i % 4) * 0.65, 11.1 + (i // 4) * 0.55
        o.f(xx, s + 1.25, zz, xx + 0.45, s + 1.35 + (i % 3) * 0.05, zz + 0.4, (255, 120 + (i % 3) * 40, 40), 0, 1)
    o.f(4.6, s + 1.4, 11.6, 6.2, s + 1.45, 11.7, (255, 210, 120), 0, 1)        # barra al rojo
    o.f(6.2, s + 1.35, 11.6, 7.4, s + 1.43, 11.7, M.HIE2)
    o.f(3.8, s + 2.6, 10.3, 7.2, s + 2.85, 13, PIEDRA_F)                       # campana
    o.f(4.0, s + 2.85, 10.6, 7.0, s + 3.0, 13, (140, 136, 128))
    for y in range(s + 3, c.cumbre + 2):
        o.mbox(4, y, 11, 6, y, 12, "chimenea")
    o.f(3.8, c.cumbre + 2, 10.8, 7.2, c.cumbre + 2.22, 13.2, PIEDRA_F)
    o.f(4.4, c.cumbre + 2.22, 11.4, 6.6, c.cumbre + 2.26, 12.6, (30, 26, 24))
    for xx in (3.9, 6.95):
        o.f(xx, s + 1.25, 10.85, xx + 0.15, s + 2.6, 11.0, (120, 116, 110))
    c.fuegos.append((5.5, 11.8, s, 2.5))
    c.reservar(4, 8.6, 7, 10.8, s, s + 2, "paso", "frente de la fragua")
    c.ocupa("fuelle", 7.2, 11.0, 9.0, 12.6, s, s + 1.0, False)
    fuelle(o, 7.5, s, 11.2)
    c.mueble(135, 8, s, 7.5, 0, "yunque")
    o.f(8.9, s + 1.075, 7.62, 9.55, s + 1.14, 7.68, M.MADC)
    o.f(9.55, s + 1.06, 7.55, 9.75, s + 1.2, 7.75, M.HIE2)
    lingotes(o, 10.2, s, 7.6); c.ocupa("lingotes", 10.2, 7.6, 11.1, 8.2, s, s + 0.3, False)
    tina_temple(o, c, 10.4, s, 11.6)
    piedra_afilar(o, c, 13, s, 11.6)
    carbonera(o, c, 4.2, s, 5.4)
    g = M.panel_herramientas(o, c.caras["s"], 9.6, 13.6, s + 2.2)
    M.martillo(g, 10.0, s + 2.35); M.martillo(g, 10.45, s + 2.4)
    M.tenazas(g, 11.0, s + 2.25); M.tenazas(g, 11.45, s + 2.3)
    M.lima(g, 11.95, s + 2.4); M.atizador(g, 12.4, s + 2.1)
    M.herradura(g, 13.05, s + 3.0); M.herradura(g, 13.05, s + 2.55)
    armero(o, 14, s, 5.2, 2)
    c.ocupa("armero", 14, 5.2, 17, 6.2, s, s + 2.7)
    c.farol_pared("o", 3.0, s + 3.5)
    return o


# ---------------------------------------------------------------- carpinteria
def virutas(o, x, y, z, ni=6, nk=5, seed=0):
    v = Vox(0.125)
    for i in range(ni):
        for k in range(nk):
            h = int(2.2 * math.sin((i + 0.5) / ni * math.pi) * math.sin((k + 0.5) / nk * math.pi) + (_h(seed, i, k) % 2) * 0.6)
            for j in range(h):
                v.set(i, j, k, ((232, 206, 150), (220, 188, 128), (240, 220, 170))[_h(seed, i, j, k) % 3])
    for (x0, y0, z0, x1, y1, z1, col, g) in v.cajas():
        o.f(x + x0, y + y0 * 0.5, z + z0, x + x1, y + y1 * 0.5, z + z1, col)


def banco_carpintero(o, c, x0, z0, y, largo=4):
    """Banco de carpintero (a lo largo de x, contra un muro en +z): tapa gruesa de tablones, patas con travesanos,
    tornillo de banco con husillo, topes, cajon y herramientas encima (cepillo, formon, mazo, regla)."""
    c.ocupa("banco de carpintero", x0, z0, x0 + largo, z0 + 1, y, y + 1.4)
    for i in range(3):
        o.f(x0, y + 1.0, z0 + i * 0.333 + 0.01, x0 + largo, y + 1.25, z0 + i * 0.333 + 0.323, M.MADCC if i % 2 else M.MADC, 2)
    for xx in (x0 + 0.15, x0 + largo - 0.35):
        for zz in (z0 + 0.1, z0 + 0.7):
            o.f(xx, y, zz, xx + 0.2, y + 1.0, zz + 0.2, M.MADO)
        o.f(xx, y + 0.25, z0 + 0.3, xx + 0.2, y + 0.37, z0 + 0.7, M.MADO)
    o.f(x0 + 0.35, y + 0.25, z0 + 0.45, x0 + largo - 0.35, y + 0.37, z0 + 0.55, M.MADO)
    o.f(x0 + 0.4, y + 0.37, z0 + 0.15, x0 + largo - 0.4, y + 0.42, z0 + 0.85, M.MAD, 2)          # repisa baja
    for i in range(4):
        o.f(x0 + 0.6 + i * 0.7, y + 0.42, z0 + 0.3, x0 + 1.2 + i * 0.7, y + 0.55, z0 + 0.7, (176, 126, 76), 2)
    o.f(x0 - 0.12, y + 0.7, z0 + 0.25, x0, y + 1.25, z0 + 0.75, M.MAD, 2)                          # tornillo
    o.f(x0 - 0.3, y + 0.92, z0 + 0.47, x0 - 0.12, y + 1.0, z0 + 0.53, M.HIE2)
    o.f(x0 - 0.33, y + 0.85, z0 + 0.35, x0 - 0.3, y + 1.07, z0 + 0.65, M.MADO)
    for xx in (x0 + 1.5, x0 + 2.8):
        o.f(xx, y + 1.25, z0 + 0.1, xx + 0.1, y + 1.33, z0 + 0.2, M.MADO)
    o.f(x0 + 0.6, y + 1.25, z0 + 0.35, x0 + 1.1, y + 1.4, z0 + 0.6, M.MAD)                          # cepillo
    o.f(x0 + 0.68, y + 1.4, z0 + 0.42, x0 + 0.82, y + 1.5, z0 + 0.53, M.MADC)
    o.f(x0 + 0.95, y + 1.4, z0 + 0.43, x0 + 1.0, y + 1.47, z0 + 0.52, M.ACERO)
    o.f(x0 + 1.8, y + 1.25, z0 + 0.5, x0 + 2.25, y + 1.3, z0 + 0.56, M.ACERO)                        # formon
    o.f(x0 + 2.25, y + 1.25, z0 + 0.49, x0 + 2.5, y + 1.32, z0 + 0.57, M.MADC)
    o.f(x0 + 2.7, y + 1.25, z0 + 0.3, x0 + 2.8, y + 1.33, z0 + 0.8, M.MADC)                          # mazo
    o.f(x0 + 2.62, y + 1.25, z0 + 0.15, x0 + 2.88, y + 1.45, z0 + 0.32, M.MAD)
    o.f(x0 + 3.0, y + 1.25, z0 + 0.12, x0 + 3.9, y + 1.27, z0 + 0.2, (220, 200, 140))                # regla
    o.box(int(x0), y, int(z0), int(x0 + largo) - 1, y, int(z0), COL_INV)


def caballetes_tronco(o, c, x0, z0, y):
    """Dos caballetes en A con un tronco descortezado a medias y un serrucho clavado en el corte."""
    c.ocupa("caballetes con tronco", x0, z0, x0 + 3.5, z0 + 1, y, y + 1.6)
    for xx in (x0 + 0.3, x0 + 2.8):
        o.f(xx, y + 0.8, z0 + 0.05, xx + 0.4, y + 0.95, z0 + 0.95, M.MAD)
        for zz in (z0 + 0.1, z0 + 0.75):
            o.f(xx + 0.13, y, zz, xx + 0.27, y + 0.8, zz + 0.15, M.MADO)
        o.f(xx + 0.15, y + 0.3, z0 + 0.25, xx + 0.25, y + 0.4, z0 + 0.75, M.MADO)
    o.f(x0, y + 0.95, z0 + 0.2, x0 + 3.5, y + 1.5, z0 + 0.8, (104, 72, 44))
    o.f(x0 + 1.6, y + 0.97, z0 + 0.18, x0 + 3.5, y + 1.52, z0 + 0.82, (196, 160, 112))
    o.f(x0 - 0.02, y + 1.0, z0 + 0.25, x0, y + 1.45, z0 + 0.75, (210, 176, 128))
    o.f(x0 - 0.03, y + 1.15, z0 + 0.4, x0 - 0.02, y + 1.3, z0 + 0.6, (176, 136, 90))
    o.f(x0 + 2.45, y + 1.3, z0 + 0.47, x0 + 2.5, y + 1.95, z0 + 0.53, M.ACERO)
    o.f(x0 + 2.45, y + 1.95, z0 + 0.4, x0 + 2.5, y + 2.15, z0 + 0.6, M.MADC)
    o.put(int(x0), y, int(z0), COL_INV); o.put(int(x0) + 3, y, int(z0), COL_INV)


def tablas_de_pie(o, c, x0, z0, y, n=7):
    """Tablas y listones de pie contra el muro (+z), de distintas alturas y tonos."""
    c.ocupa("tablas de pie", x0, z0, x0 + n * 0.3 + 0.2, z0 + 0.6, y, y + 3.2)
    o.f(x0, y + 2.4, z0 + 0.45, x0 + n * 0.3 + 0.2, y + 2.5, z0 + 0.55, M.MADO)
    for i in range(n):
        h = 2.2 + (_h(i, 3) % 5) * 0.2
        w = 0.22 if i % 3 else 0.12
        col = ((176, 126, 76), (160, 112, 66), (190, 140, 90))[i % 3]
        o.f(x0 + 0.1 + i * 0.3, y, z0 + 0.1 + (i % 2) * 0.08, x0 + 0.1 + i * 0.3 + w, y + h, z0 + 0.4 + (i % 2) * 0.08, col, 2)


def silla_a_medias(o, x, y, z):
    """Silla sin terminar (asiento y dos patas puestas, el respaldo apoyado en el suelo)."""
    o.f(x + 0.125, y + 0.625, z + 0.125, x + 0.875, y + 0.75, z + 0.875, M.MADCC, 2)
    for (xx, zz) in ((0.125, 0.125), (0.75, 0.75)):
        o.f(x + xx, y, z + zz, x + xx + 0.125, y + 0.625, z + zz + 0.125, M.MAD)
    o.f(x + 0.4, y + 0.3, z + 0.4, x + 0.55, y + 0.625, z + 0.55, M.MADO)
    o.f(x + 1.1, y, z + 0.2, x + 1.9, y + 0.12, z + 0.9, M.MAD)
    for xx in (1.2, 1.45, 1.7):
        o.f(x + xx, y + 0.12, z + 0.3, x + xx + 0.08, y + 0.16, z + 0.8, M.MADC)


def barril_en_obra(o, x, y, z):
    """Barril a medio armar: aro de hierro, la mitad de las duelas puestas y otras apoyadas al lado."""
    v = Vox(0.125)
    for j in range(10):
        for i in range(8):
            for k in range(8):
                d = math.hypot(i - 3.5, k - 3.5)
                if 2.9 <= d < 3.9:
                    a = math.atan2(k - 3.5, i - 3.5)
                    if a < 0.6 or j in (1, 8):
                        v.set(i, j, k, M.HIE2 if j in (1, 8) else (M.MAD if int(a * 3) % 2 else (126, 84, 50)))
    v.poner(o, x, y, z, 2)
    for i in range(3):
        o.f(x + 1.1 + i * 0.16, y, z + 0.1, x + 1.22 + i * 0.16, y + 1.1 - i * 0.1, z + 0.35, (150, 100, 60))


def carpinteria():
    W, D = 22, 18
    o = Obra("cw_carpinteria", W, 26, D,
             "Carpinteria semiabierta (progreso: muebles, arcos, mejoras de casa). Frente abierto con pilares; banco de carpintero "
             "con tornillo y herramientas, caballetes con tronco a medio descortezar, tablas de pie, pilas de tablones, silla y barril "
             "a medio armar, virutas, tabla de herramientas (serrucho, escuadra, formones, martillo, hacha), troncos afuera. "
             "Cartel con sierra colgado del pilar de la entrada.",
             entry=(10, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    c = Casa(o, 3, 4, 18, 13, muro="muro_ocre", teja="techo_rojo")       # interior x 4..17, z 5..12
    s = c.suelos[0]
    c.abrir("n", 1, 15, 0, cada=5)
    c.ventana("e", 3); c.ventana("o", 5)
    c.cartel_colgante("n", 1.5, s + 3, "sierra")
    banco_carpintero(o, c, 5, 11.6, s, 4)
    virutas(o, 6.0, s, 10.6, 8, 5, 1)
    g = M.panel_herramientas(o, c.caras["s"], 1.6, 5.0, s + 2.3)
    M.sierra(g, 1.8, s + 2.9); M.escuadra(g, 2.8, s + 2.45)
    M.formon(g, 3.4, s + 2.5); M.formon(g, 3.65, s + 2.55); M.martillo(g, 4.1, s + 2.4); M.hacha(g, 4.6, s + 2.35)
    caballetes_tronco(o, c, 10.5, 8.2, s)
    virutas(o, 11.5, s, 9.3, 6, 4, 2)
    tablas_de_pie(o, c, 10.4, 12.3, s, 8)
    c.mueble(161, 14.6, s, 11.9, 0, "pila de lena")
    silla_a_medias(o, 14.4, s, 6.0); c.ocupa("silla a medias", 14.4, 6.0, 16.4, 7.0, s, s + 0.8)
    barril_en_obra(o, 4.4, s, 7.2); c.ocupa("barril a medias", 4.4, 7.2, 6.0, 8.2, s, s + 1.3)
    c.mueble(122, 15.8, s, 9, 3, "caja de herramientas")
    for (xx, zz) in ((20.1, 6), (20.9, 6), (20.5, 6.6)):        # troncos afuera, apilados contra el muro este
        yy = 1 if xx != 20.5 else 1.6
        o.f(xx, yy, zz, xx + 0.6, yy + 0.6, zz + 2.6, (104, 72, 44))
        o.f(xx + 0.05, yy + 0.05, zz - 0.02, xx + 0.55, yy + 0.55, zz, (200, 166, 116))
        o.f(xx + 0.2, yy + 0.2, zz - 0.03, xx + 0.4, yy + 0.4, zz - 0.02, (170, 130, 86))
    c.farol_pared("e", 7.0, s + 3.5); c.farol_pared("o", 7.6, s + 3.5)
    return o


# ---------------------------------------------------------------- pabellon de entrenamiento (cuerpo a cuerpo)
def pabellon_entrenamiento():
    W, D = 28, 24
    o = Obra("cw_pabellon_entrenamiento", W, 20, D,
             "Pabellon de entrenamiento cuerpo a cuerpo. Plataforma con suelo de losas grandes de dos tonos y ruedo central de arena "
             "con bordillo de madera; 10 columnas de piedra con capitel, arquitrabe y techo escalonado, estandartes entre columnas. "
             "Seis munecos de practica (con casco o escudo), dos armeros, banco y barril de agua. La punteria va en cw_campo_tiro.",
             entry=(13, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    o.mbox(2, 1, 3, 25, 2, 20, "zocalo")
    o.mbox(10, 1, 2, 17, 1, 2, "piedra")
    y = 3
    cxr, czr, R = 14.0, 11.5, 4.6
    for i in range(3, 25, 2):
        for k in range(4, 20, 2):
            d = math.hypot(i + 1 - cxr, k + 1 - czr)
            if d < R - 0.2:
                continue
            t = _h(i // 2, k // 2) % 3
            col = ((176, 170, 156), (160, 154, 140), (188, 182, 168))[t]
            o.f(i + 0.03, y - 0.06, k + 0.03, i + 1.97, y, k + 1.97, col)
    v = Vox(0.25)
    for i in range(-20, 20):
        for k in range(-20, 20):
            d = math.hypot((i + 0.5) * 0.25, (k + 0.5) * 0.25)
            if d < R - 0.25:
                v.set(i, 0, k, ((214, 190, 140), (204, 180, 130), (222, 200, 150))[_h(i, k) % 3])
            elif d < R + 0.25:
                v.set(i, 0, k, M.MADO); v.set(i, 1, k, M.MAD)
    for (x0, y0, z0, x1, y1, z1, col, g) in v.cajas():
        o.f(cxr + x0, y - 0.06 + y0 * 0.5, czr + z0, cxr + x1, y - 0.06 + y1 * 0.5, czr + z1, col)
    cols = [(3, 4), (9, 4), (17, 4), (23, 4), (3, 18), (9, 18), (17, 18), (23, 18), (3, 11), (23, 11)]
    for (cx, cz) in cols:
        o.mbox(cx, y, cz, cx + 1, y + 6, cz + 1, "pilar")
        o.f(cx - 0.2, y, cz - 0.2, cx + 2.2, y + 0.3, cz + 2.2, PIEDRA_F)
        o.f(cx - 0.12, y + 0.3, cz - 0.12, cx + 2.12, y + 0.42, cz + 2.12, (164, 160, 150))
        o.f(cx - 0.25, y + 6.6, cz - 0.25, cx + 2.25, y + 7.0, cz + 2.25, PIEDRA_F)
        o.f(cx - 0.12, y + 6.45, cz - 0.12, cx + 2.12, y + 6.6, cz + 2.12, (164, 160, 150))
    yt = y + 7
    o.f(2.8, yt, 3.8, 25.2, yt + 0.8, 6.2, M.MADO, 2)
    o.f(2.8, yt, 17.8, 25.2, yt + 0.8, 20.2, M.MADO, 2)
    o.f(2.8, yt, 6.2, 5.2, yt + 0.8, 17.8, M.MADO, 2)
    o.f(22.8, yt, 6.2, 25.2, yt + 0.8, 17.8, M.MADO, 2)
    for xx in range(7, 23, 4):
        o.f(xx, yt + 0.2, 6.2, xx + 0.6, yt + 0.8, 17.8, M.MAD, 2)
    yr = yt + 1
    o.f(5.2, yr - 0.03, 6.2, 22.8, yr, 17.8, (110, 76, 50), 2)
    for k, (a0, a1, b0, b1) in enumerate(((2, 25, 3, 20), (4, 23, 5, 18), (6, 21, 7, 16), (8, 19, 9, 14))):
        o.mbox(a0, yr + k, b0, a1, yr + k, b1, "techo")
    for xa in (5.4, 19.4):          # estandartes en el frente, entre columnas
        o.f(xa, yt - 0.1, 3.82, xa + 3.2, yt, 3.9, M.MADO)
        o.f(xa + 0.3, yt - 3.2, 3.84, xa + 2.9, yt - 0.1, 3.88, (130, 34, 44))
        o.f(xa + 0.3, yt - 3.6, 3.84, xa + 1.5, yt - 3.2, 3.88, (130, 34, 44))
        o.f(xa + 1.7, yt - 3.6, 3.84, xa + 2.9, yt - 3.2, 3.88, (130, 34, 44))
        o.f(xa + 0.9, yt - 2.4, 3.8, xa + 2.3, yt - 1.0, 3.84, M.ORO)
        o.f(xa + 1.45, yt - 2.6, 3.79, xa + 1.75, yt - 0.8, 3.8, (230, 232, 240))
        o.f(xa + 1.1, yt - 1.4, 3.79, xa + 2.1, yt - 1.25, 3.8, (230, 232, 240))
    for n, (mx, mz) in enumerate(((7, 8.5), (7, 14), (20, 8.5), (20, 14), (11.5, 17.2), (16, 17.2))):
        rot = 3 if mx < 10 else (1 if mx > 18 else 0)
        o.f(mx - 0.4, y, mz - 0.4, mx + 1.4, y + 0.04, mz + 1.4, PAJA2)
        muneco(o, mx, y, mz, rot, casco=(n % 3 == 0), escudo=(n % 3 == 1), k=n)
    armero(o, 5.5, y, 18.3, 2)
    armero(o, 19.5, y, 18.3, 2)
    o.obj(125, 12.5, y, 5.0, 0)
    o.obj(128, 18.0, y, 5.0)
    o.f(18.2, y + 1.32, 5.2, 18.8, y + 1.34, 5.8, (70, 120, 170))
    o.f(18.6, y + 1.3, 5.3, 18.75, y + 1.5, 5.45, M.MADC)
    for (fx, fz) in ((8.0, 11.5), (19.9, 11.5)):
        o.f(fx - 0.02, yt - 1.4, fz - 0.02, fx + 0.02, yt, fz + 0.02, HIERRO2)
        farol(o, fx, yt - 2.55, fz, 1.0)
    for (px, pz) in ((1, 1), (25, 1)):
        farola(o, px, 1, pz)
    return o


# ---------------------------------------------------------------- campo de tiro
def campo_tiro():
    W, D = 36, 36
    o = Obra("cw_campo_tiro", W, 14, D,
             "Campo de tiro con arco (punteria, separado del pabellon cuerpo a cuerpo). Puesto de tiro techado de madera con "
             "barandilla, barriles con flechas, arcos colgados y banco; cuatro calles separadas por cuerdas con postes, una diana "
             "por calle a 10, 14, 18 y 22 bloques, fardos de paja detras como parapeto y banderines de distancia.",
             entry=(18, 0, "norte"))
    for x in range(W):
        for z in range(D):
            o.mat(x, 0, z, "pasto" if _h(x, z) % 5 else "pasto_os")
    # puesto de tiro: tarima, postes, techo, baranda delantera
    o.mbox(4, 1, 2, 31, 1, 6, "madera")
    o.mbox(15, 1, 0, 20, 1, 1, "piedra")
    for xx in (4, 13, 22, 31):
        for zz in (2, 6):
            o.f(xx + 0.3, 2, zz + 0.3, xx + 0.7, 6.4, zz + 0.7, M.MADO, 2)
            o.put(xx, 2, zz, COL_INV); o.put(xx, 3, zz, COL_INV)
    o.f(4.2, 6.4, 2.3, 31.8, 6.7, 2.7, M.MADO, 2); o.f(4.2, 6.4, 6.3, 31.8, 6.7, 6.7, M.MADO, 2)
    for k, (a0, a1, b0, b1) in enumerate(((3, 32, 1, 7), (3, 32, 3, 5))):
        o.mbox(a0, 7 + k, b0, a1, 7 + k, b1, "techo")
    baranda(o, 4.0, 32.0, 6.74, 2, "x", H=1.0)
    # calles
    centros = [8.5, 14.5, 21.5, 27.5]
    for xs in (11.5, 18, 24.5):
        for zz in range(8, 33, 4):
            o.f(xs - 0.07, 0.95, zz - 0.07, xs + 0.07, 2.0, zz + 0.07, M.MADO)
        o.f(xs - 0.02, 1.85, 8, xs + 0.02, 1.9, 32, (210, 190, 140))
    dist = [10, 14, 18, 22]
    for n, (cx, dd) in enumerate(zip(centros, dist)):
        z = 7 + dd
        diana(o, cx - 1, 1, z, 0, n)
        for i in range(3):
            M.fardo(o, cx - 2.25 + i * 1.5, 1, z + 1.4, 0, n * 3 + i)
        M.fardo(o, cx - 1.5, 1.75, z + 1.4, 0, n * 3 + 7)
        # banderin de distancia
        o.f(cx + 1.8, 1, 13, cx + 1.9, 3.2, 13.1, M.MADO)
        o.f(cx + 1.9, 2.7, 13.04, cx + 2.5, 3.1, 13.07, ((200, 50, 50), (60, 110, 190), (230, 190, 60), (90, 170, 80))[n])
    # en la tarima
    carcaj_barril(o, 5.2, 2, 3.0, 1)
    carcaj_barril(o, 29.8, 2, 3.0, 2)
    o.obj(125, 16.5, 2, 2.2, 2)
    for xa in (9.5, 25.5):     # arcos en un tablero de pie
        o.f(xa, 2, 2.15, xa + 2.0, 4.6, 2.3, M.MAD, 2)
        for i, xx in enumerate((xa + 0.5, xa + 1.3)):
            for j in range(12):
                t = (j - 5.5) / 5.5
                du = 0.25 * (1 - t * t)
                o.f(xx + du - 0.03, 2.4 + j * 0.16, 2.3, xx + du + 0.03, 2.56 + j * 0.16, 2.36, M.MADC if 3 < j < 8 else M.MAD)
            o.f(xx - 0.01, 2.45, 2.3, xx + 0.01, 4.27, 2.31, (230, 226, 210))
    for (fx, fz) in ((13.5, 6.5), (22.5, 6.5)):
        o.f(fx - 0.03, 5.3, fz - 0.03, fx + 0.03, 6.4, fz + 0.03, HIERRO2)
        farol(o, fx, 4.15, fz, 1.0)
    return o


# ---------------------------------------------------------------- casas en hilera (techos a dos aguas, cocinas)
def casas_hilera():
    W, D = 45, 19
    o = Obra("cw_casas_hilera", W, 32, D,
             "Tres casas en hilera con muro compartido y techo a dos aguas (cumbrera paralela a la calle): ocre de 2 plantas con "
             "cocina de hogar (olla colgada, encimera, repisa de platos, ollas, ristras) y dormitorio arriba; rosa de 2 plantas mas alta "
             "con cocina de hierro y cuarto de ninos; una de 1 planta con hogar-cocina y cama. Hastiales de muro, sillares solo donde "
             "la casa queda a la vista, cornisas a distinta altura.",
             entry=(9, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    # C: 1 planta (x 29..42) -- primero las bajas
    C = Casa(o, 29, 4, 42, 15, pisos=1, muro="muro", teja="techo", techo_tipo="dos", alero_o=False, alero_e=True,
             esquinas=["ne", "se"], cornisa=False)
    # A: ocre 2 plantas (x 2..15)
    A = Casa(o, 2, 4, 15, 15, pisos=2, h=7, muro="muro_ocre", teja="techo", techo_tipo="dos", alero_o=True, alero_e=False,
             esquinas=["no", "so"], cornisa=["n", "s", "o"])
    # B: rosa 2 plantas mas alta (x 15..29), la ultima: sus muros compartidos suben por encima de las vecinas
    B = Casa(o, 15, 4, 29, 15, pisos=2, h=8, muro="muro_rosa", teja="techo_rojo", techo_tipo="dos", alero_o=False, alero_e=False,
             esquinas={"no": A.cumbre + 1, "so": A.cumbre + 1, "ne": C.cumbre + 1, "se": C.cumbre + 1}, cornisa=["n", "s"])
    for c in (A, B, C):
        o.mbox(c.x0 + 1, 1, c.z0 + 1, c.x1 - 1, 2, c.z1 - 1, "piso")
    # ---- A: cocina de hogar abajo, dormitorio arriba
    s, s2 = A.suelos
    A.puerta("n", 6)                                     # x 8..9
    A.ventana("n", 1); A.ventana("n", 11)
    A.ventana("n", 1, 1); A.ventana("n", 11, 1)
    A.ventana("s", 3, 1); A.ventana("s", 9, 1)
    A.ventana("o", 2, 1)
    A.chimenea("o", 6, olla=True)                        # hogar en z 10..11
    A.farol_pared("n", 4.4, s + 1, interior=False); A.farol_pared("n", 9.6, s + 1, interior=False)
    A.enredadera("o", 8.6, s - 1, s2 + 5, 2.0)
    escalera(A, 6, 13, 14, 0, 1)                         # x 6..13 por el fondo
    _encimera_rot(o, 13, s, 5, 3, 3, A, "encimera")
    _repisa_e(o, A, 2.2, s + 2.6, 2.4)
    M.ollas_colgadas(o, A.caras["e"], 4.8, s + 3.6, 2)
    M.ristra(o, A.caras["n"], 4.6, s + 3.4); M.ristra(o, A.caras["n"], 5.0, s + 3.3, (200, 120, 80))
    A.mueble(124, 7, s, 10, 0, "mesa de cocina")
    A.mueble(131, 7, s, 9, 2, "silla"); A.mueble(131, 8, s, 9, 2, "silla")
    A.mueble(131, 7, s, 11, 0, "silla"); A.mueble(131, 8, s, 11, 0, "silla")
    A.mueble(128, 3, s, 5, 0, "barril"); A.mueble(129, 4, s, 5, 0, "saco"); A.mueble(129, 3, s, 6.1, 0, "saco")
    A.farol_pared("e", 6.5, s + 3.5)
    A.alfombra(5.5, 6, 10.5, 11.5, 1, AZUL, CELESTE, 0.5)
    A.cama_con_cofre(3.5, s2, 5, 2)
    A.mueble(133, 14, s2, 6, 3, "armario")
    A.farol_pared("o", 5.0, s2 + 3.5)
    # ---- B: cocina de hierro abajo, cuarto de ninos arriba
    s, s2 = B.suelos
    B.puerta("n", 6)                                     # x 21..22
    for p in (0, 1):
        B.ventana("n", 1, p); B.ventana("n", 11, p)
    B.ventana("n", 6, 1)
    B.ventana("s", 6, 1)
    B.farol_pared("n", 4.4, s + 1, interior=False); B.farol_pared("n", 9.6, s + 1, interior=False)
    escalera(B, 18, 13, 14, 0, 1)                        # x 18..26
    _fogon_e(o, B, 27, s, 6)
    _encimera_rot(o, 27, s, 9, 3, 3, B, "encimera")
    B.mueble(124, 21, s, 10, 0, "mesa"); B.mueble(131, 21, s, 9, 2, "silla"); B.mueble(131, 22, s, 11, 0, "silla")
    B.mueble(127, 16, s, 7, 1, "estanteria de despensa")
    _repisa_e(o, B, 4.6, s + 3.0, 2.2)
    B.alfombra(20, 6, 25, 10.5, 1, ROJO, ORO, 0.5)
    B.cama_con_cofre(16.5, s2, 5, 2)
    B.cama_con_cofre(26.0, s2, 5, 2)
    B.mueble(127, 16, s2, 10, 1, "estanteria")
    B.farol_pared("s", 3.0, s2 + 3.6)
    # ---- C: una planta: hogar-cocina y cama
    s = C.suelos[0]
    C.puerta("n", 6)                                     # x 35..36
    C.ventana("n", 1); C.ventana("n", 11)
    C.ventana("s", 6)
    C.chimenea("e", 5, olla=True)                        # z 9..10
    C.farol_pared("n", 4.4, s + 1, interior=False); C.farol_pared("n", 9.6, s + 1, interior=False)
    C.enredadera("s", 10.5, s - 1, C.roof_y - 0.3, 2.0)
    C.cama_con_cofre(30.5, s, 10, 0)
    C.mueble(124, 34, s, 9, 0, "mesa"); C.mueble(131, 34.5, s, 8, 2, "silla"); C.mueble(131, 34.5, s, 10, 0, "silla")
    _encimera_rot(o, 36, s, 14, 3, 2, C, "encimera")
    C.mueble(128, 41, s, 13, 0, "barril")
    C.farol_pared("o", 2.5, s + 3.5)
    afuera(B, "banco", 16.0, 1.4, 19.0, 2.4, 1, 2, 125, 16.0, 1, 1.4)
    return o


def _cara_int(c, cara):
    return c.caras[cara]


def _encimera_rot(o, x, y, z, largo, rot, casa, nombre):
    """Encimera girada: rot 0 frente -Z, 2 frente +Z, 1 frente +X, 3 frente -X. (x, z) = esquina minima de la huella."""
    w, d = (largo, 1) if rot % 2 == 0 else (1, largo)
    casa.ocupa(nombre, x, z, x + w, z + d, y, y + 1.3)
    p = Pieza(largo, 1)
    tmp = _Captura()
    M.encimera(tmp, 0, 0, 0, largo)
    for b in tmp.cajas:
        p.f(*b)
    p.poner(o, x, y, z, rot)
    for i in range(w):
        for k in range(d):
            o.put(int(x) + i, y, int(z) + k, COL_INV)


class _Captura:
    """Obra falsa que junta cajas (para girar piezas armadas con o.f)."""
    def __init__(self):
        self.cajas = []

    def f(self, x0, y0, z0, x1, y1, z1, col, pat=0, glow=0):
        self.cajas.append((x0, y0, z0, x1, y1, z1, col, pat, glow))

    def box(self, *a):
        pass

    def put(self, *a):
        pass


def _fogon_e(o, casa, x, y, z):
    """Cocina de hierro contra el muro este (frente -X)."""
    casa.ocupa("cocina de hierro", x, z, x + 1, z + 2, y, y + 1.3, False)
    tmp = _Captura()
    M.fogon(tmp, 0, 0, 0)
    p = Pieza(2, 1)
    for b in tmp.cajas:
        p.f(*b)
    p.poner(o, x, y, z, 3)
    o.put(int(x), y, int(z), COL_INV); o.put(int(x), y, int(z) + 1, COL_INV)
    casa.fuegos.append((x + 0.5, z + 1.0, y, 1.2))


def _repisa_e(o, casa, u, v, largo):
    M.repisa_platos(o, casa.caras["e"], u, v, largo)
    x0, z0, x1, z1 = casa.rect("e", u, -1.0, u + largo, -1.5)
    casa.ocupa("repisa", x0, z0, x1, z1, v - 0.4, v + 0.5, True)


# ---------------------------------------------------------------- torre de vigia / campanario (simetrica, escalas de mano)
def torre_vigia():
    W, D = 14, 14
    o = Obra("cw_torre_vigia", W, 40, D,
             "Torre de vigia / campanario de 3 plantas (8x8), simetrica: puerta y ventanas de 2 centradas en cada cara, "
             "escaleras de mano abiertas con baranda entre plantas, ultima planta abierta con pilares y pretil, campana de bronce "
             "centrada, aguja y veleta.",
             entry=(6, 13, "sur"))
    acera(o, 0, 0, W - 1, D - 1)
    c = Casa(o, 3, 3, 10, 10, pisos=3)              # interior x 4..9, z 4..9
    s0, s1, s2 = c.suelos
    c.puerta("s", 3)                                # x 6..7
    for p in (0, 1):
        for cn in ("n", "e", "o"):
            c.ventana(cn, 3, p, flores=False)
    c.ventana("s", 3, 1, flores=False)
    escalera_mano(c, 9, 4, 0, "e")
    escalera_mano(c, 4, 9, 1, "o")
    for cn in ("n", "s", "e", "o"):
        c.abrir(cn, 1, 7, 2, cada=5, viga=False)
        for u in range(2, 6):
            x, y, z = c.celda(cn, u, s2)
            o.mat(x, y, z, c.muro)
        c.o.fc(c.caras[cn], 1.0, s2 + 1, -1.0, 7.0, s2 + 1.15, 0.12, PIEDRA_F)
    for y in range(c.cumbre + 1, c.cumbre + 4):
        o.mbox(6, y, 6, 7, y, 7, "techo")
    t = c.cumbre + 4
    o.f(6.85, t, 6.85, 7.15, t + 1.4, 7.15, BRONCE)
    o.f(6.2, t + 1.0, 6.95, 7.8, t + 1.1, 7.05, BRONCE)
    o.f(7.4, t + 0.8, 6.98, 7.9, t + 1.2, 7.02, BRONCE)
    o.f(3.5, c.roof_y - 0.7, 6.7, 10.5, c.roof_y - 0.2, 7.3, M.MADO, 2)
    campana(o, 7.0, c.roof_y - 0.7, 7.0)
    c.mueble(128, 4, s0, 4, 0, "barril"); c.mueble(129, 5, s0, 4, 0, "saco")
    c.farol_pared("o", 1.5, s0 + 3.5); c.farol_pared("e", 6.5, s1 + 3.5)
    return o


# ---------------------------------------------------------------- granero y establo
def granero_establo():
    W, D = 30, 22
    o = Obra("cw_granero_establo", W, 26, D,
             "Granero y establo (progreso: monturas). Muros de tablas con sillares, porton de 4x4, cinco boxes con divisiones, "
             "paja tupida en el suelo de cada box, comedero y balde; fardos apilados, sillas de montar colgadas, horquilla; "
             "carreta con ruedas de rayos afuera.",
             entry=(14, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    c = Casa(o, 3, 4, 24, 17, pisos=1, h=8, muro="madera_pared", teja="techo_rojo")   # interior x 4..23, z 5..16
    s = c.suelos[0]
    c.puerta("n", 9, w=4, h=4)                      # x 12..15
    c.ventana("n", 3, flores=False); c.ventana("n", 17, flores=False)
    c.ventana("o", 3, flores=False); c.ventana("e", 3, flores=False)
    for b in (8, 12, 16, 20):
        o.f(b - 0.1, s, 12, b + 0.1, s + 1.6, 17, (150, 104, 62), 2)
        o.f(b - 0.15, s + 1.6, 12, b + 0.15, s + 1.75, 17, M.MADO, 2)
    for i, b in enumerate((4, 8, 12, 16, 20)):
        c.ocupa("box %d" % (i + 1), b, 12, b + 4, 17, s, s + 1.8, True, choca=False)
        x0 = b + 0.1 if b > 4 else b
        x1 = b + 3.9 if b < 20 else b + 4
        for yy in (0.6, 1.25):
            o.f(x0, s + yy, 11.9, x0 + 1.2, s + yy + 0.15, 12.1, M.MAD, 2)
            o.f(x1 - 1.2, s + yy, 11.9, x1, s + yy + 0.15, 12.1, M.MAD, 2)
        o.f(x0 + 1.2, s, 11.85, x0 + 1.4, s + 1.6, 12.15, M.MADO)
        o.f(x1 - 1.4, s, 11.85, x1 - 1.2, s + 1.6, 12.15, M.MADO)
        for xx in (x0, x1 - 1):
            o.put(int(xx), s, 12, COL_INV); o.put(int(xx), s + 1, 12, COL_INV)
        M.heno_suelo(o, x0 + 0.15, 12.2, x1 - 0.15, 16.2, s, seed=i * 7 + 1, densidad=0.9)
        o.f(b + 0.8, s, 16.3, b + 3.2, s + 0.8, 16.95, (124, 84, 52), 2)
        o.f(b + 0.9, s + 0.65, 16.4, b + 3.1, s + 0.75, 16.85, (120, 160, 70))
        v = Vox(0.0625)
        torno(v, 4.0, 4.0, 0, [3.2, 3.4, 3.6, 3.7, 3.8, 3.9, 3.9], lambda a, t, bb: ((70, 120, 170) if t == 6 and not bb else (M.HIE2 if t in (1, 5) else M.MAD)))
        v.poner(o, b + 3.15, s, 13.0)
    M.heno_suelo(o, 4.2, 5.2, 11.5, 11.4, s, seed=99, densidad=0.35)
    for (x, z, y, sd) in ((4.2, 5.2, s, 1), (4.2, 6.0, s, 2), (5.7, 5.2, s, 3), (4.2, 5.6, s + 0.75, 4), (5.7, 5.6, s + 0.75, 5)):
        M.fardo(o, x, y, z, 0, sd)
    c.ocupa("fardos", 4.2, 5.2, 7.2, 6.8, s, s + 1.5, True)
    for (x, z, y, sd) in ((20.3, 5.2, s, 7), (21.8, 5.2, s, 8), (21.0, 5.2, s + 0.75, 9)):
        M.fardo(o, x, y, z, 0, sd)
    c.ocupa("fardos", 20.3, 5.2, 23.3, 6.0, s, s + 1.5, True)
    o.f(16.25, s, 11.6, 16.32, s + 2.0, 11.68, M.MADC)
    for dx in (-0.12, 0.0, 0.12):
        o.f(16.26 + dx, s + 2.0, 11.6, 16.3 + dx, s + 2.35, 11.66, HIERRO2)
    o.f(16.14, s + 1.98, 11.6, 16.44, s + 2.03, 11.66, HIERRO2)
    ce = c.caras["e"]
    montura(o, ce, c, 2.5, s + 2.2); montura(o, ce, c, 4.5, s + 2.2)
    c.ocupa("sillas de montar", 22, 6.5, 23.0, 9.5, s + 1.8, s + 3.2, True)
    c.farol_pared("o", 8.0, s + 4); c.farol_pared("s", 10.5, s + 4.5)
    o.obj(1016, 25.6, 1, 7.0, 0)
    for (x, z, sd) in ((25.6, 12.2, 11), (25.6, 13.0, 12)):
        M.fardo(o, x, 1, z, 1, sd)
    return o


# ---------------------------------------------------------------- torre arcana (escalas de mano)
def torre_arcana():
    W, D = 16, 16
    o = Obra("cw_torre_arcana", W, 46, D,
             "Torre arcana de 3 plantas (progreso: encantar equipo). Planta baja con circulo de runas y mesa de encantamientos "
             "(libro abierto y cristales flotantes) al centro y cristales en la esquina; primera planta biblioteca con estanterias, "
             "mesa de lectura y candelabro; ultima observatorio con telescopio y mesa de cartas. Escaleras de mano abiertas con "
             "baranda en esquinas opuestas; techo morado con aguja y orbe.",
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
        c.ventana("e", 4, p, flores=False)
    c.cartel_colgante("n", 2.0, s0 + 3, "libro")
    escalera_mano(c, 11, 11, 0, "e")
    escalera_mano(c, 4, 11, 1, "o")
    circulo_runas(o, 8.0, s0 + 0.01, 8.5, 2.2)
    mesa_encantar(o, c, 8.0, s0, 8.5)
    cristales(o, 4.1, s0, 10.0); c.ocupa("cristales", 4.1, 10.0, 5.0, 11.0, s0, s0 + 1, False)
    c.farol_pared("o", 2.6, s0 + 3.5); c.farol_pared("e", 2.6, s0 + 3.5)
    # biblioteca
    c.mueble(127, 4, s1, 4, 2, "estanteria")
    c.mueble(127, 9, s1, 4, 2, "estanteria")
    c.mueble(124, 7, s1, 8, 0, "mesa de lectura")
    c.mueble(131, 7.5, s1, 7, 2, "silla")
    c.mueble(138, 6, s1, 8, 0, "candelabro")
    o.f(7.3, s1 + 1.3, 8.2, 7.9, s1 + 1.45, 8.7, (90, 50, 120)); o.f(8.1, s1 + 1.3, 8.3, 8.7, s1 + 1.4, 8.8, (40, 90, 70))
    c.farol_pared("e", 2.6, s1 + 3.5)
    # observatorio
    telescopio(o, 8.0, s2, 5.5); c.ocupa("telescopio", 7.5, 5.0, 8.5, 6.0, s2, s2 + 2.4, True)
    c.mueble(124, 7, s2, 8.5, 0, "mesa de cartas")
    o.f(7.1, s2 + 1.3, 8.6, 8.9, s2 + 1.32, 9.4, (30, 40, 80))
    for i in range(6):
        o.f(7.3 + (i * 0.27) % 1.5, s2 + 1.32, 8.75 + (i * 0.19) % 0.55, 7.36 + (i * 0.27) % 1.5, s2 + 1.34, 8.81 + (i * 0.19) % 0.55, (250, 240, 170))
    v = Vox(0.0625)
    torno(v, 4.0, 4.0, 0, [1, 1.5, 1, 0.6], lambda a, t, b: M.HIE2, hueco=False)
    for j in range(8):
        r = 3.6 * math.sin((j + 0.5) / 8 * math.pi)
        for i in range(8):
            for k in range(8):
                if math.hypot(i - 3.5, k - 3.5) < r and math.hypot(i - 3.5, k - 3.5) > r - 1.2:
                    v.set(i, 4 + j, k, (60, 110, 180) if (_h(i, j, k) % 3) else (90, 160, 80))
    v.poner(o, 10.3, s2, 9.7)
    c.ocupa("globo", 10.3, 9.7, 10.8, 10.2, s2, s2 + 0.8, True)
    for y in range(c.cumbre + 1, c.cumbre + 5):
        o.mbox(7, y, 7, 8, y, 8, "techo_morado")
    t = c.cumbre + 5
    o.f(7.85, t, 7.85, 8.15, t + 0.8, 8.15, BRONCE)
    o.f(7.65, t + 0.8, 7.65, 8.35, t + 1.5, 8.35, (180, 120, 255), 0, 1)
    return o


TODOS = [tienda_pociones, herreria, carpinteria, pabellon_entrenamiento, campo_tiro, casas_hilera, posada_balcon, pozo,
         torre_vigia, granero_establo, muro_porton, puente_piedra, torre_arcana]
