# Formato de archivo del Taller (`farlands-taller`, versión 1)

Cada creación es **un solo `.json`** (más una captura `.png` con el mismo nombre). Está pensado para que lo puedas
enviar tal cual y yo lo pegue en la semilla fija.

Ubicación en el catálogo: `catalogo/estructuras/<nombre>.json` y `catalogo/zonas/<nombre>.json`.

## Cabecera (una línea por campo, legible a ojo)

| campo | significado |
|---|---|
| `format`, `version` | siempre `"farlands-taller"`, `1` |
| `taller` | versión del Taller que lo guardó |
| `name`, `kind` | nombre y tipo: `"estructura"` o `"zona"` |
| `description` | texto libre |
| `size` | `[ancho X, alto Y, fondo Z]` del marco, en **bloques** (1 bloque = 0,5 m) |
| `origin` | `[0, 200, 0]`: esquina mínima del marco. 200 es el primer bloque sobre el suelo plano |
| `bbox_min`, `bbox_max` | esquinas del marco, en coordenadas absolutas (incluidas) |
| `coords` | recordatorio de cómo leer las coordenadas |
| `entry` | `{x, z, facing}`: celda de entrada **local** y hacia dónde mira la fachada (`norte` = −Z, `este` = +X, `sur` = +Z, `oeste` = −X) |
| `stamps` | creaciones pegadas desde el catálogo: `{name, file, pos [x,y,z locales], rot 0/90/180/270}`. Es solo informativo: su contenido ya está dentro de `edits` |
| `counts` | cuántos cubos / voxeles finos / objetos hay; `dropped_outside_frame` = ediciones descartadas por estar fuera del marco |
| `edits` | el contenido (ver abajo) |

## Coordenadas

Las coordenadas de `edits` son **absolutas** y están en bloques. La posición local de algo dentro de la creación es:

```
local = (x, y − 200, z)        x en 0..size[0]−1,  z en 0..size[2]−1,  y_local en 0..size[1]−1
```

El suelo plano termina en y = 199; lo primero que se construye está en y = 200 (y_local = 0).
Nada de lo que quede fuera del marco se guarda.

## `edits`

Es el mismo formato `farlands-edits` que usa el editor del juego (así se puede cargar sin conversión):

- `cubes`: `[x, y, z, b]` — un bloque por celda (`b` = id, ver `docs/ids.md`; `0` = vaciado).
- `fine`: `[id, x0, y0, z0, x1, y1, z1, r, g, b, pat, glow]` — caja fina (voxel de 1/8 a 1 bloque) con color 0-255, textura `pat` y brillo `glow`. Las coordenadas son flotantes, en unidades de bloque.
- `placed`: `[id, cat, x, y, z, rot, var, dflags, solid]` — objeto del catálogo (ids en `docs/ids.md`). `(x, y, z)` es la esquina mínima de su huella **ya girada**; `rot` 0-3 (giros de 90°).
- `erase`, `pieces`: siempre vacíos en el Taller (el suelo plano no tiene nada generado que borrar).

## Giros (cómo se estampa una creación girada)

Para un giro de 90° en un marco de fondo `D` (D = size[2]) la celda local `(x, z)` pasa a `(D − 1 − z, x)`;
para cajas finas (continuas) `(x, z) → (D − z, x)` (y se intercambian mínimo/máximo); un objeto de catálogo suma 1 a `rot`
y su esquina mínima pasa a `(D − (z + fondo), x)`. Tras el giro, ancho y fondo del marco se intercambian.
El Taller y las pruebas (`taller/selftest.gd`) usan exactamente esta regla.

## Cómo se integra en la semilla fija (más adelante)

1. Me envías el `.json` (o el zip del catálogo).
2. Yo leo `edits` y lo convierto a coordenadas locales restando `origin`.
3. En el generador, la estructura se coloca en su sitio de la semilla (posición, giro, altura del suelo) y sus cubos/cajas/objetos
   se aplican igual que se aplican hoy las ediciones del editor de mundo.

Eso queda para la fase siguiente; lo importante ahora es que el archivo ya contiene todo lo necesario.
