# DEVLOG — Farlands Taller

## v0.1.7
- **Catálogo nuevo**: se sacaron las casas antiguas (y la Taberna v1 y la caseta de ejemplo); quedan solo las 18 estructuras `cw_`.
- **12 estructuras nuevas**: `cw_tienda_pociones`, `cw_herreria` (semiabierta, fragua con chimenea, yunque, pila de temple, piedra de afilar), `cw_carpinteria` (semiabierta), `cw_pabellon_entrenamiento` (suelo de laberinto, columnas, muñecos, dianas), `cw_casas_hilera` (3 casas con muro compartido), `cw_posada_balcon` (balcón y escalera exterior), `cw_pozo`, `cw_torre_vigia` (campanario), `cw_granero_establo` (5 boxes, monturas), `cw_muro_porton` (muralla, casa de guardia, rastrillo), `cw_puente_piedra`, `cw_torre_arcana` (encantamientos, biblioteca, observatorio).
- **Correcciones**: los símbolos de los carteles ya no parpadean (cada pieza va a otra profundidad); los faroles y muebles ya no chocan (la revisión de criterio ahora detecta choques entre objetos y muebles que tapan una ventana por dentro); vuelven los **sillares de esquina**; enredaderas más frondosas (mata al pie, tallos en abanico, racimos de hojas, florcitas y remate que cae a los lados).
- Herramientas: `Casa.abrir` (lados abiertos con pilares y escalón corrido), `escalera_perimetral` (escalera pegada a los muros para torres), `baranda` genérica, puertas de cualquier alto (portones), cornisa y sillares por cara, nuevos materiales (muros ocre/rosa/blanco/tablas, techos morado/rojo/oscuro, piedra de muralla). Símbolos de cartel nuevos: poción, yunque, sierra, cama, libro.

## v0.1.6
Correcciones de la revisión de Ivan a las propuestas `cw_`:
- **Vigas**: ya no cruzan el hueco de la escalera; se cortan y descansan en brochales alrededor del hueco.
- **Chimenea**: cuerpo de sección constante (sin ensanches ni piezas de otro tono), remate y boca de humo centrados. El fuego va al fondo de un nicho de piedra (morillos, leños, brasas, llamas), con solera, marco de piedra y repisa; ya no toca los bordes ni sale a la sala. No se puede entrar al fuego (colisión).
- **Cofres** a los pies de cada cama, pegados y mirando hacia afuera (`Casa.cama_con_cofre`).
- **Baranda** robusta: pilares de 0,26 con capitel en las esquinas y al medio, pasamanos ancho, zócalo, balaustres cada 0,5 y remate contra el muro.
- **Taberna y Gremio** reordenada: barra lejos del hogar con pasillo para el tabernero, mesa redonda, gremio con 3 de fondo detrás del mostrador para el recepcionista (estantería y cofre), tableros con espacio libre delante. Nada frente a la puerta.
- **Mostrador** nuevo: paneles enmarcados, zócalo oscuro metido y tapa con vuelo parejo (sin tablas que sobresalen).
- **Ventanas** abiertas (se ve a través) y muchas menos por fachada.
- **Carteles** de dos caras: tablones con marco, esquineros, cadenas, brazo con voluta y el símbolo detallado en ambas caras; puestos a los lados de la puerta, nunca frente a una ventana.
- **Faroles** de hierro detallados (placa, brazo con voluta, gancho, montantes, vidrio con aro, techito de 3 pisos, argolla). Farolas de la plaza con pie escalonado, anillos, ménsulas y farol grande.
- **Enredaderas** finas: tallos delgados con quiebres, ramitas y hojas chicas de 3 verdes.
- **Plaza**: árbol más grande (tronco 3x3, copa de 17 de ancho).
- **Nuevo `cw_campo_ladera`**: campo sobre terreno irregular, terrazas que siguen las curvas de nivel, labio sin plantar y camino en zigzag.
- **Revisión de criterio** en el generador (`Casa.revisar`): paso libre delante de puertas, escaleras, hogar y tableros; nada inflamable a menos de 2,5 del fuego; nada tapando ventanas por fuera. Si algo no cumple, el generador se detiene y dice qué.

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
