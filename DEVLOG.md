# DEVLOG — Farlands Taller

## v0.1.2
- Nueva herramienta **Seleccionar (T)**: elige muebles y objetos de las casas. Modos: objeto completo (cajas pequeñas conectadas), una sola pieza, o caja de dos clics (todo lo que quede dentro). Mayús+clic suma al grupo. Flechas/RePág/AvPág mueven, R gira, Supr borra, Ctrl+Z deshace.
- **Mover (0)** ahora también ve las cajas pequeñas y los objetos (antes el rayo solo tocaba bloques).
- Arreglo: el texto de información de lo elegido daba error de formato.
- Pruebas: 39 (selección, mover con paso 1/8, girar, borrar, caja, casa real).

## v0.1.1
- El catálogo trae 24 casas generadas por el juego (8 tipos × 3 variantes, sin el terreno de debajo), con captura. Se sacaron del juego con la nueva función de núcleo `VoxelWorld.export_clipboard(pos)` y la prueba `--only=export_houses` del repo de Farlands.
- `dev_thumbs.gd` (`--thumbs`): genera las capturas que falten en el catálogo.
- Nota: `editor.gd` se edita directamente (ya no se regenera desde el editor del juego).

## v0.1.0
Primera versión del Taller como herramienta aparte.

- Núcleo: `Generator(seed, flat_y)` y `VoxelWorld.setup_flat()` generan un mundo plano (suelo en y = 199, damero de piedra de 4×4 bloques), sin estructuras, cuevas, árboles ni decoración. El juego normal no cambia.
- Editor: el editor de mundo del juego adaptado (sin mapa/sitios/estructuras generadas) más:
  - documento con **marco** de tamaño limitado (estructura 32×64×32, zona 512×320×512 bloques), entrada y orientación;
  - rejilla de suelo (4, 16 y 1 bloque cerca de la cámara) y borde del marco;
  - catálogo «Mis creaciones» con captura, abrir/estampar/borrar/importar;
  - herramienta **Estampar** (giros de 90°, flechas, comprobación de que cabe);
  - guardado en `.json` (`farlands-taller` v1), autoguardado y exportación en zip.
- Pruebas (`selftest.gd`): suelo, ediciones, archivo, ida y vuelta, estampas con giros 0-3, catálogo en disco.
- Creación de ejemplo: `catalogo/estructuras/ejemplo_caseta.json`.
- `editor.gd` ya es el código fuente propio del Taller (se derivó del editor de mundo v0.15.2 de Farlands).

Pendiente (fase siguiente): integrar las creaciones en el generador y la semilla fija; plantillas de zonas de ejemplo (poblado, árbol).
