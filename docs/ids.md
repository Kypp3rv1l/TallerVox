# Ids de bloques y de objetos

Referencia para leer los archivos del Taller (`docs/formato.md`).

## Bloques

En `cubes` cada cubo es `[x, y, z, b]`. `b` = id del bloque; si `b >= 128` es **medio bloque (losa)**: `b - 128` es el id y la losa ocupa la mitad inferior de la celda. `0` = aire (se usa para vaciar).

| id | bloque |
|---:|---|
| 1 | Pasto pradera |
| 2 | Pasto bosque |
| 3 | Pasto humedal |
| 4 | Pasto cañón |
| 5 | Pasto cueva |
| 6 | Tierra con pasto |
| 7 | Tierra |
| 8 | Tierra oscura |
| 9 | Piedra |
| 10 | Piedra clara |
| 11 | Piedra oscura |
| 12 | Arena |
| 13 | Arena oscura |
| 14 | Nieve |
| 15 | Hielo |
| 16 | Barro |
| 17 | Tierra muerta |
| 18 | Tierra muerta oscura |
| 19 | Cañón 1 |
| 20 | Cañón 2 |
| 21 | Cañón 3 |
| 22 | Cañón 4 |
| 23 | Cañón 5 |
| 24 | Cañón (cima) |
| 25 | Cañón (camino) |
| 26 | Pared de cueva |
| 27 | Pared de cueva 2 |
| 28 | Tronco |
| 29 | Tronco oscuro |
| 30 | Abedul |
| 31 | Palmera |
| 32 | Madera muerta |
| 33 | Hoja verde |
| 34 | Hoja lima |
| 35 | Hoja rosa |
| 36 | Hoja violeta |
| 37 | Hoja naranja |
| 38 | Hoja roja |
| 39 | Hoja amarilla |
| 40 | Pino |
| 41 | Pino azul |
| 42 | Hoja nevada |
| 43 | Hoja seca |
| 44 | Cactus |
| 45 | Hoja de palma |
| 46 | Arbusto |
| 47 | Tablones |
| 48 | Tablones oscuros |
| 49 | Entramado |
| 50 | Yeso |
| 51 | Adobe |
| 52 | Adobe oscuro |
| 53 | Adoquín |
| 54 | Adoquín con musgo |
| 55 | Techo rojo |
| 56 | Techo azul |
| 57 | Techo verde |
| 58 | Techo oscuro |
| 59 | Paja |
| 60 | Cristal |
| 61 | Farol (bloque) |
| 62 | Fuego |
| 63 | Tela blanca |
| 64 | Tela roja |
| 65 | Tela azul |
| 66 | Estatua |
| 67 | Estatua oscura |
| 68 | Oro |
| 69 | Piedra negra |
| 70 | Piedra púrpura |
| 71 | Cristal luminoso |
| 72 | Corrupción |
| 73 | Camino |
| 74 | Hoja sagrada |
| 75 | Leño A |
| 76 | Leño B |
| 77 | Pintura roja |
| 78 | Caja |
| 79 | Camino A |
| 80 | Camino B |
| 81 | Hueso |
| 82 | Hueso oscuro |
| 83 | Cristal oscuro |
| 84 | Cristal claro |
| 85 | Ruina |
| 86 | Ruina oscura |
| 87 | Castillo |
| 88 | Castillo oscuro |
| 89 | Colisión invisible |
| 90 | Cascarón (techo invisible) |
| 91 | Cal |
| 92 | Ocre |
| 93 | Rosa |
| 94 | Barro y paja |
| 95 | Granito |
| 96 | Losa |
| 97 | Pizarra |
| 98 | Césped (techo) |
| 99 | Tejuela |
| 100 | Cascada |
| 101 | Musgo |

## Objetos del catálogo (`placed`)

