# Manual del Taller

## Idea

Un mundo **plano y vacío** con una rejilla grande. Dentro hay un **marco** verde que marca el espacio máximo de la creación.
Construyes dentro del marco; lo que quede fuera no se guarda.

- **Estructura**: tamaño de casa como máximo (límite 32 × 64 × 32 bloques = 16 × 32 × 16 m; la casa más grande del juego mide 22 × 13 y la torre más alta unos 40 de alto).
- **Zona**: sitios grandes (poblado, árbol gigante…). Límite 512 × 320 × 512 bloques = 256 × 160 × 256 m.
  En una zona puedes **estampar** estructuras de tu catálogo y seguir construyendo encima.

Los límites están en `taller/editor.gd` (`LIM_STRUCT`, `LIM_ZONE`); se cambian en una línea.

## Suelo y rejilla

- El suelo es un damero de 4 × 4 bloques (dos tonos de piedra).
- Líneas finas cada **4 bloques**, amarillas cada **16**, borde verde = límite del marco.
- Cerca de la cámara aparecen también las líneas de **1 bloque**.
- **G** activa/desactiva la cuadrícula sobre la cara que apuntas (1 bloque, o 1/8 con voxel fino).
- El suelo no se puede picar (y cualquier cosa por debajo de y = 200 se descarta al guardar).

## Moverse y mirar

| | |
|---|---|
| W A S D | volar · Espacio/E sube · C/Q baja · Mayús = rápido |
| Clic derecho mantenido y arrastrar | girar la cámara (un clic corto = acción secundaria) |
| Tab | mirar con el ratón (mirilla fija) |
| Flechas | girar la cámara (si no hay nada seleccionado) |

## Herramientas (teclas 1-9, 0 y −)

1 Bloque · 2 Pincel · 3 Caja · 4 Detalles · 5 Voxel fino · 6 Catálogo · 7 (sin uso en el Taller) · 8 Pegar · 9 Inspeccionar · 0 Mover · **−  Estampar**.
Son las mismas del editor de mundo del juego (ver `docs/editor_mundo.md` de Farlands). Atajos comunes: Ctrl+Z / Ctrl+Y, V (paso 1 · 1/2 · 1/8), R girar, Supr borrar, H ayuda.

## Pestañas del panel

- **Herram.**, **Bloques**, **Catálogo**: como en el editor del juego (el catálogo de objetos: ventanas, puertas, muebles, faroles…).
- **Taller**: nombre, tipo (estructura/zona), tamaño del marco, entrada y orientación de la fachada, y los botones de guardar/exportar/nuevo.
- **Mis creaciones**: lista de lo guardado, con captura. Estampar · Abrir para editar · Borrar · Importar un .json.
- **Vista**: velocidad, hora del día, colisiones invisibles, salir.

## Flujo de trabajo

1. Pestaña *Taller*: elige Estructura o Zona, ponle nombre y tamaño. Marca la entrada (amarilla) y hacia dónde mira.
2. Construye. Todo se **autoguarda** (al cerrar y volver a abrir sigues donde estabas).
3. **Ctrl+S** → *Guardar en el catálogo*: crea `catalogo/estructuras/<nombre>.json` (o `zonas/`) y su captura.
4. Para usarla en una zona: *Mis creaciones* → elige → **Estampar**. Apunta al suelo del marco, **R** gira, flechas la mueven,
   clic izquierdo la coloca (rojo = no cabe). Una estampa **se funde** con el documento: después puedes editarla como cualquier otra cosa.
5. Para enviármelo: *Exportar este documento* (zip en el Escritorio) o *Exportar TODO el catálogo*; o simplemente los `.json` de la carpeta `catalogo`.

## Dónde se guardan las cosas

- Catálogo: carpeta `catalogo` junto a `FarlandsTaller.exe` (en desarrollo, la del repo). Si no se puede escribir ahí, usa la carpeta de datos del usuario.
- Autoguardado: `taller_autosave.json` en la carpeta de datos del usuario de Godot (`%APPDATA%\Godot\app_userdata\Farlands Taller`).
- Ajustes: `taller.cfg` en esa misma carpeta.

## Límites conocidos (v0.1)

- Aún **no** se integran las creaciones en el generador/semilla (eso viene después).
- Estampar usa el mismo editor de cubos: si la estampa es enorme y la cámara está lejos, los trozos no cargados se omiten; acércate a la zona antes de estampar.
- El marco no impide pintar fuera con el pincel/caja, pero lo de fuera no se guarda.
