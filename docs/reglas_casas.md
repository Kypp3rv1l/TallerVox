# Reglas de las casas (sacadas de la Taberna v1)

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
