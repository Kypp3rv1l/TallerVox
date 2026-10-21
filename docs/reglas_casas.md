# Reglas de las casas

## Estilo Cube World (v0.1.5, vigente)

Sacado del video de Thalmor City. Medidas en bloques (1 bloque = 0,5 m; el personaje mide 2). Lo arma `tools/cw_casas.py`.

- **Material**: superficies grandes lisas, un color por bloque con leve variación de tono (sin ladrillo). Todo el detalle va en objetos de voxel chico.
  - muro (186,176,140) · zócalo (98,106,102) · techo (46,86,82) · suelo interior (156,152,138) · entrepiso y techo interior de madera.
- **Casa**: acera de losas de 2 tonos; la casa queda 2 bloques más alta (zócalo oscuro de 2 que sobresale 1). Muro de 7 de alto por planta; cornisa oscura entre plantas.
- **Puerta**: hueco de 2×3 **sin hoja** (sistema de abrir y cerrar a futuro), marco de madera oscura, dintel que sobresale, umbral; un escalón de piedra + el zócalo hacen 2 escalones.
- **Ventanas**: 2×2, alféizar a 2 del suelo, marco y cruz de madera oscura, vidrio azul, repisa por dentro y **jardinera con flores** por fuera. Pocas por cara (1 o 2), simétricas; alineadas entre plantas. Hueco con Colisión invisible (89).
- **Techo**: a cuatro aguas escalonado (cada piso entra 2 bloques), alero de 1, vigas que asoman bajo el alero en los lados largos; por dentro, tablas con vigas.
- **Chimenea**: hogar (130) en un nicho de 2×3 metido en el muro; cuerpo de piedra de 2 de fondo que sale por fuera y se angosta a 2×2 sobre el alero. El nicho es cerrado: fondo con hollín, lados y campana de piedra; repisa de madera encima.
- **Interior**: una sala grande por planta, muebles contra los muros, alfombra grande de borde a dos tonos, farol de pared, plantas en maceta. Escalera recta de madera de 2 de ancho con baranda arriba.
- **Pueblo**: losas de 2 tonos, farolas negras de 6, bancos, árbol en jardinera elevada con borde de piedra, puestos con toldo a rayas.
- **Campos**: terrazas de 1 de desnivel y 10 de fondo, tierra lisa con surcos de dos tonos, borde de pasto, camino de piedra; cultivos cada 2 bloques.

## Reglas anteriores (v0.1.4, sacadas de la Taberna v1)

Sacado del modelo `taberna_gremio_1` (hecho por Ivan). `tools/reeditar.py` aplica estas reglas a las casas del catálogo.
Medidas en bloques (1 bloque = 0,5 m). «Suelo» = primer bloque transitable de la planta (y_local = losa + 1).

## Ventanas
- Hueco de **6 de ancho × 6 de alto**; el **alféizar queda a 2 bloques del suelo** (1 m). Encima quedan al menos 2 bloques de muro.
- Hueco relleno con **Colisión invisible** (id 89): se ve a través y no se atraviesa (hasta que haya vidrio/ventanas que abran).
- Cajas finas (relativas al centro de la ventana, en bloques): alféizar de piedra clara 8,3 × 0,5 sobresale 0,38; montantes blancos a ±3 a ±3,75; dintel blanco arriba (6 → 6,5); **cruz** (poste central + travesaño a media altura); **postigos azules** a cada lado (2,16 de ancho × 6 de alto, con dos listones más oscuros). Plantilla exacta en `tools/plantillas.json` (`ventana`).
- **Simetría**: las ventanas de una misma cara son idénticas y quedan simétricas respecto al centro del muro.
  - cara de menos de 44: una ventana centrada; de 44 a 63: dos, a ~27 % y ~73 %; de 64 o más: tres.
  - Nunca pisan una puerta, la chimenea ni las esquinas (los postigos necesitan 6 de cada lado).
- **Sin puertas**: la entrada es solo el hueco, para agregar las puertas con el sistema de abrir y cerrar después.
- Cada piso lleva su fila de ventanas, alineadas verticalmente.

## Chimenea
- Caja hueca de **adoquín (53) pegada al hastial, 3 de fondo × 6 de ancho**, desde el suelo hasta sobre el caballete.
- Boca de **4 de ancho** abierta en el muro desde el suelo transitable hasta arriba (la chimenea se ve desde la sala como un nicho alto).
- Dentro del hueco va el **Hogar con fuego** (prefab 130).

## Muebles
- Mesa redonda con pedestal (2,5 de diámetro, 1,5 de alto), separadas ≥ 2 bloques entre sí (`mesa_redonda` en las plantillas).
- Barra / mostrador: **2 de fondo × 2 de alto** de Leño B (76), tapa oscura de 0,2 con 0,2 de vuelo hacia el cliente, estanterías detrás con un pasillo de 4. Queda **bajo las ventanas** (alféizar a 2).
- Hogar y mesas dejan pasillo de ≥ 5 bloques delante de puertas y chimenea.
- Hay «Colisión invisible» debajo de lo grande (tableros, bancos, repisas) para que no se atraviesen.

## Qué hace `reeditar.py` en cada casa
1. Mide el anillo de muros y los pisos (losas). 2. Rellena con muro las ventanas viejas (celdas 0/89 que no llegan al suelo) y borra sus cajas finas. 3. Corta las ventanas nuevas según las reglas. 4. Reconstruye la chimenea. 5. Añade muebles (mesas redondas, mostrador en tiendas/tabernas, taburetes) solo donde hay espacio libre.
Se saltan las **ruinas** del juego (`casa_2_plantas_1`, `edificio_medieval_2`, `salon_2_plantas_1/3`) y `ejemplo_caseta`.