| id | nombre | grupo | ancho x fondo x alto (bloques) | tipo |
|---:|---|---|---|---|
| 101 | Ventana pequena 1x1 | Ventanas | 1 x 1 x 1 | piezas de voxel fino |
| 102 | Ventana 2x2 | Ventanas | 2 x 1 x 2 | piezas de voxel fino |
| 103 | Ventana ancha 3x2 | Ventanas | 3 x 1 x 2 | piezas de voxel fino |
| 104 | Ventana con postigos | Ventanas | 2 x 1 x 2 | piezas de voxel fino |
| 105 | Ventana ojival 2x3 | Ventanas | 2 x 1 x 3 | piezas de voxel fino |
| 106 | Ventana estrecha 1x2 | Ventanas | 1 x 1 x 2 | piezas de voxel fino |
| 107 | Escaparate con toldo | Ventanas | 3 x 1 x 3 | piezas de voxel fino |
| 111 | Puerta 2x3 | Puertas | 2 x 1 x 3 | piezas de voxel fino |
| 112 | Puerta 3x4 | Puertas | 3 x 1 x 4 | piezas de voxel fino |
| 113 | Porton doble 4x4 | Puertas | 4 x 1 x 4 | piezas de voxel fino |
| 114 | Puerta estrecha 1x3 | Puertas | 1 x 1 x 3 | piezas de voxel fino |
| 121 | Cama | Muebles | 2 x 4 x 2 | piezas de voxel fino |
| 122 | Cofre | Muebles | 2 x 1 x 2 | piezas de voxel fino |
| 123 | Mesa larga | Muebles | 3 x 1 x 2 | piezas de voxel fino |
| 124 | Mesa corta | Muebles | 2 x 1 x 2 | piezas de voxel fino |
| 125 | Banco | Muebles | 3 x 1 x 1 | piezas de voxel fino |
| 126 | Taburete | Muebles | 1 x 1 x 1 | piezas de voxel fino |
| 127 | Estanteria | Muebles | 3 x 1 x 4 | piezas de voxel fino |
| 128 | Barril (fino) | Muebles | 1 x 1 x 2 | piezas de voxel fino |
| 129 | Saco | Muebles | 1 x 1 x 1 | piezas de voxel fino |
| 130 | Hogar con fuego | Muebles | 2 x 2 x 1 | piezas de voxel fino |
| 131 | Silla | Muebles | 1 x 1 x 2 | piezas de voxel fino |
| 132 | Alfombra | Muebles | 3 x 2 x 1 | piezas de voxel fino |
| 133 | Armario | Muebles | 2 x 1 x 3 | piezas de voxel fino |
| 134 | Escalera de mano | Estructuras | 1 x 1 x 5 | piezas de voxel fino |
| 135 | Yunque | Muebles | 2 x 1 x 1 | piezas de voxel fino |
| 136 | Cuadro de pared | Decoracion | 2 x 1 x 2 | piezas de voxel fino |
| 137 | Estandarte | Decoracion | 1 x 1 x 3 | piezas de voxel fino |
| 138 | Candelabro | Luces | 1 x 1 x 2 | piezas de voxel fino |
| 139 | Caldero | Muebles | 1 x 1 x 1 | piezas de voxel fino |
| 151 | Pilar de piedra | Estructuras | 1 x 1 x 4 | piezas de voxel fino |
| 152 | Arco de piedra | Estructuras | 4 x 1 x 4 | piezas de voxel fino |
| 153 | Farol de pared | Luces | 1 x 1 x 1 | piezas de voxel fino |
| 154 | Poste de madera | Estructuras | 1 x 1 x 2 | piezas de voxel fino |
| 155 | Valla fina | Estructuras | 3 x 1 x 2 | piezas de voxel fino |
| 156 | Cartel de madera (sin texto) | Estructuras | 2 x 1 x 2 | piezas de voxel fino |
| 157 | Antorcha de pared | Luces | 1 x 1 x 2 | piezas de voxel fino |
| 158 | Chimenea exterior | Estructuras | 2 x 2 x 6 | piezas de voxel fino |
| 159 | Maceta con flores | Decoracion | 1 x 1 x 1 | piezas de voxel fino |
| 160 | Viga / tronco | Estructuras | 4 x 1 x 1 | piezas de voxel fino |
| 161 | Pila de lena | Estructuras | 2 x 1 x 1 | piezas de voxel fino |
| 162 | Escalon de piedra | Estructuras | 2 x 2 x 1 | piezas de voxel fino |
| 163 | Tejadillo de puerta | Puertas | 3 x 2 x 4 | piezas de voxel fino |
| 1001 | Helecho | Naturaleza | 1 x 1 x 1 | decoración (1 bloque) |
| 1002 | Mata de hierba | Naturaleza | 1 x 1 x 1 | decoración (1 bloque) |
| 1003 | Flor azul | Naturaleza | 1 x 1 x 1 | decoración (1 bloque) |
| 1004 | Flor roja | Naturaleza | 1 x 1 x 1 | decoración (1 bloque) |
| 1005 | Flor blanca | Naturaleza | 1 x 1 x 1 | decoración (1 bloque) |
| 1006 | Junco | Naturaleza | 1 x 1 x 1 | decoración (1 bloque) |
| 1007 | Seta | Naturaleza | 1 x 1 x 1 | decoración (1 bloque) |
| 1008 | Arbusto seco | Naturaleza | 1 x 1 x 1 | decoración (1 bloque) |
| 1009 | Flor de hielo | Naturaleza | 1 x 1 x 1 | decoración (1 bloque) |
| 1010 | Hierba muerta | Naturaleza | 1 x 1 x 1 | decoración (1 bloque) |
| 1011 | Ventana (modelo del juego, 2) | Ventanas | 1 x 1 x 1 | decoración (1 bloque) |
| 1012 | Ventana (modelo del juego, 1) | Ventanas | 1 x 1 x 1 | decoración (1 bloque) |
| 1013 | Puerta (modelo del juego) | Puertas | 1 x 1 x 1 | decoración (1 bloque) |
| 1014 | Farol | Luces | 1 x 1 x 1 | decoración (1 bloque) |
| 1015 | Farol de pared (juego) | Luces | 1 x 1 x 1 | decoración (1 bloque) |
| 1016 | Carreta | Estructuras | 1 x 1 x 1 | decoración (1 bloque) |
| 1017 | Cartel | Estructuras | 1 x 1 x 1 | decoración (1 bloque) |
| 1018 | Barril | Estructuras | 1 x 1 x 1 | decoración (1 bloque) |
| 1019 | Valla | Estructuras | 1 x 1 x 1 | decoración (1 bloque) |
| 1020 | Piedritas | Naturaleza | 1 x 1 x 1 | decoración (1 bloque) |
| 1021 | Escombros | Naturaleza | 1 x 1 x 1 | decoración (1 bloque) |
| 1022 | Enredadera | Naturaleza | 1 x 1 x 1 | decoración (1 bloque) |
| 1023 | Farola | Luces | 1 x 1 x 1 | decoración (1 bloque) |
| 1024 | Polea de pozo | Estructuras | 1 x 1 x 1 | decoración (1 bloque) |
| 1025 | Fogata | Luces | 1 x 1 x 1 | decoración (1 bloque) |
| 1026 | Asiento de tronco | Estructuras | 1 x 1 x 1 | decoración (1 bloque) |
| 1027 | Lapida | Estructuras | 1 x 1 x 1 | decoración (1 bloque) |
| 1028 | Caja | Estructuras | 1 x 1 x 1 | decoración (1 bloque) |
| 1029 | Obelisco | Estructuras | 1 x 1 x 1 | decoración (1 bloque) |
| 1030 | Cartel colgante | Estructuras | 1 x 1 x 1 | decoración (1 bloque) |
| 1031 | Cultivo | Naturaleza | 1 x 1 x 1 | decoración (1 bloque) |
| 1032 | Rail | Estructuras | 1 x 1 x 1 | decoración (1 bloque) |
| 1033 | Vagoneta | Estructuras | 1 x 1 x 1 | decoración (1 bloque) |
| 1034 | Toldo con mercancia | Estructuras | 1 x 1 x 1 | decoración (1 bloque) |
| 1035 | Ventana (modelo del juego, 3) | Ventanas | 1 x 1 x 1 | decoración (1 bloque) |
| 1036 | Puesto de mercado | Estructuras | 1 x 1 x 1 | decoración (1 bloque) |
| 1037 | Espantapajaros | Estructuras | 1 x 1 x 1 | decoración (1 bloque) |

Las piezas con id 101-163 son prefabricados de cajas finas (ventanas, puertas, muebles); su frente mira a −Z (norte) con rot = 0. Los ids 1000+ son decoraciones de 1 bloque.
