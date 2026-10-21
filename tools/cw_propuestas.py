# Farlands Taller v0.1.5 - propuestas estilo Cube World (Thalmor City). Genera catalogo/estructuras/cw_*.json
# Uso: python tools/cw_propuestas.py [carpeta_salida]
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cw_lib import Obra, WD, WDD, IRON, _h
from cw_casas import Casa, planta, jarron_flores, mesa_redonda, escalera, barra, tablero, HOJA, HOJA2

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "catalogo", "estructuras")

ROJO = (150, 34, 44); ORO = (206, 168, 72); MORADO = (84, 44, 120); AZUL = (60, 110, 170); CELESTE = (130, 180, 214)


def acera(o, x0, z0, x1, z1):
    """Acera de losas lisas de 2x2 con dos tonos (como la plaza de Thalmor)."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            o.mat(x, 0, z, "acera_os" if (_h(x // 2, z // 2) % 4 == 0) else "acera")


# ---------------------------------------------------------------- casa de 1 planta
def casa_1_planta():
    W, D = 22, 19
    o = Obra("cw_casa_1_planta", W, 24, D,
             "Propuesta estilo Cube World: casa de 1 planta 16x12, muros lisos, zocalo oscuro, puerta 2x3 sin hoja con 2 escalones, "
             "ventanas 2x2 con cruz y jardinera, techo bajo escalonado, chimenea de piedra con hogar. Sala unica con cama, mesa, armario y alfombra.",
             entry=(9, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    c = Casa(o, 3, 4, 18, 15)              # 16 x 12
    s = c.suelos[0]
    c.puerta("n", 7)
    c.ventana("n", 2); c.ventana("n", 12)
    c.ventana("o", 5); c.ventana("e", 5)
    c.ventana("s", 3)
    c.chimenea("s", 9)
    c.enredadera("n", 0.6, s - 1, s + 6)
    c.farol_pared("n", 5.5, s + 2, interior=False)
    c.farol_pared("n", 9.5, s + 2, interior=False)
    # interior (x 4..17, z 5..14)
    c.alfombra(6.5, 7, 12.5, 12, 0, MORADO, ORO, 0.5)
    o.obj(124, 8.5, s, 9)                   # mesa
    o.obj(131, 9.0, s, 8, 2); o.obj(131, 9.0, s, 10, 0)
    o.obj(121, 15, s, 11, 0)                # cama contra el muro del fondo
    o.obj(122, 15, s, 9, 0)                 # cofre a los pies
    o.obj(133, 4, s, 13, 1)                 # armario contra el muro oeste
    o.obj(127, 4, s, 5, 1)                  # estanteria
    planta(o, 16, s, 5, grande=True)
    jarron_flores(o, 4, s, 11)
    c.farol_pared("o", 7.5, s + 3); c.farol_pared("e", 2.5, s + 3)
    return o


# ---------------------------------------------------------------- casa de 2 plantas
def casa_2_plantas():
    W, D = 20, 19
    o = Obra("cw_casa_2_plantas", W, 30, D,
             "Propuesta estilo Cube World: casa de 2 plantas 14x12. Abajo cocina-comedor con hogar, escalera de madera al fondo; "
             "arriba dormitorio con dos camas. Ventanas 2x2 alineadas por planta, cornisa entre plantas, enredadera.",
             entry=(9, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    c = Casa(o, 3, 4, 16, 15, pisos=2)
    s, s2 = c.suelos
    c.puerta("n", 6)
    for p in (0, 1):
        c.ventana("n", 2, p); c.ventana("n", 10, p)
        c.ventana("e", 5, p)
        c.ventana("s", 3, p); c.ventana("s", 9, p)
    c.ventana("n", 6, 1)
    c.chimenea("o", 5)
    c.enredadera("n", 13.4, s - 1, s2 + 5)
    c.farol_pared("n", 4.5, s + 2, interior=False); c.farol_pared("n", 8.5, s + 2, interior=False)
    # planta baja (x 4..15, z 5..14): escalera al fondo subiendo hacia +X
    escalera(c, 6, 13, 14, 0, 1)
    c.alfombra(6, 6.5, 12, 11, 0, ROJO, ORO, 0.5)
    o.obj(123, 7.5, s, 8.5)                          # mesa larga
    o.obj(125, 7.5, s, 7.5, 0); o.obj(125, 7.5, s, 9.5, 2)
    o.obj(127, 12, s, 5, 2)                          # estanteria contra el frente
    o.obj(128, 14.2, s, 9); o.obj(128, 14.2, s, 10); o.obj(129, 14.1, s, 11)
    o.obj(161, 4, s, 10, 1)                          # lena junto al hogar
    planta(o, 4, s, 5, grande=True)
    c.farol_pared("e", 2.5, s + 3); c.farol_pared("o", 2.5, s + 3)
    # planta alta: dormitorio
    c.alfombra(6.5, 6, 12.5, 10.5, 1, AZUL, CELESTE, 0.5)
    o.obj(121, 4.5, s2, 5, 2); o.obj(121, 13.5, s2, 5, 2)   # camas con la cabecera al frente
    o.obj(122, 4.5, s2, 9.2, 0); o.obj(122, 13.5, s2, 9.2, 0)
    o.obj(133, 15, s2, 9, 3)                         # armario contra el muro este
    jarron_flores(o, 9.5, s2, 5)
    c.farol_pared("o", 4.5, s2 + 3); c.farol_pared("e", 8.5, s2 + 3)
    return o


# ---------------------------------------------------------------- taberna y gremio
def taberna_gremio():
    W, D = 32, 24
    o = Obra("cw_taberna_gremio", W, 32, D,
             "Propuesta estilo Cube World de la Taberna y Gremio de Ivan (26x16, 2 plantas). Planta baja: a la izquierda la taberna "
             "(barra con barriles detras, mesas largas con bancos, mesa redonda, hogar); a la derecha el gremio (mostrador de recompensas "
             "y dos tableros de misiones en el muro este). Arriba, cuartos de posada. Puerta 2x3 sin hoja, carteles colgantes.",
             entry=(15, 0, "norte"))
    acera(o, 0, 0, W - 1, D - 1)
    c = Casa(o, 3, 4, 28, 19, pisos=2)
    s, s2 = c.suelos
    c.puerta("n", 12)
    for u in (3, 7, 17, 21):
        c.ventana("n", u, 0)
    for u in (3, 7, 12, 17, 21):
        c.ventana("n", u, 1)
    for p in (0, 1):
        c.ventana("o", 3, p); c.ventana("o", 11, p)
        c.ventana("s", 4, p); c.ventana("s", 20, p)
    c.ventana("e", 4, 1); c.ventana("e", 10, 1)
    c.chimenea("o", 7)
    c.cartel_colgante("n", 10, s + 3, "jarra")
    c.cartel_colgante("n", 22, s + 3, "escudo")
    c.farol_pared("n", 10.5, s + 1, interior=False); c.farol_pared("n", 14.5, s + 1, interior=False)
    c.enredadera("n", 0.6, s - 1, s2 + 5); c.enredadera("n", 25.4, s - 1, s2 + 5)
    o.obj(128, 6, 1, 1); o.obj(128, 7, 1, 1); o.obj(128, 24, 1, 1)
    o.obj(125, 9, 1, 1)
    # --- taberna (x 4..15)
    escalera(c, 10, 17, 18, 0, 1)                    # escalera al fondo, x 10..17
    barra(o, 4, 13, 8, 14, s, "n")
    for x in (5, 7):
        o.obj(126, x, s, 11.6)
    for z in (16, 17, 18):
        o.obj(128, 4, s, z)
    o.obj(128, 5, s, 18); o.obj(128, 6, s, 18)
    o.obj(123, 7, s, 7); o.obj(125, 7, s, 6, 0); o.obj(125, 7, s, 8, 2)
    mesa_redonda(o, 12.5, s, 10.5)
    o.obj(126, 10.6, s, 10); o.obj(126, 13.4, s, 10); o.obj(126, 12, s, 12)
    c.alfombra(10, 5.5, 22, 9, 0, ROJO, ORO, 0.5)
    # --- gremio (x 17..27)
    barra(o, 19, 15, 26, 16, s, "n")
    o.obj(122, 20, s, 18, 0); o.obj(122, 24, s, 18, 0)
    tablero(o, "e", c, 3, s + 1.5)
    tablero(o, "e", c, 9, s + 1.5)
    mesa_redonda(o, 21.5, s, 9.5)
    o.obj(126, 19.6, s, 9); o.obj(126, 22.4, s, 9)
    planta(o, 16, s, 5, grande=True); planta(o, 27, s, 5, grande=True)
    for cn, u in (("o", 2.5), ("o", 13.5), ("e", 7.5), ("s", 2.5), ("s", 23.5)):
        c.farol_pared(cn, u, s + 3.5)
    # --- arriba: posada
    for x in (5, 9, 19, 23):
        o.obj(121, x, s2, 5, 2)
        o.obj(122, x, s2, 9.2, 0)
    c.alfombra(5, 11, 26, 15, 1, MORADO, ORO, 0.6)
    o.obj(133, 27, s2, 11, 3)
    jarron_flores(o, 14.5, s2, 5); jarron_flores(o, 16.5, s2, 5)
    for cn, u in (("o", 5.5), ("e", 7.5), ("n", 13.5), ("s", 23.5)):
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
def farola(o, x, y, z):
    cx, cz = x + 0.5, z + 0.5
    o.f(cx - 0.35, y, cz - 0.35, cx + 0.35, y + 0.4, cz + 0.35, (34, 34, 38))
    o.f(cx - 0.14, y + 0.4, cz - 0.14, cx + 0.14, y + 5.2, cz + 0.14, (24, 24, 28))
    o.f(cx - 0.3, y + 5.2, cz - 0.3, cx + 0.3, y + 5.32, cz + 0.3, (24, 24, 28))
    o.f(cx - 0.24, y + 5.32, cz - 0.24, cx + 0.24, y + 5.9, cz + 0.24, (255, 222, 140), 0, 1)
    o.f(cx - 0.36, y + 5.9, cz - 0.36, cx + 0.36, y + 6.02, cz + 0.36, (24, 24, 28))
    o.f(cx - 0.2, y + 6.02, cz - 0.2, cx + 0.2, y + 6.3, cz + 0.2, (24, 24, 28))
    o.put(x, y, z, 89); o.put(x, y + 1, z, 89)


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


def plaza_arbol():
    W, D = 30, 30
    o = Obra("cw_plaza_arbol", W, 26, D,
             "Propuesta estilo Cube World: trozo de plaza de Thalmor. Losas lisas de dos tonos, arbol grande en jardinera elevada con borde de piedra, "
             "bancos alrededor, dos farolas negras y dos puestos de mercado con toldo a rayas.",
             entry=(15, 0, "norte"))
    for x in range(W):
        for z in range(D):
            o.mat(x, 0, z, "acera_os" if (_h(x // 2, z // 2) % 4 == 0) else "acera")
    cx, cz = 15, 15
    for x in range(W):
        for z in range(D):
            d = max(abs(x + 0.5 - cx), abs(z + 0.5 - cz)) * 0.62 + (abs(x + 0.5 - cx) + abs(z + 0.5 - cz)) * 0.38
            if d < 4.6:
                o.mat(x, 1, z, "pasto" if (_h(x, z) % 5) else "pasto_os")
            elif d < 5.6:
                o.mat(x, 1, z, "zocalo")
    # arbol: tronco 2x2 que se abre abajo, copa en capas
    for y in range(2, 10):
        o.mbox(14, y, 14, 15, y, 15, "tronco")
    for (x, z) in ((13, 14), (16, 15), (14, 13), (15, 16)):
        o.mat(x, 2, z, "tronco")
    o.mat(13, 3, 15, "tronco"); o.mat(16, 3, 14, "tronco")
    # copa en pisos (como los arboles de Thalmor): discos de 2 de alto que se achican y se corren un poco
    pisos = [(9, 6.3, 15.0, 15.0), (11, 6.0, 14.6, 15.4), (13, 4.7, 15.4, 14.7), (15, 2.7, 15.0, 15.1)]
    for (y0, r, bx, bz) in pisos:
        for y in (y0, y0 + 1):
            rr = r if y == y0 else r - 0.7
            for x in range(W):
                for z in range(D):
                    if ((x + 0.5 - bx) ** 2 + (z + 0.5 - bz) ** 2) < rr * rr:
                        o.mat(x, y, z, "hoja_os" if y == y0 else ("hoja" if (_h(x, y, z) % 4) else "hoja_os"))
    # bancos mirando hacia afuera, farolas y puestos
    o.obj(125, 13.5, 1, 7.6, 2); o.obj(125, 13.5, 1, 21.4, 0)
    o.obj(125, 7.6, 1, 13.5, 3); o.obj(125, 21.4, 1, 13.5, 1)
    farola(o, 6, 1, 6); farola(o, 23, 1, 23)
    puesto(o, 3, 1, 23)
    puesto(o, 22, 1, 3, (40, 90, 170), (244, 240, 228))
    for (x, z) in ((25, 9), (4, 19)):
        o.obj(159, x, 1, z)
    o.obj(128, 8, 1, 25); o.obj(129, 9, 1, 25.2)
    return o


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn in (casa_1_planta, casa_2_plantas, taberna_gremio, campo_terrazas, plaza_arbol):
        ob = fn()
        print(ob.nombre, ob.escribir(os.path.join(OUT, ob.nombre + ".json")))
