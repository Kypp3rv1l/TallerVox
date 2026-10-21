# Farlands Taller v0.1.8 - propuestas estilo Cube World (Thalmor City). Genera catalogo/estructuras/cw_*.json
# Uso: python tools/cw_propuestas.py [carpeta_salida]
# Cada casa pasa por Casa.revisar(): si un mueble pisa el paso de una puerta o escalera, queda pegado al fuego
# o algo tapa una ventana por fuera, el generador se detiene y dice que fallo.
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cw_lib import Obra, WD, WDD, IRON, _h
from cw_casas import (Casa, planta, jarron_flores, mesa_redonda, escalera, barra, tablero, farol,
                      HOJA, HOJA2, HIERRO, HIERRO2)

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "catalogo", "estructuras")

ROJO = (150, 34, 44); ORO = (206, 168, 72); MORADO = (84, 44, 120); AZUL = (60, 110, 170); CELESTE = (130, 180, 214)


def acera(o, x0, z0, x1, z1):
    """Acera de losas lisas de 2x2 con dos tonos (como la plaza de Thalmor)."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            o.mat(x, 0, z, "acera_os" if (_h(x // 2, z // 2) % 4 == 0) else "acera")


def afuera(c, nombre, x0, z0, x1, z1, y0, y1, cat=None, x=None, y=None, z=None, rot=0):
    """Objeto fuera de la casa: revisa que no tape ventanas ni el paso de la puerta."""
    c.ocupa(nombre, x0, z0, x1, z1, y0, y1, False, exterior=True)
    if cat:
        c.o.obj(cat, x, y, z, rot)


# ---------------------------------------------------------------- casa de 1 planta
def casa_1_planta():
    W, D = 22, 19
    o = Obra("cw_casa_1_planta", W, 24, D,
             "Propuesta estilo Cube World: casa de 1 planta 16x12, muros lisos, zocalo oscuro, puerta 2x3 sin hoja con 2 escalones, "
             "ventanas 2x2 abiertas con cruz y jardinera, techo bajo escalonado, chimenea de piedra con hogar en nicho. "
             "Sala unica: cama con cofre a los pies, mesa con sillas, armario y estanteria.",
             entry=(10, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    c = Casa(o, 3, 4, 18, 15)              # interior x 4..17, z 5..14
    s = c.suelos[0]
    c.puerta("n", 7)                       # x 10..11
    c.ventana("n", 2); c.ventana("n", 12)
    c.ventana("o", 5); c.ventana("e", 5)
    c.ventana("s", 3)
    c.chimenea("s", 8)                     # hogar en x 11..12, contra el fondo
    c.enredadera("n", 0.7, s - 1, s + 4.5)
    c.farol_pared("n", 5.4, s + 1, interior=False)
    c.farol_pared("n", 10.6, s + 1, interior=False)
    # interior
    c.alfombra(5.5, 7.5, 10.5, 11.5, 0, MORADO, ORO, 0.5)
    c.mueble(124, 7, s, 9, 0, "mesa")
    c.mueble(131, 7.5, s, 8, 2, "silla"); c.mueble(131, 7.5, s, 10, 0, "silla")
    c.cama_con_cofre(15, s, 11, 0)        # cabecera contra el muro del fondo
    c.mueble(133, 4, s, 12, 1, "armario")
    c.mueble(127, 4, s, 5, 1, "estanteria")
    planta(o, 16, s, 5, grande=True, casa=c)
    jarron_flores(o, 4, s, 10, casa=c)
    c.farol_pared("o", 7.6, s + 3.5); c.farol_pared("e", 3.0, s + 3.5)
    return o


# ---------------------------------------------------------------- casa de 2 plantas
def casa_2_plantas():
    W, D = 20, 19
    o = Obra("cw_casa_2_plantas", W, 30, D,
             "Propuesta estilo Cube World: casa de 2 plantas 14x12. Abajo comedor con hogar en nicho y escalera de madera al fondo "
             "(vigas cortadas en el hueco, baranda robusta arriba); arriba dormitorio con dos camas y cofres a los pies. "
             "Ventanas 2x2 abiertas alineadas por planta, cornisa entre plantas, enredadera fina.",
             entry=(9, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    c = Casa(o, 3, 4, 16, 15, pisos=2)     # interior x 4..15, z 5..14
    s, s2 = c.suelos
    c.puerta("n", 6)                       # x 9..10
    for p in (0, 1):
        c.ventana("n", 1, p); c.ventana("n", 11, p)
        c.ventana("e", 5, p)
    c.ventana("s", 6, 1)
    c.chimenea("o", 5, olla=True)          # hogar en z 9..10
    c.enredadera("n", 13.3, s - 1, s2 + 3)
    c.farol_pared("n", 4.4, s + 1, interior=False); c.farol_pared("n", 9.6, s + 1, interior=False)
    # planta baja
    escalera(c, 6, 13, 14, 0, 1)          # sube en +X por el fondo, x 6..13
    c.alfombra(7, 7.5, 12.5, 11.5, 0, ROJO, ORO, 0.5)
    c.mueble(123, 8, s, 9, 0, "mesa larga")
    c.mueble(125, 8, s, 8, 0, "banco"); c.mueble(125, 8, s, 10, 2, "banco")
    c.mueble(127, 15, s, 6, 3, "estanteria")
    c.mueble(128, 14, s, 11, 0, "barril"); c.mueble(128, 14, s, 12, 0, "barril"); c.mueble(129, 13, s, 12, 0, "saco")
    c.mueble(161, 4, s, 5, 1, "lena")
    planta(o, 14, s, 5, grande=True, casa=c)
    c.farol_pared("e", 8.0, s + 3.5); c.farol_pared("o", 3.2, s + 3.5)
    # planta alta: dormitorio
    c.alfombra(7, 6, 12, 10.5, 1, AZUL, CELESTE, 0.5)
    c.cama_con_cofre(4.5, s2, 5, 2); c.cama_con_cofre(12.5, s2, 5, 2)
    c.mueble(133, 15, s2, 6, 3, "armario")
    jarron_flores(o, 9.5, s2, 5, casa=c)
    c.farol_pared("o", 3.5, s2 + 3); c.farol_pared("e", 9.5, s2 + 3)
    return o


# ---------------------------------------------------------------- taberna y gremio
def taberna_gremio():
    W, D = 32, 24
    o = Obra("cw_taberna_gremio", W, 32, D,
             "Propuesta estilo Cube World de la Taberna y Gremio de Ivan (26x16, 2 plantas). Planta baja: a la izquierda la taberna "
             "(hogar en el muro oeste, barra lejos del fuego con barriles detras y pasillo para el tabernero, mesa redonda); "
             "a la derecha el gremio (dos tableros de misiones en el muro este y mostrador de recompensas con 3 de fondo para el "
             "recepcionista, estanteria y cofre). Arriba, cuartos de posada. Puerta 2x3 sin hoja; carteles colgantes a los lados.",
             entry=(15, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    c = Casa(o, 3, 4, 28, 19, pisos=2)     # interior x 4..27, z 5..18
    s, s2 = c.suelos
    c.puerta("n", 12)                      # x 15..16
    c.ventana("n", 4, 0); c.ventana("n", 20, 0)
    c.ventana("s", 4, 0)
    for u in (4, 12, 20):
        c.ventana("n", u, 1)
    c.ventana("s", 4, 1); c.ventana("s", 20, 1)
    c.ventana("e", 7, 1)
    c.chimenea("o", 4)                     # hogar en z 8..9
    c.cartel_colgante("n", 8.5, s + 3, "jarra")
    c.cartel_colgante("n", 17.5, s + 3, "escudo")
    c.farol_pared("n", 10.4, s + 1, interior=False); c.farol_pared("n", 15.6, s + 1, interior=False)
    c.enredadera("n", 0.7, s - 1, s2 + 3); c.enredadera("n", 25.3, s - 1, s2 + 3)
    afuera(c, "barril", 5, 1, 6, 2, 1, 3, 128, 5, 1, 1); afuera(c, "barril", 6, 1, 7, 2, 1, 3, 128, 6, 1, 1)
    afuera(c, "banco", 20, 1.4, 23, 2.4, 1, 2, 125, 20, 1, 1.4)
    escalera(c, 13, 17, 18, 0, 1)         # al fondo, x 13..20
    # --- taberna (x 4..12)
    barra(o, 5, 13, 9, 14, s, "n", casa=c, nombre="barra")
    for x in (5, 6, 7, 8):
        c.mueble(128, x, s, 18, 0, "barril")
    for x in (5.3, 7.0, 8.7):
        c.mueble(126, x, s, 11.6, 0, "taburete")
    mesa_redonda(o, 10, s, 8.5, casa=c)
    c.mueble(126, 7.6, s, 8.0, 0, "taburete"); c.mueble(126, 11.4, s, 8.0, 0, "taburete"); c.mueble(126, 9.5, s, 10.0, 0, "taburete")
    c.alfombra(13.5, 9.5, 18.5, 15.5, 0, ROJO, ORO, 0.5)
    # --- gremio (x 19..27)
    tablero(o, "e", c, 2, s + 1.2)
    tablero(o, "e", c, 6, s + 1.2)
    barra(o, 21, 14, 27, 15, s, "n", casa=c, nombre="mostrador del gremio")
    c.mueble(127, 23, s, 18, 0, "estanteria")
    c.mueble(122, 27, s, 16, 3, "cofre")
    mesa_redonda(o, 22.5, s, 9, casa=c)
    c.mueble(126, 20.1, s, 8.5, 0, "taburete"); c.mueble(126, 23.9, s, 8.5, 0, "taburete")
    planta(o, 12, s, 5, grande=True, casa=c); planta(o, 27, s, 5, grande=True, casa=c)
    for cn, u, y in (("o", 11.5, s + 3.5), ("s", 2.5, s + 3.5), ("e", 10.5, s + 3.5), ("n", 9.5, s + 3.5), ("n", 17.5, s + 3.5)):
        c.farol_pared(cn, u, y)
    # --- arriba: posada
    for x in (5, 9, 19, 23):
        c.cama_con_cofre(x, s2, 5, 2)
    c.alfombra(6, 11, 22, 15.5, 1, MORADO, ORO, 0.6)
    c.mueble(133, 27, s2, 13, 3, "armario")
    jarron_flores(o, 13, s2, 5, casa=c); jarron_flores(o, 17, s2, 5, casa=c)
    for cn, u in (("o", 6.5), ("e", 4.0), ("n", 9.5), ("n", 17.5)):
        c.farol_pared(cn, u, s2 + 3)
    return o


# ---------------------------------------------------------------- cultivos (voxel chico)
NAR = (232, 112, 30); NAR2 = (206, 90, 24); TALLO = (60, 120, 40); AMA = (246, 200, 40); MARRON = (96, 56, 30)


def calabaza(o, x, y, z, k):
    s = 0.8 + (k % 3) * 0.1
    cx, cz = x + 0.5, z + 0.5
    for i, dx in enumerate((-0.3, -0.1, 0.1, 0.3)):
        hh = s * (0.62 if i in (1, 2) else 0.52)
        o.f(cx + dx * s - 0.1 * s, y, cz - 0.4 * s, cx + dx * s + 0.1 * s, y + hh, cz + 0.4 * s, NAR if i % 2 else NAR2)
    o.f(cx - 0.4 * s, y + 0.06, cz - 0.3 * s, cx + 0.4 * s, y + 0.5 * s, cz + 0.3 * s, NAR2)
    o.f(cx - 0.05, y + 0.6 * s, cz - 0.05, cx + 0.05, y + 0.8 * s, cz + 0.05, TALLO)
    o.f(cx - 0.02, y + 0.72 * s, cz - 0.2, cx + 0.16, y + 0.8 * s, cz + 0.02, HOJA)
    for j, (dx, dz) in enumerate(((-0.75, 0.2), (0.7, -0.3), (0.2, 0.75))):
        if (k + j) % 3:
            o.f(cx + dx - 0.22, y, cz + dz - 0.18, cx + dx + 0.22, y + 0.12, cz + dz + 0.18, HOJA if j % 2 else HOJA2)
            o.f(cx + dx - 0.04, y, cz + dz - 0.04, cx + dx + 0.04, y + 0.25, cz + dz + 0.04, TALLO)


def trepadora(o, x, y, z, k):
    cx, cz = x + 0.5, z + 0.5
    hh = 2.4 + (k % 3) * 0.25
    o.f(cx - 0.06, y, cz - 0.06, cx + 0.06, y + hh, cz + 0.06, MARRON)
    yy, i = y + 0.3, 0
    while yy < y + hh - 0.1:
        sgn = 1 if (i + k) % 2 else -1
        ax = (i % 2 == 0)
        dx, dz = (sgn * 0.3, 0) if ax else (0, sgn * 0.3)
        o.f(cx + dx - 0.22, yy, cz + dz - 0.22, cx + dx + 0.22, yy + 0.28, cz + dz + 0.22, HOJA if i % 2 else HOJA2)
        o.f(cx + dx * 1.7 - 0.12, yy + 0.18, cz + dz * 1.7 - 0.12, cx + dx * 1.7 + 0.12, yy + 0.36, cz + dz * 1.7 + 0.12, HOJA2)
        if i % 3 == 2:
            o.f(cx - dx - 0.06, yy, cz - dz - 0.06, cx - dx + 0.06, yy + 0.3, cz - dz + 0.06, (110, 170, 60))
        yy += 0.38
        i += 1
    o.f(cx - 0.2, y + hh, cz - 0.2, cx + 0.2, y + hh + 0.25, cz + 0.2, HOJA2)


def girasol(o, x, y, z, k):
    cx, cz = x + 0.5, z + 0.5
    hh = 2.5 + (k % 3) * 0.3
    o.f(cx - 0.07, y, cz - 0.07, cx + 0.07, y + hh, cz + 0.07, TALLO)
    for i, yy in enumerate((0.6, 1.2, 1.8)):
        sg = 1 if (i + k) % 2 else -1
        o.f(cx + sg * 0.07, y + yy, cz - 0.15, cx + sg * 0.5, y + yy + 0.12, cz + 0.15, HOJA)
        o.f(cx + sg * 0.4, y + yy + 0.12, cz - 0.12, cx + sg * 0.6, y + yy + 0.24, cz + 0.12, HOJA2)
    # cabeza mirando a -Z (hacia el camino), un poco inclinada hacia adelante
    zf = cz - 0.12
    o.f(cx - 0.55, y + hh - 0.35, zf - 0.12, cx + 0.55, y + hh + 0.65, zf, AMA)
    o.f(cx - 0.35, y + hh - 0.55, zf - 0.12, cx + 0.35, y + hh + 0.85, zf, AMA)
    o.f(cx - 0.75, y + hh - 0.15, zf - 0.12, cx + 0.75, y + hh + 0.45, zf, AMA)
    o.f(cx - 0.3, y + hh - 0.15, zf - 0.2, cx + 0.3, y + hh + 0.45, zf - 0.1, MARRON)
    o.f(cx - 0.4, y + hh - 0.05, zf, cx + 0.4, y + hh + 0.35, zf + 0.12, TALLO)


def col(o, x, y, z, k):
    cx, cz = x + 0.5, z + 0.5
    o.f(cx - 0.3, y, cz - 0.3, cx + 0.3, y + 0.5, cz + 0.3, (150, 200, 110))
    for i, (dx, dz) in enumerate(((-0.35, 0), (0.35, 0), (0, -0.35), (0, 0.35))):
        o.f(cx + dx - 0.22, y, cz + dz - 0.22, cx + dx + 0.22, y + 0.35 + (i % 2) * 0.08, cz + dz + 0.22, (96, 170, 80) if (i + k) % 2 else (80, 150, 70))


def espantapajaros(o, x, y, z):
    cx, cz = x + 0.5, z + 0.5
    o.f(cx - 0.08, y, cz - 0.08, cx + 0.08, y + 3.0, cz + 0.08, MARRON)
    o.f(cx - 1.1, y + 2.0, cz - 0.07, cx + 1.1, y + 2.14, cz + 0.07, MARRON)
    o.f(cx - 0.32, y + 1.2, cz - 0.22, cx + 0.32, y + 2.3, cz + 0.22, (40, 40, 48))
    o.f(cx - 0.9, y + 1.9, cz - 0.16, cx - 0.32, y + 2.24, cz + 0.16, (40, 40, 48))
    o.f(cx + 0.32, y + 1.9, cz - 0.16, cx + 0.9, y + 2.24, cz + 0.16, (40, 40, 48))
    o.f(cx - 1.05, y + 1.75, cz - 0.1, cx - 0.9, y + 2.2, cz + 0.1, (214, 190, 120))
    o.f(cx + 0.9, y + 1.75, cz - 0.1, cx + 1.05, y + 2.2, cz + 0.1, (214, 190, 120))
    o.f(cx - 0.26, y + 2.3, cz - 0.26, cx + 0.26, y + 2.82, cz + 0.26, (214, 190, 120))
    o.f(cx - 0.12, y + 2.5, cz - 0.27, cx - 0.04, y + 2.6, cz - 0.26, (30, 30, 30))
    o.f(cx + 0.04, y + 2.5, cz - 0.27, cx + 0.12, y + 2.6, cz - 0.26, (30, 30, 30))
    o.f(cx - 0.5, y + 2.82, cz - 0.5, cx + 0.5, y + 2.9, cz + 0.5, (28, 28, 32))
    o.f(cx - 0.25, y + 2.9, cz - 0.25, cx + 0.25, y + 3.4, cz + 0.25, (28, 28, 32))
    o.put(x, y, z, 89); o.put(x, y + 1, z, 89)


def campo_terrazas():
    W, D, NT, P = 48, 44, 4, 10
    o = Obra("cw_campo_terrazas", W, 14, D,
             "Propuesta estilo Cube World: campo de cultivo en 4 terrazas de tierra lisa (1 bloque de desnivel, 10 de fondo) con bordes de pasto "
             "y camino de piedra al medio. Terrazas: calabazas, matas trepadoras, girasoles y coles; espantapajaros. Cultivos de voxel chico.",
             entry=(24, 0, "norte"))
    o.mbox(0, 0, 0, W - 1, 0, 1, "pasto")
    for t in range(NT):
        z0, z1 = 2 + P * t, 1 + P * (t + 1)
        for x in range(W):
            for z in range(z0, z1 + 1):
                borde = x < 4 or x > W - 5 or z == z1 and t == NT - 1
                camino = 22 <= x <= 25
                for y in range(0, t + 1):
                    if y < t:
                        o.mat(x, y, z, "tierra_os" if not borde else "pasto_os")
                    else:
                        o.mat(x, y, z, "pasto" if borde else ("piedra" if camino else ("tierra" if (z - z0) % 2 == 0 else "tierra_os")))
        y = t + 1
        planta_fn = (calabaza, trepadora, girasol, col)[t]
        k = 0
        for zz in range(z0 + 1, z1, 2):
            for xx in list(range(5, 21, 2)) + list(range(27, 43, 2)):
                planta_fn(o, xx, y, zz, k)
                k += 1
    o.mbox(0, 0, NT * P + 2, W - 1, NT - 2, D - 1, "pasto_os")
    o.mbox(0, NT - 1, NT * P + 2, W - 1, NT - 1, D - 1, "pasto")
    espantapajaros(o, 14, 2, 17)
    espantapajaros(o, 34, 3, 26)
    for x in list(range(4, 20, 3)) + list(range(27, 43, 3)):
        o.obj(155, x, 1, 0.6, 0)
    return o


# ---------------------------------------------------------------- plaza con arbol
def puesto(o, x0, y, z0, a=(206, 46, 52), b=(244, 240, 228)):
    """Puesto de mercado 4x2 con toldo a rayas (frente a -Z)."""
    for (px, pz) in ((x0, z0), (x0 + 3.85, z0), (x0, z0 + 1.85), (x0 + 3.85, z0 + 1.85)):
        o.f(px, y, pz, px + 0.15, y + 2.9, pz + 0.15, WDD)
    o.f(x0, y + 1.0, z0, x0 + 4, y + 1.15, z0 + 2, WD, 2)
    o.f(x0 + 0.1, y + 0.2, z0 + 0.1, x0 + 3.9, y + 1.0, z0 + 1.9, (110, 72, 44), 2)
    for i in range(8):
        col = a if i % 2 == 0 else b
        o.f(x0 - 0.2 + i * 0.55, y + 2.9, z0 - 0.4, x0 - 0.2 + (i + 1) * 0.55, y + 3.05, z0 + 2.2, col)
        o.f(x0 - 0.2 + i * 0.55, y + 2.6, z0 - 0.45, x0 - 0.2 + (i + 1) * 0.55, y + 2.9, z0 - 0.35, col)
    frutas = [(232, 60, 40), (250, 200, 40), (120, 190, 60), (240, 140, 40)]
    for i in range(4):
        cx = x0 + 0.5 + i * 0.85
        o.f(cx - 0.35, y + 1.15, z0 + 0.3, cx + 0.35, y + 1.4, z0 + 1.0, (150, 110, 70), 2)
        for j in range(3):
            o.f(cx - 0.28 + j * 0.2, y + 1.4, z0 + 0.4 + (j % 2) * 0.2, cx - 0.12 + j * 0.2, y + 1.56, z0 + 0.56 + (j % 2) * 0.2, frutas[i])
    o.box(int(x0), y, int(z0), int(x0) + 3, y + 1, int(z0) + 1, 89)




# ---------------------------------------------------------------- campo en ladera (terreno irregular)
def campo_ladera():
    """Campo que sigue el terreno: la ladera (altura que sube hacia +Z con ondulaciones) se corta en terrazas de 1 bloque
    que siguen las curvas de nivel, asi que tienen fondos y bordes distintos. Fuera de la mancha del campo queda pasto.
    Cada nivel lleva su cultivo; el borde de cada terraza queda sin plantar (labio) y un camino de piedra sube serpenteando."""
    W, D = 48, 48
    o = Obra("cw_campo_ladera", W, 20, D,
             "Propuesta estilo Cube World: campo en ladera irregular. Las terrazas siguen las curvas de nivel del terreno "
             "(fondos y bordes distintos), con labio sin plantar, pasto alrededor, camino de piedra que sube en zigzag "
             "y un cultivo por nivel (calabazas, matas trepadoras, girasoles, coles). Ejemplo de como el generador adapta los campos.",
             entry=(24, 0, "norte"))

    def alt(x, z):
        return 0.6 + z * 0.19 + 1.5 * math.sin(x / 6.5 + 0.4) + 1.1 * math.sin((x + 1.7 * z) / 11.0)

    def campo(x, z):
        return ((x - 24) / 19.5) ** 2 + ((z - 25) / 19.0) ** 2 + 0.18 * math.sin(x * 0.35) * math.cos(z * 0.28) < 1.0

    def camino(x, z):
        return abs(x - (24 + 5 * math.sin(z / 7.0))) < 1.6

    L = {}
    for x in range(W):
        for z in range(D):
            L[(x, z)] = max(0, int(math.floor(alt(x, z))))
    for (x, z), lv in L.items():
        dentro = campo(x, z)
        for y in range(0, lv + 1):
            if y < lv:
                o.mat(x, y, z, "tierra_os" if dentro else "pasto_os")
            elif camino(x, z) and dentro:
                o.mat(x, y, z, "piedra")
            elif dentro:
                o.mat(x, y, z, "tierra" if (z % 2 == 0) else "tierra_os")
            else:
                o.mat(x, y, z, "pasto" if (_h(x, z) % 5) else "pasto_os")
    cultivos = (calabaza, trepadora, girasol, col)
    k = 0
    for x in range(1, W - 1, 2):
        for z in range(1, D - 1, 2):
            if not campo(x, z) or camino(x, z) or camino(x + 1, z) or camino(x - 1, z):
                continue
            lv = L[(x, z)]
            labio = any(L[(x + dx, z + dz)] != lv or not campo(x + dx, z + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if labio:
                continue
            cultivos[(lv // 2) % 4](o, x, lv + 1, z, k)
            k += 1
    espantapajaros(o, 14, L[(14, 19)] + 1, 19)
    espantapajaros(o, 33, L[(33, 31)] + 1, 31)
    return o


# ---------------------------------------------------------------- plaza con arbol
def farola(o, x, y, z):
    """Farola negra de 6,4: pie de 3 escalones, fuste con anillos, capitel, mensulas y farol grande arriba."""
    cx, cz = x + 0.5, z + 0.5
    for (r, y0, y1) in ((0.46, 0, 0.18), (0.36, 0.18, 0.36), (0.26, 0.36, 0.6)):
        o.f(cx - r, y + y0, cz - r, cx + r, y + y1, cz + r, HIERRO if r < 0.4 else HIERRO2)
    o.f(cx - 0.11, y + 0.6, cz - 0.11, cx + 0.11, y + 4.7, cz + 0.11, HIERRO)
    for yy in (1.0, 2.8, 4.45):
        o.f(cx - 0.16, y + yy, cz - 0.16, cx + 0.16, y + yy + 0.08, cz + 0.16, HIERRO2)
    o.f(cx - 0.2, y + 4.7, cz - 0.2, cx + 0.2, y + 4.82, cz + 0.2, HIERRO2)
    o.f(cx - 0.3, y + 4.82, cz - 0.3, cx + 0.3, y + 4.9, cz + 0.3, HIERRO)
    for (dx, dz) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        for i in range(3):
            a = 0.12 + i * 0.07
            o.f(cx + dx * a - 0.03 - (0.03 if dz else 0), y + 4.5 + i * 0.12, cz + dz * a - 0.03 - (0.03 if dx else 0),
                cx + dx * a + 0.03 + (0.03 if dz else 0), y + 4.6 + i * 0.12, cz + dz * a + 0.03 + (0.03 if dx else 0), HIERRO)
    farol(o, cx, y + 4.9, cz, 1.35, pie=False)
    o.put(x, y, z, 89); o.put(x, y + 1, z, 89)


def plaza_arbol():
    W, D = 30, 30
    o = Obra("cw_plaza_arbol", W, 30, D,
             "Propuesta estilo Cube World: trozo de plaza de Thalmor. Losas lisas de dos tonos, arbol grande (tronco 3x3, copa en pisos "
             "de 17 de ancho) en jardinera elevada con borde de piedra, bancos alrededor, dos farolas negras detalladas y dos puestos de "
             "mercado con toldo a rayas.",
             entry=(15, 0, "norte"))
    for x in range(W):
        for z in range(D):
            o.mat(x, 0, z, "acera_os" if (_h(x // 2, z // 2) % 4 == 0) else "acera")
    cx, cz = 15.0, 15.0
    for x in range(W):
        for z in range(D):
            d = max(abs(x + 0.5 - cx), abs(z + 0.5 - cz)) * 0.62 + (abs(x + 0.5 - cx) + abs(z + 0.5 - cz)) * 0.38
            if d < 5.0:
                o.mat(x, 1, z, "pasto" if (_h(x, z) % 5) else "pasto_os")
            elif d < 6.0:
                o.mat(x, 1, z, "zocalo")
    for y in range(2, 13):
        o.mbox(14, y, 14, 16, y, 16, "tronco")
    for (x, z) in ((13, 15), (17, 15), (15, 13), (15, 17), (13, 14), (17, 16), (16, 13), (14, 17)):
        o.mat(x, 2, z, "tronco")
    for (x, z) in ((13, 15), (17, 15), (15, 13), (15, 17)):
        o.mat(x, 3, z, "tronco")
    o.mat(17, 10, 15, "tronco"); o.mat(18, 11, 15, "tronco"); o.mat(12, 11, 14, "tronco")
    pisos = [(11, 8.6, 15.0, 15.0), (13, 8.2, 14.5, 15.5), (15, 6.8, 15.6, 14.6), (17, 4.9, 15.0, 15.2), (19, 2.7, 15.2, 15.0)]
    for (y0, r, bx, bz) in pisos:
        for y in (y0, y0 + 1):
            rr = r if y == y0 else r - 0.7
            for x in range(W):
                for z in range(D):
                    if ((x + 0.5 - bx) ** 2 + (z + 0.5 - bz) ** 2) < rr * rr:
                        o.mat(x, y, z, "hoja_os" if y == y0 else ("hoja" if (_h(x, y, z) % 4) else "hoja_os"))
    o.obj(125, 13.5, 1, 6.6, 2); o.obj(125, 13.5, 1, 22.4, 0)
    o.obj(125, 6.6, 1, 13.5, 3); o.obj(125, 22.4, 1, 13.5, 1)
    farola(o, 4, 1, 4); farola(o, 25, 1, 25)
    puesto(o, 2, 1, 24)
    puesto(o, 24, 1, 2, (40, 90, 170), (244, 240, 228))
    for (x, z) in ((26, 9), (3, 20)):
        o.obj(159, x, 1, z)
    o.obj(128, 7, 1, 26); o.obj(129, 8, 1, 26.2)
    return o


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    solo = sys.argv[2].split(",") if len(sys.argv) > 2 else None
    import cw_edificios
    for fn in [casa_1_planta, casa_2_plantas, taberna_gremio, campo_terrazas, campo_ladera, plaza_arbol] + cw_edificios.TODOS:
        if solo and fn.__name__ not in solo:
            continue
        ob = fn()
        print(ob.nombre, ob.escribir(os.path.join(OUT, ob.nombre + ".json")))
