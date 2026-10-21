# DEVLOG — Farlands Taller

## v0.1.5
- **Propuestas estilo Cube World** (sacadas del video de Thalmor City), nuevas en el catálogo con prefijo `cw_`: `cw_casa_1_planta`, `cw_casa_2_plantas`, `cw_taberna_gremio` (la Taberna y Gremio rehecha a esa escala), `cw_campo_terrazas` y `cw_plaza_arbol`. Las casas viejas no se tocaron.
- Escala de Cube World (personaje de 2 bloques): puerta 2×3 sin hoja, ventana 2×2 con cruz y jardinera, 7 de alto por planta, zócalo oscuro, casa 2 bloques sobre la acera con escalones, techo bajo escalonado verde azulado con vigas bajo el alero.
- **Material liso**: muros, techos, suelos y tierra de cultivo son bloques invisibles sólidos con una caja fina de 1×1×1 por bloque visible (un color por bloque con leve variación de tono, sin dibujo de ladrillo).
- Chimenea nueva: el hogar queda en un nicho cerrado de piedra (fondo, lados y campana); el humero no se ve desde dentro.
- Cultivos de voxel chico: calabazas, matas trepadoras, girasoles y coles; espantapájaros, farolas, puestos con toldo y árbol en pisos.
- Herramientas: `tools/cw_lib.py` (material liso), `tools/cw_casas.py` (casa, ventanas, puerta, chimenea, escalera, mostrador, tablero de misiones…), `tools/cw_propuestas.py` (genera las 5 propuestas).

## v0.1.4
- **Taberna y Gremio** (`taberna_gremio_1`, modelo de Ivan) entra al catálogo y es la referencia de estilo: ver `docs/reglas_casas.md`.
- Las 19 casas genéricas del catálogo se **re-editaron con esas reglas** (`tools/reeditar_todo.py`): ventanas 6×6 con cruz y postigos azules (idénticas por cara, simétricas, alféizar a 1 m), chimenea hueca de 3 de fondo con hogar, mesas redondas / mostrador donde hay espacio. Se saltan las ruinas y la caseta de ejemplo.
- `tools/plantillas.json` (ventana y mesa redonda tomadas de la Taberna), `tools/muebles.py`, `tools/geom.py`.
- `dev_ver.gd` (`--ver=archivo(s).json --out=carpeta --views=auto|nombre:x,y,z,yaw,pitch;…`): capturas de cualquier .json para revisar casas.

## v0.1.3
- Las 24 casas del catálogo se **agrandaron ×2** (interior, techo, muebles, puertas y ventanas), con los muros exteriores e interiores de 1 bloque de grosor. Se hizo con `tools/escalar.py` (duplica las rebanadas de bloques que no son muro ni suelo). Se quitaron los pilotes y el aire bajo las casas: ahora se apoyan en el suelo.
- Nueva herramienta **Caja fina (F)**: dos clics en esquinas con voxeles de 1/8, 1/4, 1/2 o 1 bloque; rellena todo con UNA sola caja (color, brillo y textura de Voxel fino). Opciones: hueca (solo paredes, de 1/8 a 2 bloques de grosor) y «Borrar detalles y cajas finas dentro». Flechas y `.` `,` mueven el punto apuntado; rueda cambia el tamaño.
- Subir y bajar lo elegido: teclas . (sube) y , (baja) además de RePág/AvPág, y botones «Subir» y «Bajar» en los paneles Mover y Seleccionar.
- Límite del marco de una estructura: 96×128×96 (antes 32×64×32).
- Las variantes en ruinas del juego (casa_2_plantas_1, edificio_medieval_2, salon_2_plantas_1/3…) ya venían incompletas del generador.

## v0.1.2
- Nueva herramienta **Seleccionar (T)**: elige muebles y objetos de las casas. Modos: objeto completo (cajas pequeñas conectadas), una sola pieza, o caja de dos clics (todo lo que quede dentro). Mayús+clic suma al grupo. Flechas/RePág/AvPág mueven, R gira, Supr borra, Ctrl+Z deshace.
- **Mover (0)** ahora también ve las cajas pequeñas y los objetos (antes el rayo solo tocaba bloques).
- Cama del catálogo: el respaldo queda ahora pegado al borde de su caja, así se apoya a ras de la pared (antes quedaba 0,75 bloque separado). Requiere la DLL nueva.
- Pestañas más chicas (Herram, Bloques, Objetos, Taller, Casas, Vista) para que no se escondan tras las flechitas.
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
  - documento con **marco** de tamaño limitado (estructura 96×128×96 (desde v0.1.3), zona 512×320×512 bloques), entrada y orientación;
  - rejilla de suelo (4, 16 y 1 bloque cerca de la cámara) y borde del marco;
  - catálogo «Mis creaciones» con captura, abrir/estampar/borrar/importar;
  - herramienta **Estampar** (giros de 90°, flechas, comprobación de que cabe);
  - guardado en `.json` (`farlands-taller` v1), autoguardado y exportación en zip.
- Pruebas (`selftest.gd`): suelo, ediciones, archivo, ida y vuelta, estampas con giros 0-3, catálogo en disco.
- Creación de ejemplo: `catalogo/estructuras/ejemplo_caseta.json`.
- `editor.gd` ya es el código fuente propio del Taller (se derivó del editor de mundo v0.15.2 de Farlands).

Pendiente (fase siguiente): integrar las creaciones en el generador y la semilla fija; plantillas de zonas de ejemplo (poblado, árbol).
