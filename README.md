# Farlands Taller

Herramienta **aparte del juego** para crear estructuras y zonas de Farlands sobre un suelo plano y entregarlas como
archivos `.json` entendibles, para pegarlas luego en la semilla fija.

- **Estructuras**: tamaño de casa como máximo (la casa más grande como referencia).
- **Zonas**: sitios grandes (poblados, el árbol gigante…); en ellas se pueden **estampar estructuras** del catálogo y construir encima.
- **Catálogo «Mis creaciones»**: cada creación se guarda con nombre, captura y archivo; se pueden reabrir, estampar, borrar e importar.
- **Casas del juego ya incluidas** en `catalogo/estructuras` (salón, posada, tiendas, casas, fragua, edificio medieval; 3 variantes de cada una, sacadas de la semilla 1337) para estamparlas o abrirlas y editarlas.
- Mismas herramientas que el editor de mundo del juego (bloques, pincel, caja, detalles, voxel fino 1/8, catálogo de objetos, mover, pegar).

Versión actual: **0.1.5** (ver `DEVLOG.md`).

## Carpetas

| carpeta | contenido |
|---|---|
| `taller/` | proyecto Godot 4.7 (GL Compatibility). `taller.gd` = escena principal, `editor.gd` = el editor, `selftest.gd` = pruebas |
| `taller/bin/` | núcleo C++ de Farlands (GDExtension). Contiene el modo «suelo plano» que necesita el Taller |
| `catalogo/` | tus creaciones (`estructuras/` y `zonas/`): un `.json` + un `.png` por creación |
| `docs/` | `manual.md` (uso), `formato.md` (archivo), `ids.md` (bloques y objetos) |
| `bats/` | scripts de Windows (ver abajo) |

## Empezar (Windows)

1. Clona el repo y corre `bats\4_actualizar_dll.bat` si quieres usar otra DLL del repo de Farlands (el repo ya trae una).
2. `bats\1_chequeo.bat` — pruebas automáticas (pide el .exe de Godot 4.7.1 la primera vez).
3. `bats\2_abrir.bat` — abre el Taller desde el proyecto, sin exportar.
4. `bats\3_exportar.bat` — genera `salida\FarlandsTaller_v<versión>\FarlandsTaller.exe` (+ DLL + `catalogo\`) y su zip.
   Necesita las plantillas de exportación de Godot instaladas (Editor → Administrar plantillas de exportación).

El `.exe` necesita estar **junto a su DLL** y a la carpeta `catalogo`.

## Enviarme una creación

`Ctrl+S` dentro del Taller guarda en `catalogo/`. Pásame el `.json` (o el zip que crea *Exportar TODO el catálogo*).
La integración en el generador/semilla es la fase siguiente.

## Relación con el repo de Farlands

El Taller usa el **mismo núcleo C++** (`codigo/src` de Farlands) en modo suelo plano
(`VoxelWorld.setup_flat(seed, flat_y)`). Cuando el núcleo cambie, copia la DLL nueva a `taller/bin/`.
