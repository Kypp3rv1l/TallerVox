extends Node
## Editor de mundo (F9). Control total del mundo de semilla fija: cubo a cubo, detalles, voxeles de 1/8,
## catalogo de objetos, edificios, mapa de sitios y exportacion a zip. El trabajo pesado lo hace el nucleo C++.

const UI := preload("res://ui_style.gd")
const BS := 0.5
const SLAB := 0x80
const MAX_REACH := 160.0      # m

const T_BLOCK := 0
const T_BRUSH := 1
const T_BOX := 2
const T_DETAIL := 3
const T_FINE := 4
const T_CAT := 5
const T_STRUCT := 6
const T_PASTE := 7
const T_INSPECT := 8
const T_MOVE := 9
const T_STAMP := 10
const T_SELECT := 11
const STEPS := [1.0, 0.5, 0.125]
const STEP_NAMES := ["1 bloque", "1/2 bloque", "1/8 de bloque"]
const TOOLS := ["Bloque", "Pincel", "Caja", "Detalles", "Voxel fino", "Catálogo", "Estructura", "Pegar", "Inspeccionar", "Mover (0)", "Estampar (−)", "Seleccionar (T)"]
const TOOL_HELP := [
	"Clic izq: quitar el bloque apuntado · Clic der: poner el bloque actual junto a la cara apuntada · Rueda: cambiar de bloque · Clic central: copiar el bloque apuntado.",
	"Clic izq: excavar (o pintar) · Clic der: rellenar (o deshacer lo editado) · Rueda: tamaño del pincel.",
	"Clic izq en dos esquinas: aplica la acción elegida a la caja · Clic der: cancelar. La acción se elige en el panel.",
	"Clic izq: borrar el detalle apuntado (ventana, marco, mueble, farol…) · Clic der: restaurar los detalles borrados alrededor · Supr: borrar.",
	"Clic izq: poner un voxel pequeño (1/8) pegado a la cara apuntada · Clic der: quitar el voxel/detalle apuntado · Clic central: copiar su color · Rueda: tamaño.",
	"Elige un objeto en la pestaña Objetos · Clic izq: colocar · Clic der: quitar el objeto apuntado · R: girar · Flechas/RePág/AvPág: mover · Inicio: reiniciar.",
	"Clic izq: elegir la estructura bajo el cursor (se resalta) · Los ajustes están en la pestaña Estructura.",
	"Pega lo copiado con la herramienta Caja · Clic izq: pegar · Mayús+clic: pegar también el aire · R: girar.",
	"Muestra qué hay bajo el cursor · Clic izq: copiar las coordenadas al portapapeles.",
	"Clic izq: elegir un detalle, objeto o bloque (Mayús+clic en otro bloque: ampliar la región) · Flechas: mover (relativo a la cámara) · RePág/AvPág: subir/bajar · Mayús+flecha: extender · Ctrl+flecha: achicar · V: paso · X: descomponer · R: girar · Supr: borrar · Esc: soltar.",
	"Estampa una creación de «Mis creaciones» dentro del marco · Clic izq: poner · R o rueda: girar · Flechas: mover la sombra · Inicio: reiniciar. Rojo = no cabe.",
	"SELECCIONAR cosas de una casa: clic izq en un mueble = elige el objeto completo (todas sus cajas pequeñas conectadas) · Mayús+clic: sumar más · modo «Caja»: dos clics en esquinas y elige todo lo que quede dentro · Flechas: mover · R: girar · Supr: borrar · V: paso · Esc: soltar.",
]
const BOX_ACTIONS := ["Rellenar con el bloque actual", "Vaciar (quitar bloques)", "Reemplazar el bloque de la esquina A por el actual", "Volver a lo generado (quitar mis ediciones)",
	"Borrar detalles y objetos (ventanas, muebles…)", "Restaurar detalles borrados", "Copiar la región", "Rellenar solo el aire", "Pintar solo los bloques sólidos", "Seleccionar para mover / extender"]
const BLOCK_NAMES := ["Aire", "Pasto pradera", "Pasto bosque", "Pasto humedal", "Pasto cañón", "Pasto cueva", "Tierra con pasto", "Tierra", "Tierra oscura", "Piedra", "Piedra clara", "Piedra oscura",
	"Arena", "Arena oscura", "Nieve", "Hielo", "Barro", "Tierra muerta", "Tierra muerta oscura", "Cañón 1", "Cañón 2", "Cañón 3", "Cañón 4", "Cañón 5", "Cañón (cima)", "Cañón (camino)",
	"Pared de cueva", "Pared de cueva 2", "Tronco", "Tronco oscuro", "Abedul", "Palmera", "Madera muerta", "Hoja verde", "Hoja lima", "Hoja rosa", "Hoja violeta", "Hoja naranja", "Hoja roja",
	"Hoja amarilla", "Pino", "Pino azul", "Hoja nevada", "Hoja seca", "Cactus", "Hoja de palma", "Arbusto", "Tablones", "Tablones oscuros", "Entramado", "Yeso", "Adobe", "Adobe oscuro",
	"Adoquín", "Adoquín con musgo", "Techo rojo", "Techo azul", "Techo verde", "Techo oscuro", "Paja", "Cristal", "Farol (bloque)", "Fuego", "Tela blanca", "Tela roja", "Tela azul",
	"Estatua", "Estatua oscura", "Oro", "Piedra negra", "Piedra púrpura", "Cristal luminoso", "Corrupción", "Camino", "Hoja sagrada", "Leño A", "Leño B", "Pintura roja", "Caja",
	"Camino A", "Camino B", "Hueso", "Hueso oscuro", "Cristal oscuro", "Cristal claro", "Ruina", "Ruina oscura", "Castillo", "Castillo oscuro", "Colisión invisible",
	"Cascarón (techo invisible)", "Cal", "Ocre", "Rosa", "Barro y paja", "Granito", "Losa", "Pizarra", "Césped (techo)", "Tejuela", "Cascada", "Musgo"]
const GROUPS := ["Todos", "Ventanas", "Puertas", "Muebles", "Luces", "Decoracion", "Estructuras", "Naturaleza"]

var main: Node3D
var world: Node
var active := false
var captured := false
var cam: Camera3D
var yaw := 0.0
var pitch := -0.4
var speed := 16.0
var fov := 70.0

# estado de las herramientas
var tool := T_BLOCK
var block := 9
var slab := false
var recent: Array = [9, 7, 1, 50, 53, 28]
var brush_n := 3
var brush_shape := 1
var brush_mode := 0
var box_action := 0
var box_a := Vector3i.ZERO
var has_a := false
var fine_size := 1
var fine_color := Color(0.85, 0.7, 0.4)
var fine_glow := false
var fine_pat := 0
var cat_id := 121
var cat_rot := 0
var cat_off := Vector3i.ZERO
var sel: Dictionary = {}
var step_i := 0
var arrow_ms := 0
var sel_label: Label
var step_btn: OptionButton
var cat_solid := false
var cat_auto := true
var cat_inside := true
var cat_items: Dictionary = {}
var paste_rot := 0
var paste_air := false
var sel_piece: Dictionary = {}
var show_barriers := false
var notes: Array = []
var sites: PackedInt32Array = PackedInt32Array()
var site_labels: PackedStringArray = PackedStringArray()

# rayo
var hit: Dictionary = {}
var txn := false
var held := 0                 # boton mantenido (1 izq, 2 der)
var repeat_t := 0.0
var last_cell := Vector3i(-999999, 0, 0)
var mmb_down := false
var mmb_moved := 0.0
var rmb_down := false
var rmb_moved := 0.0
var save_t := -1.0
var dirty_save := false
var msg_t := 0.0
var stats_t := 0.0
var barrier_t := 0.0
var map_open = null

# 3D
var lines_mesh := ImmediateMesh.new()
var fill_mesh := ImmediateMesh.new()
var lines_mi: MeshInstance3D
var fill_mi: MeshInstance3D
var barrier_mm: MultiMeshInstance3D
var _lines: Array = []
var _fills: Array = []
var _glines: Array = []
var grid_on := true

# UI
var ui: CanvasLayer
var root: Control
var panel: PanelContainer
var tabs: TabContainer
var info_label: Label
var help_label: Label
var msg_label: Label
var cross: Control
var tool_buttons: Array = []
var tool_opts: Array = []
var sel_label2: Label
var step_btn2: OptionButton
var select_mode := 0
var sel_a_set := false
var sel_a := Vector3i.ZERO
var block_label: Label
var block_grid: GridContainer
var cat_list: ItemList
var cat_search: LineEdit
var cat_group: OptionButton
var cat_ids: Array = []
var site_list: ItemList
var site_search: LineEdit
var site_filter: OptionButton
var site_ids: Array = []
var struct_label: Label
var struct_btns: Array = []
var stats_label: Label
var note_edit: LineEdit
var note_list: ItemList
var box_label: Label
var paste_label: Label
var file_dlg: FileDialog
var confirm: ConfirmationDialog
var swatch: ColorRect
var help_on := true


# ---------------------------------------------------------------------------------------------
# arranque
# ---------------------------------------------------------------------------------------------

func _ready() -> void:
	world = main.world
	cam = Camera3D.new()
	cam.near = 0.05
	cam.far = 3000.0
	cam.current = false
	main.add_child(cam)
	lines_mi = MeshInstance3D.new()
	lines_mi.mesh = lines_mesh
	lines_mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var lm := StandardMaterial3D.new()
	lm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	lm.vertex_color_use_as_albedo = true
	lm.no_depth_test = true
	lm.render_priority = 10
	lm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	lines_mi.material_override = lm
	lines_mi.top_level = true
	main.add_child(lines_mi)
	fill_mi = MeshInstance3D.new()
	fill_mi.mesh = fill_mesh
	fill_mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var fm := StandardMaterial3D.new()
	fm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	fm.vertex_color_use_as_albedo = true
	fm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	fm.cull_mode = BaseMaterial3D.CULL_DISABLED
	fm.render_priority = 9
	fill_mi.material_override = fm
	fill_mi.top_level = true
	main.add_child(fill_mi)
	barrier_mm = MultiMeshInstance3D.new()
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	var bm := BoxMesh.new()
	bm.size = Vector3(0.5, 0.5, 0.5) * 1.02
	var bmat := StandardMaterial3D.new()
	bmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	bmat.albedo_color = Color(1, 0.15, 0.15, 0.35)
	bmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	bm.material = bmat
	mm.mesh = bm
	mm.instance_count = 0
	barrier_mm.multimesh = mm
	barrier_mm.top_level = true
	main.add_child(barrier_mm)
	for c in world.catalog_list():
		cat_items[int(c["id"])] = c
	_build_ui()
	_load_notes()
	active = false
	ui.visible = false
	lines_mi.visible = false
	fill_mi.visible = false
	barrier_mm.visible = false
	set_process(false)
	set_process_unhandled_input(false)


func kind_group(k: int) -> int:
	if k in [0, 1, 27, 28, 29, 33]:
		return 0
	if k in [5, 6, 7, 8, 9, 10, 11, 21, 22, 23, 24, 25, 26, 30, 32]:
		return 1
	return 2


func _set_captured(on: bool) -> void:
	captured = on
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED if on else Input.MOUSE_MODE_VISIBLE
	cross.visible = on
	if on:
		var f := get_viewport().gui_get_focus_owner()
		if f:
			f.release_focus()


# ---------------------------------------------------------------------------------------------
# interfaz
# ---------------------------------------------------------------------------------------------

func _lbl(text: String, size := 13, col := Color(0.9, 0.95, 1.0), wrap := 0.0) -> Label:
	return UI.label(text, size, col, wrap)


func _btn(text: String, cb: Callable) -> Button:
	var b := Button.new()
	b.text = text
	UI.button(b)
	b.pressed.connect(cb)
	return b


func _build_ui() -> void:
	ui = CanvasLayer.new()
	ui.layer = 8
	main.add_child(ui)
	root = Control.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.add_child(root)
	# mirilla
	cross = Control.new()
	cross.set_anchors_preset(Control.PRESET_CENTER)
	cross.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(cross)
	for r in [Rect2(-9, -1, 18, 2), Rect2(-1, -9, 2, 18)]:
		var cr := ColorRect.new()
		cr.color = Color(1, 1, 1, 0.8)
		cr.position = r.position
		cr.size = r.size
		cr.mouse_filter = Control.MOUSE_FILTER_IGNORE
		cross.add_child(cr)
	info_label = _lbl("", 14)
	info_label.position = Vector2(10, 8)
	info_label.add_theme_color_override("font_outline_color", Color.BLACK)
	info_label.add_theme_constant_override("outline_size", 6)
	root.add_child(info_label)
	help_label = _lbl("", 13, Color(0.8, 0.95, 1.0), 640.0)
	help_label.add_theme_color_override("font_outline_color", Color.BLACK)
	help_label.add_theme_constant_override("outline_size", 5)
	root.add_child(help_label)
	msg_label = _lbl("", 16, Color(1, 0.95, 0.5))
	msg_label.add_theme_color_override("font_outline_color", Color.BLACK)
	msg_label.add_theme_constant_override("outline_size", 7)
	root.add_child(msg_label)
	# panel derecho
	panel = PanelContainer.new()
	panel.add_theme_stylebox_override("panel", UI.box(UI.BG, UI.LINE, 1, 4))
	panel.theme = UI.theme()
	panel.set_anchors_preset(Control.PRESET_RIGHT_WIDE)
	panel.offset_left = -430
	panel.offset_right = 0
	panel.offset_top = 0
	panel.offset_bottom = 0
	root.add_child(panel)
	tabs = TabContainer.new()
	tabs.custom_minimum_size = Vector2(408, 0)
	tabs.add_theme_font_size_override("font_size", 12)
	tabs.clip_tabs = false
	panel.add_child(tabs)
	_build_tab_tools()
	_build_tab_blocks()
	_build_tab_catalog()
	_build_dummies()
	_build_tab_taller()
	_build_tab_creations()
	_build_tab_view()
	_build_dialogs()


func _tab(name: String) -> VBoxContainer:
	var sc := ScrollContainer.new()
	sc.name = name
	sc.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	tabs.add_child(sc)
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 6)
	v.custom_minimum_size = Vector2(388, 0)
	sc.add_child(v)
	return v


func _build_tab_tools() -> void:
	var v := _tab("Herram")
	var grid := GridContainer.new()
	grid.columns = 3
	v.add_child(grid)
	for i in range(TOOLS.size()):
		var b := Button.new()
		b.text = "%d %s" % [i + 1, TOOLS[i]]
		b.toggle_mode = true
		b.custom_minimum_size = Vector2(104, 34)
		UI.button(b)
		var idx := i
		b.pressed.connect(func() -> void: set_tool(idx))
		grid.add_child(b)
		tool_buttons.append(b)
	var ur := HBoxContainer.new()
	ur.add_child(_btn("Deshacer (Ctrl+Z)", func() -> void: do_undo()))
	ur.add_child(_btn("Rehacer (Ctrl+Y)", func() -> void: do_redo()))
	v.add_child(ur)
	# opciones por herramienta
	for i in range(TOOLS.size()):
		var o := VBoxContainer.new()
		o.add_theme_constant_override("separation", 6)
		v.add_child(o)
		tool_opts.append(o)
	var o0: VBoxContainer = tool_opts[T_BLOCK]
	block_label = _lbl("", 14)
	o0.add_child(block_label)
	var sl := CheckBox.new()
	sl.text = "Medio bloque (losa)"
	sl.toggled.connect(func(on: bool) -> void: slab = on)
	o0.add_child(sl)
	o0.add_child(_lbl("Elige el bloque en la pestaña Bloques. [ y ] lo cambian.", 12, UI.DIM, 370.0))
	var o1: VBoxContainer = tool_opts[T_BRUSH]
	var r1 := HBoxContainer.new()
	r1.add_child(_lbl("Tamaño", 13))
	var sp := SpinBox.new()
	sp.min_value = 1
	sp.max_value = 15
	sp.value = brush_n
	sp.value_changed.connect(func(x: float) -> void: brush_n = int(x))
	sp.name = "BrushSize"
	r1.add_child(sp)
	o1.add_child(r1)
	var sh := OptionButton.new()
	sh.add_item("Esfera")
	sh.add_item("Cubo")
	sh.selected = 0
	brush_shape = 1
	sh.item_selected.connect(func(i: int) -> void: brush_shape = 1 - i)
	o1.add_child(sh)
	var bm := OptionButton.new()
	bm.add_item("Excavar (izq) / Rellenar (der)")
	bm.add_item("Pintar con el bloque (izq) / Quitar mi edición (der)")
	bm.item_selected.connect(func(i: int) -> void: brush_mode = i)
	o1.add_child(bm)
	o1.add_child(_lbl("Excavar abre cuevas; Rellenar tapa las existentes (solo el aire).", 12, UI.DIM, 370.0))
	var o2: VBoxContainer = tool_opts[T_BOX]
	var ba := OptionButton.new()
	for a in BOX_ACTIONS:
		ba.add_item(a)
	ba.item_selected.connect(func(i: int) -> void: box_action = i)
	o2.add_child(ba)
	box_label = _lbl("", 13, UI.ACCENT, 370.0)
	o2.add_child(box_label)
	var o3: VBoxContainer = tool_opts[T_DETAIL]
	o3.add_child(_lbl("Apunta a una ventana, marco, mueble, farol… y borra solo ese detalle. Para quitar un muro entero usa Bloque o Caja.", 12, UI.DIM, 370.0))
	var o4: VBoxContainer = tool_opts[T_FINE]
	var fs := OptionButton.new()
	for t in ["1/8 de bloque", "2/8 (1/4)", "4/8 (1/2)", "8/8 (1 bloque)"]:
		fs.add_item(t)
	fs.item_selected.connect(func(i: int) -> void: fine_size = [1, 2, 4, 8][i])
	o4.add_child(fs)
	var cp := ColorPickerButton.new()
	cp.color = fine_color
	cp.custom_minimum_size = Vector2(0, 30)
	cp.color_changed.connect(func(c: Color) -> void: fine_color = c)
	o4.add_child(cp)
	var gl := CheckBox.new()
	gl.text = "Brilla (luz propia)"
	gl.toggled.connect(func(on: bool) -> void: fine_glow = on)
	o4.add_child(gl)
	var pt := OptionButton.new()
	for t in ["Textura 0 (lisa)", "1 piedra", "2 madera", "3 tela", "4", "5", "6", "7", "8", "9", "10"]:
		pt.add_item(t)
	pt.item_selected.connect(func(i: int) -> void: fine_pat = i)
	o4.add_child(pt)
	var o5: VBoxContainer = tool_opts[T_CAT]
	o5.add_child(_lbl("Objeto: (elige uno en Catálogo)", 13, UI.ACCENT, 370.0))
	o5.get_child(0).name = "CatName"
	var ca := CheckBox.new()
	ca.text = "Orientar solo según la pared apuntada"
	ca.button_pressed = true
	ca.toggled.connect(func(on: bool) -> void: cat_auto = on)
	o5.add_child(ca)
	var ci := CheckBox.new()
	ci.text = "Dentro del muro (ventanas y puertas)"
	ci.button_pressed = true
	ci.toggled.connect(func(on: bool) -> void: cat_inside = on)
	o5.add_child(ci)
	var cs := CheckBox.new()
	cs.text = "Con colisión sólida"
	cs.toggled.connect(func(on: bool) -> void: cat_solid = on)
	o5.add_child(cs)
	var rr := HBoxContainer.new()
	rr.add_child(_btn("Girar (R)", func() -> void: cat_rot = (cat_rot + 1) % 4))
	rr.add_child(_btn("Reiniciar posición", func() -> void: cat_off = Vector3i.ZERO))
	o5.add_child(rr)
	var o6: VBoxContainer = tool_opts[T_STRUCT]
	o6.add_child(_lbl("Clic en una casa, iglesia, pozo… para elegirla y cambiarla en la pestaña Estructura.", 12, UI.DIM, 370.0))
	var o7: VBoxContainer = tool_opts[T_PASTE]
	paste_label = _lbl("", 13, UI.ACCENT, 370.0)
	o7.add_child(paste_label)
	var pa := CheckBox.new()
	pa.text = "Pegar también el aire"
	pa.toggled.connect(func(on: bool) -> void: paste_air = on)
	o7.add_child(pa)
	o7.add_child(_btn("Girar (R)", func() -> void: paste_rot = (paste_rot + 1) % 4))
	var o8: VBoxContainer = tool_opts[T_INSPECT]
	o8.add_child(_lbl("La información sale arriba a la izquierda.", 12, UI.DIM, 370.0))

	var o9: VBoxContainer = tool_opts[T_MOVE]
	sel_label = _lbl("Nada elegido. Clic en un detalle, objeto o bloque.", 13, UI.ACCENT, 370.0)
	o9.add_child(sel_label)
	var sr := HBoxContainer.new()
	sr.add_child(_lbl("Paso (V)", 13))
	step_btn = OptionButton.new()
	for t in STEP_NAMES:
		step_btn.add_item(t)
	step_btn.item_selected.connect(func(i: int) -> void: step_i = i)
	sr.add_child(step_btn)
	o9.add_child(sr)
	var mr := HBoxContainer.new()
	mr.add_child(_btn("Descomponer (X)", func() -> void: _decompose()))
	mr.add_child(_btn("Borrar (Supr)", func() -> void: _delete_sel()))
	mr.add_child(_btn("Soltar (Esc)", func() -> void: sel = {}))
	o9.add_child(mr)
	o9.add_child(_lbl("Flechas: mover según hacia dónde miras · RePág/AvPág: subir/bajar · Mayús+flecha: extender esa cara · Ctrl+flecha: achicar esa cara · R: girar objetos. Con algo elegido la cámara no gira con las flechas.", 12, UI.DIM, 370.0))

	var o11: VBoxContainer = tool_opts[T_SELECT]
	o11.add_child(_lbl("Elegir:", 13))
	var mode_btn := OptionButton.new()
	mode_btn.add_item("Objeto completo (cajas pequeñas conectadas)")
	mode_btn.add_item("Una sola pieza pequeña")
	mode_btn.add_item("Caja: todo lo que quede dentro (2 clics)")
	mode_btn.item_selected.connect(func(i: int) -> void:
		select_mode = i
		sel_a_set = false)
	o11.add_child(mode_btn)
	sel_label2 = _lbl("Nada elegido. Clic en un mueble, objeto o bloque.", 13, UI.ACCENT, 370.0)
	o11.add_child(sel_label2)
	var sr2 := HBoxContainer.new()
	sr2.add_child(_lbl("Paso (V)", 13))
	step_btn2 = OptionButton.new()
	for t2 in STEP_NAMES:
		step_btn2.add_item(t2)
	step_btn2.item_selected.connect(func(i: int) -> void: step_i = i)
	sr2.add_child(step_btn2)
	o11.add_child(sr2)
	var mr2 := HBoxContainer.new()
	mr2.add_child(_btn("Girar (R)", func() -> void: _sel_rotate()))
	mr2.add_child(_btn("Borrar (Supr)", func() -> void: _delete_sel()))
	mr2.add_child(_btn("Soltar (Esc)", func() -> void: sel = {}))
	o11.add_child(mr2)
	o11.add_child(_lbl("Mayús+clic suma al grupo. Flechas mueven según hacia dónde miras, RePág/AvPág suben/bajan. Con el paso 1/2 o 1/8 solo se mueven las cajas pequeñas (los objetos del catálogo necesitan paso 1 bloque).", 12, UI.DIM, 370.0))


func _build_tab_blocks() -> void:
	var v := _tab("Bloques")
	var sr := LineEdit.new()
	sr.placeholder_text = "Buscar bloque…"
	v.add_child(sr)
	swatch = ColorRect.new()
	swatch.custom_minimum_size = Vector2(0, 26)
	v.add_child(swatch)
	block_grid = GridContainer.new()
	block_grid.columns = 6
	block_grid.add_theme_constant_override("h_separation", 3)
	block_grid.add_theme_constant_override("v_separation", 3)
	v.add_child(block_grid)
	for b in range(1, world.block_count()):
		var btn := Button.new()
		btn.custom_minimum_size = Vector2(48, 40)
		btn.tooltip_text = "%d · %s" % [b, BLOCK_NAMES[b] if b < BLOCK_NAMES.size() else "?"]
		var col: Color = world.block_color(b)
		var sb := UI.box(col, col.lightened(0.35), 1, 2)
		btn.add_theme_stylebox_override("normal", sb)
		btn.add_theme_stylebox_override("hover", UI.box(col.lightened(0.15), Color.WHITE, 2, 2))
		btn.add_theme_stylebox_override("pressed", UI.box(col, Color.WHITE, 2, 2))
		btn.text = ""
		var bb := b
		btn.pressed.connect(func() -> void: set_block(bb))
		btn.set_meta("name", String(BLOCK_NAMES[b]).to_lower() if b < BLOCK_NAMES.size() else "")
		block_grid.add_child(btn)
	sr.text_changed.connect(func(t: String) -> void:
		var q := t.strip_edges().to_lower()
		for c in block_grid.get_children():
			c.visible = q == "" or q in String(c.get_meta("name")))


func _build_tab_catalog() -> void:
	var v := _tab("Objetos")
	cat_search = LineEdit.new()
	cat_search.placeholder_text = "Buscar objeto (ventana, cama, farol…)"
	cat_search.text_changed.connect(func(_t: String) -> void: _fill_catalog())
	v.add_child(cat_search)
	cat_group = OptionButton.new()
	for g in GROUPS:
		cat_group.add_item(g)
	cat_group.item_selected.connect(func(_i: int) -> void: _fill_catalog())
	v.add_child(cat_group)
	cat_list = ItemList.new()
	cat_list.custom_minimum_size = Vector2(0, 420)
	cat_list.item_selected.connect(func(i: int) -> void:
		cat_id = int(cat_ids[i])
		cat_rot = 0
		cat_off = Vector3i.ZERO
		set_tool(T_CAT))
	v.add_child(cat_list)
	v.add_child(_lbl("Las ventanas y puertas se colocan dentro de un hueco: primero abre el muro con la herramienta Caja (Vaciar).", 12, UI.DIM, 370.0))


# ---------------------------------------------------------------------------------------------
# listas
# ---------------------------------------------------------------------------------------------

func _fill_catalog() -> void:
	if cat_list == null:
		return
	cat_list.clear()
	cat_ids.clear()
	var q := cat_search.text.strip_edges().to_lower()
	var g: String = GROUPS[cat_group.selected]
	var ids: Array = cat_items.keys()
	ids.sort()
	for id in ids:
		var c: Dictionary = cat_items[id]
		if g != "Todos" and String(c["group"]) != g:
			continue
		if q != "" and q not in String(c["name"]).to_lower():
			continue
		cat_list.add_item("%s   ·   %s   (%dx%dx%d)" % [c["name"], c["group"], c["w"], c["d"], c["h"]])
		cat_ids.append(id)


func _fill_sites() -> void:
	if site_list == null:
		return
	site_list.clear()
	site_ids.clear()
	var q := site_search.text.strip_edges().to_lower()
	var f: int = site_filter.selected
	var n := sites.size() / 9
	for i in range(n):
		var g := kind_group(sites[i * 9 + 1])
		if f > 0 and g != f - 1:
			continue
		var lab := String(site_labels[i])
		if q != "" and q not in lab.to_lower():
			continue
		site_list.add_item("%s   (%d, %d)" % [lab, sites[i * 9 + 2], sites[i * 9 + 3]])
		site_ids.append(i)
		if site_ids.size() > 3000:
			break


func _refresh_notes() -> void:
	note_list.clear()
	for n in notes:
		note_list.add_item("(%d, %d, %d) %s" % [int(n["x"]), int(n["y"]), int(n["z"]), n["text"]])


func _refresh_all() -> void:
	set_tool(tool)
	set_block(block)
	_refresh_notes()


# ---------------------------------------------------------------------------------------------
# herramientas y estado
# ---------------------------------------------------------------------------------------------

func set_tool(t: int) -> void:
	_end_txn()
	tool = t
	has_a = false
	if t != T_MOVE and t != T_SELECT:
		sel = {}
	sel_a_set = false
	for i in range(tool_buttons.size()):
		tool_buttons[i].button_pressed = i == t
		tool_opts[i].visible = i == t
	if t == T_CAT:
		var nm: Label = tool_opts[T_CAT].get_node("CatName")
		var c: Dictionary = cat_items.get(cat_id, {})
		nm.text = "Objeto: %s" % c.get("name", "(elige uno en Catálogo)")
	if t == T_PASTE:
		var sz: Vector3i = world.clipboard_size()
		paste_label.text = "Portapapeles: %d x %d x %d bloques" % [sz.x, sz.y, sz.z] if sz.x > 0 else "Portapapeles vacío: copia algo con Caja → Copiar la región, o desde la pestaña Estructura."
	help_label.text = TOOL_HELP[t] if help_on else ""
	tabs.current_tab = 0 if t != T_CAT else tabs.current_tab


func set_block(b: int) -> void:
	block = clampi(b, 1, world.block_count() - 1)
	var nm: String = BLOCK_NAMES[block] if block < BLOCK_NAMES.size() else "?"
	block_label.text = "Bloque: %s  (id %d)" % [nm, block]
	swatch.color = world.block_color(block)
	recent.erase(block)
	recent.push_front(block)
	if recent.size() > 8:
		recent.pop_back()


func _cycle_block(d: int) -> void:
	var b := block + d
	if b < 1:
		b = world.block_count() - 1
	if b >= world.block_count():
		b = 1
	set_block(b)


func _block_value() -> int:
	return block | (SLAB if slab else 0)


func _say(t: String, secs := 4.0) -> void:
	msg_label.text = t
	msg_t = secs


func do_undo() -> void:
	_end_txn()
	if world.edit_undo():
		_changed()
		_say("Deshecho")
	else:
		_say("Nada que deshacer")


func do_redo() -> void:
	_end_txn()
	if world.edit_redo():
		_changed()
		_say("Rehecho")
	else:
		_say("Nada que rehacer")


func _begin_txn() -> void:
	if not txn:
		world.edit_begin()
		txn = true


func _end_txn() -> void:
	if txn:
		txn = false
		var r: Dictionary = world.edit_commit()
		if r.get("changed", false):
			_changed()


func _changed() -> void:
	dirty_save = true
	save_t = 2.0


func _flush() -> void:
	world.edit_flush()
	dirty_save = true
	save_t = 2.0


# ---------------------------------------------------------------------------------------------
# bucle
# ---------------------------------------------------------------------------------------------

func _process(delta: float) -> void:
	if rmb_down and not Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
		rmb_down = false
	if map_open:
		return
	_fly(delta)
	_rotate_cam_keys(delta)
	var P: Node3D = main.player
	P.global_position = cam.global_position - Vector3(0, 1.0, 0)
	cam.rotation = Vector3(pitch, yaw, 0)
	_update_hit()
	_lines.clear()
	_glines.clear()
	_fills.clear()
	_draw_tool()
	_flush_overlay()
	_update_info()
	if held != 0 and not map_open:
		repeat_t -= delta
		if repeat_t <= 0.0:
			_repeat()
	if msg_t > 0.0:
		msg_t -= delta
		if msg_t <= 0.0:
			msg_label.text = ""
	if save_t > 0.0:
		save_t -= delta
		if save_t <= 0.0 and not txn and held == 0:
			_save_now()
	stats_t -= delta
	if stats_t <= 0.0:
		stats_t = 0.5
		_update_stats()
	barrier_t -= delta
	if show_barriers and barrier_t <= 0.0:
		barrier_t = 0.7
		_update_barriers()
	var vs := get_viewport().get_visible_rect().size
	msg_label.position = Vector2(10, vs.y - 112)
	help_label.position = Vector2(10, vs.y - 74)


func _fly(delta: float) -> void:
	var f := get_viewport().gui_get_focus_owner()
	if f is LineEdit or f is SpinBox or Input.is_physical_key_pressed(KEY_CTRL):
		return
	var d := Vector3.ZERO
	var fw := Vector3(-sin(yaw) * cos(pitch), sin(pitch), -cos(yaw) * cos(pitch))
	var rt := Vector3(cos(yaw), 0, -sin(yaw))
	if Input.is_physical_key_pressed(KEY_W):
		d += fw
	if Input.is_physical_key_pressed(KEY_S):
		d -= fw
	if Input.is_physical_key_pressed(KEY_D):
		d += rt
	if Input.is_physical_key_pressed(KEY_A):
		d -= rt
	if Input.is_physical_key_pressed(KEY_SPACE) or Input.is_physical_key_pressed(KEY_E):
		d += Vector3.UP
	if Input.is_physical_key_pressed(KEY_C) or Input.is_physical_key_pressed(KEY_Q):
		d -= Vector3.UP
	if d != Vector3.ZERO:
		var sp := speed * (4.0 if Input.is_physical_key_pressed(KEY_SHIFT) else 1.0)
		cam.global_position += d.normalized() * sp * delta
	cam.global_position.y = clampf(cam.global_position.y, 100.6, 400.0)


func _mouse_pos() -> Vector2:
	if captured:
		return get_viewport().get_visible_rect().size * 0.5
	return get_viewport().get_mouse_position()


func _over_ui() -> bool:
	return not captured and get_viewport().gui_get_hovered_control() != null


func _ray_flags() -> int:
	var f := 1
	if show_barriers:
		f |= 2
	match tool:
		T_DETAIL:
			f |= 12
		T_FINE:
			f |= 4
		T_CAT:
			f |= 12
		T_MOVE, T_SELECT:
			f |= 12
	return f


func _update_hit() -> void:
	if _over_ui():
		hit = {}
		return
	var mp := _mouse_pos()
	var o := cam.project_ray_origin(mp)
	var d := cam.project_ray_normal(mp)
	hit = world.edit_ray(o, d, MAX_REACH, _ray_flags())


# ---------------------------------------------------------------------------------------------
# entrada
# ---------------------------------------------------------------------------------------------

func _typing() -> bool:
	var f := get_viewport().gui_get_focus_owner()
	return f is LineEdit


func _unhandled_input(e: InputEvent) -> void:
	if not active or map_open:
		return
	if e is InputEventMouseMotion:
		if captured or ((mmb_down or rmb_down) and not _over_ui()):
			var s: float = float(main.cfg["sens"]) * 0.0025
			yaw -= e.relative.x * s
			pitch = clampf(pitch - e.relative.y * s, -1.5, 1.5)
			if mmb_down:
				mmb_moved += e.relative.length()
			if rmb_down:
				rmb_moved += e.relative.length()
		return
	if e is InputEventMouseButton:
		if _over_ui():
			return
		if e.button_index == MOUSE_BUTTON_MIDDLE:
			if e.pressed:
				mmb_down = true
				mmb_moved = 0.0
			else:
				mmb_down = false
				if mmb_moved < 6.0:
					_eyedrop()
			return
		if e.pressed and (e.button_index == MOUSE_BUTTON_WHEEL_UP or e.button_index == MOUSE_BUTTON_WHEEL_DOWN):
			_wheel(1 if e.button_index == MOUSE_BUTTON_WHEEL_UP else -1)
			return
		if e.button_index == MOUSE_BUTTON_RIGHT and not captured:
			# clic derecho: mantener y arrastrar gira la camara; un clic corto hace la accion secundaria
			if e.pressed:
				rmb_down = true
				rmb_moved = 0.0
			else:
				if rmb_down and rmb_moved < 6.0:
					_action_down(2)
					_action_up(2)
				rmb_down = false
			return
		if e.button_index == MOUSE_BUTTON_LEFT or e.button_index == MOUSE_BUTTON_RIGHT:
			var b := 1 if e.button_index == MOUSE_BUTTON_LEFT else 2
			if e.pressed:
				_action_down(b)
			elif held == b:
				_action_up(b)
		return
	if e is InputEventKey and e.pressed and not e.echo:
		if _typing() or e.physical_keycode == KEY_F9:
			return
		get_viewport().set_input_as_handled()
		var ctrl: bool = e.ctrl_pressed
		match e.physical_keycode:
			KEY_TAB:
				_set_captured(not captured)
			KEY_ESCAPE:
				if not sel.is_empty():
					sel = {}
				elif captured:
					_set_captured(false)
			KEY_Z:
				if ctrl:
					if e.shift_pressed:
						do_redo()
					else:
						do_undo()
			KEY_Y:
				if ctrl:
					do_redo()
			KEY_S:
				if ctrl:
					save_doc()
			KEY_G:
				grid_on = not grid_on
				_say("Cuadrícula: " + ("sí" if grid_on else "no"))
			KEY_H:
				help_on = not help_on
				help_label.text = TOOL_HELP[tool] if help_on else ""
			KEY_R:
				if sel.get("type", "") == "group":
					_sel_rotate()
				elif sel.get("type", "") == "placed":
					_placed_move(Vector3i.ZERO, 1)
				elif tool == T_PASTE:
					paste_rot = (paste_rot + 1) % 4
				elif tool == T_STAMP:
					stamp_rot = (stamp_rot + 1) % 4
				elif tool == T_CAT:
					cat_rot = (cat_rot + 1) % 4
			KEY_BRACKETLEFT:
				_cycle_block(-1)
			KEY_BRACKETRIGHT:
				_cycle_block(1)
			KEY_DELETE:
				if not sel.is_empty():
					_delete_sel()
				elif _hit_ok() and hit["kind"] != "block":
					_begin_txn()
					world.edit_erase_pick(hit)
					_flush()
					_end_txn()
					_say("Detalle borrado")
			KEY_V:
				step_i = (step_i + 1) % STEPS.size()
				if step_btn:
					step_btn.selected = step_i
				if step_btn2:
					step_btn2.selected = step_i
				_say("Paso: " + STEP_NAMES[step_i], 2.0)
			KEY_T:
				if not ctrl:
					set_tool(T_SELECT)
			KEY_X:
				_decompose()
			KEY_1, KEY_2, KEY_3, KEY_4, KEY_5, KEY_6, KEY_7, KEY_8, KEY_9:
				if not ctrl:
					set_tool(int(e.physical_keycode) - int(KEY_1))
			KEY_0:
				if not ctrl:
					set_tool(T_MOVE)
			KEY_MINUS:
				if not ctrl:
					set_tool(T_STAMP)


func _wheel(dir: int) -> void:
	match tool:
		T_BRUSH:
			brush_n = clampi(brush_n + dir, 1, 15)
			var sp: SpinBox = tool_opts[T_BRUSH].get_node("BrushSize") if tool_opts[T_BRUSH].has_node("BrushSize") else null
			_say("Tamaño del pincel: %d" % brush_n, 1.5)
		T_FINE:
			var sizes := [1, 2, 4, 8]
			var i: int = sizes.find(fine_size)
			fine_size = sizes[clampi(i + dir, 0, 3)]
			_say("Voxel fino: %d/8" % fine_size, 1.5)
		T_CAT:
			cat_rot = (cat_rot + (1 if dir > 0 else 3)) % 4
		T_PASTE:
			paste_rot = (paste_rot + (1 if dir > 0 else 3)) % 4
		T_STAMP:
			stamp_rot = (stamp_rot + (1 if dir > 0 else 3)) % 4
		_:
			_cycle_block(dir)


func _eyedrop() -> void:
	if not _hit_ok():
		return
	var k: String = hit["kind"]
	if k == "block":
		var rb: int = int(hit["block"]) & 0x7f
		if rb > 0 and rb != 89:
			set_block(rb)
			slab = (int(hit["block"]) & SLAB) != 0
			_say("Bloque: %s" % BLOCK_NAMES[block])
	elif k == "abox":
		var c: Vector3i = hit["color"]
		fine_color = Color8(c.x, c.y, c.z)
		fine_glow = bool(hit.get("glow", false))
		fine_pat = int(hit.get("pat", 0))
		_say("Color copiado del detalle")


func _action_down(b: int) -> void:
	held = b
	repeat_t = 0.0
	last_cell = Vector3i(-999999, 0, 0)
	if not _hit_ok() and tool != T_PASTE:
		return
	match tool:
		T_BLOCK, T_BRUSH, T_FINE:
			_begin_txn()
			_do_hold_action(b)
			repeat_t = 0.22
		T_BOX:
			_box_click(b)
		T_DETAIL:
			_detail_click(b)
		T_CAT:
			_cat_click(b)
		T_STRUCT:
			_struct_click(b)
		T_PASTE:
			_paste_click()
		T_INSPECT:
			_inspect_click()
		T_MOVE:
			_move_click(b)
		T_SELECT:
			_select_click(b)
		T_STAMP:
			_stamp_click(b)


func _action_up(_b: int) -> void:
	held = 0
	_end_txn()


func _repeat() -> void:
	repeat_t = 0.18
	if not _hit_ok():
		return
	if tool == T_BLOCK or tool == T_BRUSH or tool == T_FINE:
		_do_hold_action(held)


func _do_hold_action(b: int) -> void:
	if not _hit_ok():
		return
	var cell: Vector3i = hit["cell"]
	var adj: Vector3i = hit["adj"]
	if b == 1 and tool != T_FINE and cell.y < FLAT_Y:
		_say("El suelo no se toca: construye sobre él", 2.0)
		return
	var key_cell: Vector3i = adj if (b == 2 or tool == T_FINE) else cell
	if key_cell == last_cell and tool != T_FINE:
		return
	match tool:
		T_BLOCK:
			if b == 1:
				if hit["kind"] == "block":
					world.edit_set_cubes(cell, cell, 0, 0, 5, 0)
					last_cell = key_cell
			else:
				world.edit_set_cubes(adj, adj, _block_value(), 0, 0, 0)
				last_cell = key_cell
		T_BRUSH:
			var c: Vector3i = cell if b == 1 else adj
			var h := brush_n / 2
			var mn := c - Vector3i(h, h, h)
			var mx := mn + Vector3i(brush_n - 1, brush_n - 1, brush_n - 1)
			if brush_mode == 0:
				if b == 1:
					world.edit_set_cubes(mn, mx, 0, brush_shape, 5, 0)
				else:
					world.edit_set_cubes(mn, mx, _block_value(), brush_shape, 1, 0)
			else:
				if b == 1:
					world.edit_set_cubes(mn, mx, _block_value(), brush_shape, 2, 0)
				else:
					world.edit_set_cubes(mn, mx, 0, brush_shape, 4, 0)
			last_cell = key_cell
		T_FINE:
			if b == 1:
				var f := _fine_box()
				if f.is_empty():
					return
				var key := Vector3i(int(floor(f[0].x * 8)), int(floor(f[0].y * 8)), int(floor(f[0].z * 8)))
				if key == last_cell:
					return
				last_cell = key
				world.edit_add_fine(f[0], f[1], int(fine_color.r8), int(fine_color.g8), int(fine_color.b8), fine_pat, fine_glow)
			else:
				if hit["kind"] == "abox" or hit["kind"] == "deco":
					world.edit_erase_pick(hit)
	_flush()


func _fine_box() -> Array:
	if not _hit_ok():
		return []
	var p: Vector3 = hit["point"]
	var n: Vector3i = hit["normal"]
	var g: float = fine_size / 8.0
	var q := p + Vector3(n) * (g * 0.5)
	var mn := Vector3(floor(q.x / g) * g, floor(q.y / g) * g, floor(q.z / g) * g)
	return [mn, mn + Vector3(g, g, g)]


func _box_click(b: int) -> void:
	if b == 2:
		has_a = false
		return
	if not _hit_ok() or hit["kind"] != "block" and box_action != 4 and box_action != 5:
		if not _hit_ok():
			return
	var c: Vector3i = hit["cell"]
	if not has_a:
		box_a = c
		has_a = true
		_say("Esquina A: (%d, %d, %d) · ahora apunta a la esquina B" % [c.x, c.y, c.z], 6.0)
		return
	has_a = false
	var mn := Vector3i(mini(box_a.x, c.x), mini(box_a.y, c.y), mini(box_a.z, c.z))
	var mx := Vector3i(maxi(box_a.x, c.x), maxi(box_a.y, c.y), maxi(box_a.z, c.z))
	var vol := (mx.x - mn.x + 1) * (mx.y - mn.y + 1) * (mx.z - mn.z + 1)
	if vol > 600000 and box_action != 4 and box_action != 5 and box_action != 6:
		_say("Caja demasiado grande (%d bloques, máximo 600000)" % vol)
		return
	_begin_txn()
	var n := 0
	match box_action:
		0:
			n = world.edit_set_cubes(mn, mx, _block_value(), 0, 0, 0)
		1:
			n = world.edit_set_cubes(mn, mx, 0, 0, 5, 0)
		2:
			var src: int = world.edit_block_at(box_a.x, box_a.y, box_a.z)
			n = world.edit_set_cubes(mn, mx, _block_value(), 0, 3, maxi(src, 0))
		3:
			n = world.edit_set_cubes(mn, mx, 0, 0, 4, 0)
		4:
			n = world.edit_erase_region(Vector3(mn), Vector3(mx) + Vector3.ONE)
		5:
			n = world.edit_restore_region(Vector3(mn), Vector3(mx) + Vector3.ONE)
		6:
			n = world.copy_region(mn, mx)
		7:
			n = world.edit_set_cubes(mn, mx, _block_value(), 0, 1, 0)
		8:
			n = world.edit_set_cubes(mn, mx, _block_value(), 0, 2, 0)
		9:
			sel = {"type": "region", "mn": mn, "mx": mx}
	_flush()
	_end_txn()
	if box_action == 9:
		set_tool(T_MOVE)
		_say("Región elegida (%d x %d x %d). Flechas: mover · Mayús+flecha: extender · Ctrl+flecha: achicar" % [mx.x - mn.x + 1, mx.y - mn.y + 1, mx.z - mn.z + 1], 7.0)
	elif box_action == 6:
		_say("Copiados %d elementos (%d x %d x %d). Herramienta Pegar (8)." % [n, mx.x - mn.x + 1, mx.y - mn.y + 1, mx.z - mn.z + 1])
		set_tool(T_PASTE)
	else:
		_say("%s: %d cambios" % [BOX_ACTIONS[box_action], n])


func _detail_click(b: int) -> void:
	if not _hit_ok():
		return
	if b == 1:
		if hit["kind"] == "block":
			_say("Eso es un bloque: usa la herramienta Bloque. Apunta a un detalle (marco, cristal, mueble…)")
			return
		_begin_txn()
		world.edit_erase_pick(hit)
		_flush()
		_end_txn()
		_say("Detalle borrado (Ctrl+Z para deshacer)")
	else:
		var c: Vector3i = hit["cell"]
		_begin_txn()
		var n: int = world.edit_restore_region(Vector3(c) - Vector3(1.5, 1.5, 1.5), Vector3(c) + Vector3(2.5, 2.5, 2.5))
		_flush()
		_end_txn()
		_say("Restaurados %d detalles" % n)


func _cat_pose() -> Dictionary:
	if not _hit_ok():
		return {}
	var c: Dictionary = cat_items.get(cat_id, {})
	if c.is_empty():
		return {}
	var n: Vector3i = hit["normal"]
	var rot := cat_rot
	var grp := String(c["group"])
	var wallish := grp in ["Ventanas", "Puertas"] or cat_id in [153, 157, 136, 137]
	if cat_auto and wallish and n.y == 0 and (n.x != 0 or n.z != 0):
		rot = 0 if n.z < 0 else (1 if n.x > 0 else (2 if n.z > 0 else 3))
	var dims: Vector3i = world.catalog_dims(cat_id, rot)
	var cell: Vector3i = hit["cell"]
	var adj: Vector3i = hit["adj"]
	var base: Vector3i = adj
	var inside: bool = cat_inside and wallish and n.y == 0 and hit["kind"] == "block"
	if inside:
		base = cell
	var pos := Vector3(base)
	if bool(c["deco"]):
		pass
	else:
		pos.x = base.x - dims.x / 2
		pos.z = base.z - dims.z / 2
		if inside:
			# la profundidad (1) cae en la capa del muro apuntado
			if rot == 0 or rot == 2:
				pos.z = base.z
			else:
				pos.x = base.x
	if n.y > 0 and hit["kind"] == "block" and (int(hit["block"]) & SLAB) != 0:
		pos.y -= 0.5
	pos += Vector3(cat_off)
	return {"pos": pos, "rot": rot, "dims": dims}


func _cat_click(b: int) -> void:
	if not _hit_ok():
		return
	if b == 2:
		if hit["kind"] == "block":
			return
		_begin_txn()
		world.edit_erase_pick(hit)
		_flush()
		_end_txn()
		_say("Objeto o detalle quitado")
		return
	var pz := _cat_pose()
	if pz.is_empty():
		return
	_begin_txn()
	var id: int = world.edit_place(cat_id, pz["pos"], int(pz["rot"]), 0, 0, cat_solid)
	_flush()
	_end_txn()
	if id > 0:
		_say("Colocado: %s" % cat_items[cat_id]["name"], 2.0)


func _struct_click(b: int) -> void:
	if b == 2:
		sel_piece = {}
		_update_struct_label()
		return
	if not _hit_ok():
		return
	var p: Vector3 = hit["point"]
	var info: Dictionary = world.piece_at(p - Vector3(hit["normal"]) * 0.2)
	if info.is_empty():
		_say("Ahí no hay ninguna estructura")
		return
	sel_piece = info
	_update_struct_label()
	tabs.current_tab = 4
	_say("Elegida: %s" % info["label"])


func select_site(i: int) -> void:
	var idx: int = sites[i * 9]
	sel_piece = world.piece_info(idx)
	_update_struct_label()


func _update_struct_label() -> void:
	if sel_piece.is_empty():
		struct_label.text = "Ninguna estructura elegida.\nUsa la herramienta Estructura (7) o el mapa."
		return
	var s: Dictionary = sel_piece
	var fl := int(world.edit_get_piece_flags(int(s["idx"])))
	s["flags"] = fl
	var t := "%s\nÍndice %d · bloques (%d,%d)-(%d,%d) · suelo y=%d\nRotación %d · ruina %.2f" % [s["label"], s["idx"], s["x0"], s["z0"], s["x1"], s["z1"], s["y"], s["rot"], s["decay"]]
	if bool(s.get("is_bld", false)):
		t += "\nAberturas: %d · objetos: %d · plantas: %d · chimenea: %s" % [s["openings"], s["items"], s["storeys"], "sí" if s["has_chimney"] else "no"]
	var parts := []
	if fl & 8:
		parts.append("OCULTA")
	if fl & 1:
		parts.append("sin ventanas/puertas")
	if fl & 2:
		parts.append("sin muebles")
	if fl & 4:
		parts.append("sin chimenea")
	t += "\nEstado: %s" % (", ".join(parts) if parts.size() > 0 else "como la genera el juego")
	struct_label.text = t


func _set_flags(f: int) -> void:
	if sel_piece.is_empty():
		_say("Elige primero una estructura")
		return
	var isb := bool(sel_piece.get("is_bld", false))
	if f in [1, 2, 4, 7] and not isb:
		_say("Esta estructura solo se puede ocultar o restaurar")
		return
	var cur: int = world.edit_get_piece_flags(int(sel_piece["idx"]))
	var nf := f
	if f in [1, 2, 4]:
		nf = (cur & 7) ^ f   # alternar ese ajuste y conservar los otros
	_begin_txn()
	world.edit_set_piece_flags(int(sel_piece["idx"]), nf)
	_flush()
	_end_txn()
	_update_struct_label()
	_say("Estructura actualizada (los chunks se regeneran en un instante)")


func _paste_click() -> void:
	var sz: Vector3i = world.clipboard_size()
	if sz.x == 0:
		_say("El portapapeles está vacío")
		return
	if not _hit_ok():
		return
	var adj: Vector3i = hit["adj"]
	_begin_txn()
	var n: int = world.paste_region(adj + Vector3i(cat_off), paste_rot, paste_air or Input.is_physical_key_pressed(KEY_SHIFT))
	_flush()
	_end_txn()
	_say("Pegados %d elementos" % n)


func _inspect_click() -> void:
	if not _hit_ok():
		return
	var c: Vector3i = hit["cell"]
	DisplayServer.clipboard_set("%d %d %d" % [c.x, c.y, c.z])
	_say("Coordenadas copiadas: %d %d %d" % [c.x, c.y, c.z])


# ---------------------------------------------------------------------------------------------
# flechas, seleccion, mover y extender
# ---------------------------------------------------------------------------------------------

func has_selection() -> bool:
	return not sel.is_empty() or tool == T_CAT or tool == T_PASTE or tool == T_STAMP


func _snap_axis(v: Vector3) -> Vector3i:
	if absf(v.x) > absf(v.z):
		return Vector3i(int(signf(v.x)), 0, 0)
	return Vector3i(0, 0, int(signf(v.z)))


func _arrow_dir(k: int) -> Vector3i:
	var fw := _snap_axis(Vector3(-sin(yaw), 0, -cos(yaw)))
	var rt := _snap_axis(Vector3(cos(yaw), 0, -sin(yaw)))
	match k:
		KEY_UP:
			return fw
		KEY_DOWN:
			return -fw
		KEY_RIGHT:
			return rt
		KEY_LEFT:
			return -rt
		KEY_PAGEUP:
			return Vector3i(0, 1, 0)
		KEY_PAGEDOWN:
			return Vector3i(0, -1, 0)
	return Vector3i.ZERO


func _focus_typing() -> bool:
	var f := get_viewport().gui_get_focus_owner()
	return f is LineEdit or f is SpinBox or f is TextEdit


func _input(e: InputEvent) -> void:
	if not active or map_open:
		return
	if not (e is InputEventKey) or not e.pressed:
		return
	var k: int = e.physical_keycode
	if k != KEY_LEFT and k != KEY_RIGHT and k != KEY_UP and k != KEY_DOWN and k != KEY_PAGEUP and k != KEY_PAGEDOWN and k != KEY_HOME:
		return
	if _focus_typing():
		return
	get_viewport().set_input_as_handled()
	if e.echo:
		var now := Time.get_ticks_msec()
		if now - arrow_ms < 90:
			return
		arrow_ms = now
	else:
		arrow_ms = Time.get_ticks_msec()
	if not has_selection():
		return   # sin nada elegido las flechas giran la camara (en _process)
	if sel.is_empty():
		# objeto del catalogo / pegado: mueve la posicion de la sombra
		if k == KEY_HOME:
			cat_off = Vector3i.ZERO
		else:
			cat_off += _arrow_dir(k)
		return
	if k == KEY_HOME:
		return
	_sel_key(k, e.shift_pressed, e.ctrl_pressed)


func _rotate_cam_keys(delta: float) -> void:
	if has_selection() or _focus_typing():
		return
	var rs := 1.9 * delta * (2.2 if Input.is_physical_key_pressed(KEY_SHIFT) else 1.0)
	if Input.is_physical_key_pressed(KEY_LEFT):
		yaw += rs
	if Input.is_physical_key_pressed(KEY_RIGHT):
		yaw -= rs
	if Input.is_physical_key_pressed(KEY_UP):
		pitch = clampf(pitch + rs, -1.5, 1.5)
	if Input.is_physical_key_pressed(KEY_DOWN):
		pitch = clampf(pitch - rs, -1.5, 1.5)


func _sel_key(k: int, shift: bool, ctrl: bool) -> void:
	var d := _arrow_dir(k)
	var mode := 1 if shift else (2 if ctrl else 0)
	match String(sel.get("type", "")):
		"box":
			_box_apply(d, mode)
		"placed":
			if mode != 0:
				_say("Los objetos del catálogo solo se mueven y giran. Con X los descompones en cajas que sí se pueden extender y achicar.", 5.0)
			else:
				_placed_move(d, 0)
		"region":
			_region_apply(d, mode)
		"group":
			if mode != 0:
				_say("Un grupo solo se mueve y se gira. Para cambiar el tamaño de una pieza usa la opción «Una sola pieza».", 5.0)
			else:
				_group_move(d)


func _move_click(b: int) -> void:
	if b == 2:
		sel = {}
		return
	if not _hit_ok():
		sel = {}
		return
	var k: String = hit["kind"]
	if k == "block":
		var c: Vector3i = hit["cell"]
		if Input.is_physical_key_pressed(KEY_SHIFT) and sel.get("type", "") == "region":
			var a: Vector3i = sel["mn"]
			var z: Vector3i = sel["mx"]
			sel = {"type": "region", "mn": Vector3i(mini(a.x, c.x), mini(a.y, c.y), mini(a.z, c.z)), "mx": Vector3i(maxi(z.x, c.x), maxi(z.y, c.y), maxi(z.z, c.z))}
		else:
			sel = {"type": "region", "mn": c, "mx": c}
		return
	var pid := int(hit.get("placed_id", 0))
	if pid > 0:
		_select_placed(pid)
		return
	if k == "abox":
		var col: Vector3i = hit["color"]
		sel = {"type": "box", "mn": Vector3(hit["bmin"]), "mx": Vector3(hit["bmax"]), "col": col, "pat": int(hit["pat"]), "glow": bool(hit["glow"]), "fine_id": int(hit["fine_id"])}
	else:
		_begin_txn()
		var id: int = world.edit_adopt_deco(hit)
		_flush()
		_end_txn()
		if id > 0:
			_select_placed(id)
		else:
			_say("Ese detalle no se puede mover. Bórralo y ponlo desde el Catálogo.", 5.0)


func _select_placed(id: int) -> void:
	var p: Dictionary = world.edit_get_placed(id)
	if p.is_empty():
		return
	sel = {"type": "placed", "id": id}


func _box_apply(d: Vector3i, mode: int) -> void:
	var s: float = STEPS[step_i]
	var mn: Vector3 = sel["mn"]
	var mx: Vector3 = sel["mx"]
	var nmn := mn
	var nmx := mx
	var dv := Vector3(d)
	var pos_dir: bool = d.x + d.y + d.z > 0
	match mode:
		0:
			nmn += dv * s
			nmx += dv * s
		1:
			if pos_dir:
				nmx += dv * s
			else:
				nmn += dv * s
		2:
			if pos_dir:
				nmx -= dv * s
			else:
				nmn -= dv * s
	if nmx.x - nmn.x < 0.1 or nmx.y - nmn.y < 0.1 or nmx.z - nmn.z < 0.1:
		_say("Ya no se puede achicar más en esa dirección", 2.0)
		return
	var col: Vector3i = sel["col"]
	_begin_txn()
	world.edit_erase_pick({"hit": true, "kind": "abox", "bmin": mn, "bmax": mx, "placed_id": 0, "fine_id": int(sel["fine_id"])})
	var id: int = world.edit_add_fine(nmn, nmx, col.x, col.y, col.z, int(sel["pat"]), bool(sel["glow"]))
	_flush()
	_end_txn()
	sel["mn"] = nmn
	sel["mx"] = nmx
	sel["fine_id"] = id


func _placed_move(d: Vector3i, rot_add: int) -> void:
	var p: Dictionary = world.edit_get_placed(int(sel["id"]))
	if p.is_empty():
		sel = {}
		return
	var s: float = STEPS[step_i]
	var pos: Vector3 = p["pos"]
	var dv := Vector3(d)
	if bool(p["deco"]):
		pos += Vector3(dv.x * maxf(1.0, s), dv.y * (0.5 if s < 1.0 else 1.0), dv.z * maxf(1.0, s))
	else:
		pos += dv * s
	_begin_txn()
	var id: int = world.edit_move_placed(int(sel["id"]), pos, (int(p["rot"]) + rot_add) % 4)
	_flush()
	_end_txn()
	if id > 0:
		sel["id"] = id


func _region_apply(d: Vector3i, mode: int) -> void:
	var mn: Vector3i = sel["mn"]
	var mx: Vector3i = sel["mx"]
	var si := maxi(1, int(round(STEPS[step_i])))
	var pos_dir: bool = d.x + d.y + d.z > 0
	_begin_txn()
	match mode:
		0:
			world.copy_region(mn, mx)
			world.edit_set_cubes(mn, mx, 0, 0, 5, 0)
			world.edit_erase_region(Vector3(mn), Vector3(mx) + Vector3.ONE)
			world.paste_region(mn + d * si, 0, false)
			mn += d * si
			mx += d * si
		1:
			# extruir: se repite la capa del borde en esa direccion
			var smn := mn
			var smx := mx
			if d.x != 0:
				smn.x = mx.x if pos_dir else mn.x
				smx.x = smn.x
			elif d.y != 0:
				smn.y = mx.y if pos_dir else mn.y
				smx.y = smn.y
			else:
				smn.z = mx.z if pos_dir else mn.z
				smx.z = smn.z
			world.copy_region(smn, smx)
			for k in range(1, si + 1):
				world.paste_region(smn + d * k, 0, false)
			if pos_dir:
				mx += d * si
			else:
				mn += d * si
		2:
			var size := mx - mn + Vector3i.ONE
			var ax := 0 if d.x != 0 else (1 if d.y != 0 else 2)
			if size[ax] <= si:
				_say("La región ya no se puede achicar más en esa dirección", 2.0)
				_end_txn()
				return
			var cmn := mn
			var cmx := mx
			if pos_dir:
				cmn[ax] = mx[ax] - si + 1
				mx[ax] -= si
			else:
				cmx[ax] = mn[ax] + si - 1
				mn[ax] += si
			world.edit_set_cubes(cmn, cmx, 0, 0, 5, 0)
			world.edit_erase_region(Vector3(cmn), Vector3(cmx) + Vector3.ONE)
	_flush()
	_end_txn()
	sel["mn"] = mn
	sel["mx"] = mx


func _decompose() -> void:
	if sel.get("type", "") != "placed":
		_say("Elige un objeto del catálogo con la herramienta Mover para descomponerlo.", 3.0)
		return
	var p: Dictionary = world.edit_get_placed(int(sel["id"]))
	if p.is_empty() or bool(p["deco"]):
		_say("Ese objeto no se puede descomponer en cajas.", 3.0)
		return
	var arr: PackedFloat32Array = world.catalog_boxes(int(p["cat"]), Vector3(p["pos"]), int(p["rot"]))
	var n := arr.size() / 9
	_begin_txn()
	world.edit_erase_pick({"hit": true, "kind": "abox", "bmin": Vector3.ZERO, "bmax": Vector3.ONE, "placed_id": int(sel["id"]), "fine_id": 0})
	for i in range(n):
		var k := i * 9
		world.edit_add_fine(Vector3(arr[k], arr[k + 1], arr[k + 2]), Vector3(arr[k + 3], arr[k + 4], arr[k + 5]), int(arr[k + 6] * 255.0), int(arr[k + 7] * 255.0), int(arr[k + 8] * 255.0), 0, false)
	_flush()
	_end_txn()
	sel = {}
	_say("Descompuesto en %d cajas: elígelas una a una con Mover para extenderlas o achicarlas." % n, 6.0)


func _delete_sel() -> void:
	match String(sel.get("type", "")):
		"box":
			_begin_txn()
			world.edit_erase_pick({"hit": true, "kind": "abox", "bmin": Vector3(sel["mn"]), "bmax": Vector3(sel["mx"]), "placed_id": 0, "fine_id": int(sel["fine_id"])})
			_flush()
			_end_txn()
		"placed":
			_begin_txn()
			world.edit_erase_pick({"hit": true, "kind": "abox", "bmin": Vector3.ZERO, "bmax": Vector3.ONE, "placed_id": int(sel["id"]), "fine_id": 0})
			_flush()
			_end_txn()
		"group":
			_begin_txn()
			for f in sel["fines"]:
				_gr_erase_fine(f)
			for pid2 in sel["placed"]:
				world.edit_erase_pick({"hit": true, "kind": "abox", "bmin": Vector3.ZERO, "bmax": Vector3.ONE, "placed_id": int(pid2), "fine_id": 0})
			_flush()
			_end_txn()
		"region":
			var mn: Vector3i = sel["mn"]
			var mx: Vector3i = sel["mx"]
			_begin_txn()
			world.edit_set_cubes(mn, mx, 0, 0, 5, 0)
			world.edit_erase_region(Vector3(mn), Vector3(mx) + Vector3.ONE)
			_flush()
			_end_txn()
	sel = {}
	_say("Borrado (Ctrl+Z para deshacer)", 3.0)


# ---------------------------------------------------------------------------------------------
# Seleccionar: grupos de cajas pequeñas y objetos (muebles de las casas)
# ---------------------------------------------------------------------------------------------

func _all_fines() -> Array:
	var out: Array = []
	var ed: Variant = JSON.parse_string(world.export_edits(main.GAME_VERSION))
	if not (ed is Dictionary):
		return out
	for f in ed.get("fine", []):
		out.append(_fine_dict(f))
	return out


func _fine_dict(f: Array) -> Dictionary:
	return {"id": int(f[0]), "mn": Vector3(float(f[1]), float(f[2]), float(f[3])), "mx": Vector3(float(f[4]), float(f[5]), float(f[6])),
		"col": Vector3i(int(f[7]), int(f[8]), int(f[9])), "pat": int(f[10]), "glow": bool(f[11])}


func _all_placed() -> Array:
	var out: Array = []
	var ed: Variant = JSON.parse_string(world.export_edits(main.GAME_VERSION))
	if not (ed is Dictionary):
		return out
	for p in ed.get("placed", []):
		out.append(int(p[0]))
	return out


func _gr_touch(a: Dictionary, b: Dictionary) -> bool:
	var e := 0.02
	var amn: Vector3 = a["mn"]
	var amx: Vector3 = a["mx"]
	var bmn: Vector3 = b["mn"]
	var bmx: Vector3 = b["mx"]
	return amn.x <= bmx.x + e and bmn.x <= amx.x + e and amn.y <= bmx.y + e and bmn.y <= amx.y + e and amn.z <= bmx.z + e and bmn.z <= amx.z + e


func _gr_cluster(fid: int) -> Array:
	var all := _all_fines()
	var start := -1
	for i in range(all.size()):
		if int(all[i]["id"]) == fid:
			start = i
			break
	if start < 0:
		return []
	var res: Array = [all[start]]
	var rest: Array = []
	for i in range(all.size()):
		if i != start:
			rest.append(all[i])
	var qi := 0
	while qi < res.size():
		var cur: Dictionary = res[qi]
		qi += 1
		var keep: Array = []
		for o in rest:
			if _gr_touch(cur, o):
				res.append(o)
			else:
				keep.append(o)
		rest = keep
	return res


func _gr_in_box(mn: Vector3, mx: Vector3) -> Dictionary:
	var fl: Array = []
	for f in _all_fines():
		var c: Vector3 = (Vector3(f["mn"]) + Vector3(f["mx"])) * 0.5
		if c.x >= mn.x and c.x <= mx.x and c.y >= mn.y and c.y <= mx.y and c.z >= mn.z and c.z <= mx.z:
			fl.append(f)
	var pl: Array = []
	for id in _all_placed():
		var p: Dictionary = world.edit_get_placed(id)
		if p.is_empty():
			continue
		var pos: Vector3 = p["pos"]
		var c2: Vector3 = pos + Vector3(p["w"], p["h"], p["d"]) * 0.5
		if c2.x >= mn.x and c2.x <= mx.x and c2.y >= mn.y and c2.y <= mx.y and c2.z >= mn.z and c2.z <= mx.z:
			pl.append(id)
	return {"fines": fl, "placed": pl}


func _group_set(fl: Array, pl: Array, add: bool) -> void:
	if add and sel.get("type", "") == "group":
		var seen := {}
		for f in sel["fines"]:
			seen[int(f["id"])] = true
		for f in fl:
			if not seen.has(int(f["id"])):
				sel["fines"].append(f)
		for id in pl:
			if not sel["placed"].has(id):
				sel["placed"].append(id)
	else:
		sel = {"type": "group", "fines": fl, "placed": pl}
	_group_bounds()
	if sel["fines"].is_empty() and sel["placed"].is_empty():
		sel = {}


func _group_bounds() -> void:
	var mn := Vector3(1e9, 1e9, 1e9)
	var mx := Vector3(-1e9, -1e9, -1e9)
	for f in sel["fines"]:
		mn = mn.min(Vector3(f["mn"]))
		mx = mx.max(Vector3(f["mx"]))
	for id in sel["placed"]:
		var p: Dictionary = world.edit_get_placed(int(id))
		if p.is_empty():
			continue
		var pos: Vector3 = p["pos"]
		mn = mn.min(pos)
		mx = mx.max(pos + Vector3(p["w"], p["h"], p["d"]))
	sel["mn"] = mn
	sel["mx"] = mx


func _gr_erase_fine(f: Dictionary) -> void:
	world.edit_erase_pick({"hit": true, "kind": "abox", "bmin": Vector3(f["mn"]), "bmax": Vector3(f["mx"]), "placed_id": 0, "fine_id": int(f["id"])})


func _gr_add_fine(mn: Vector3, mx: Vector3, f: Dictionary) -> Dictionary:
	var c: Vector3i = f["col"]
	var id: int = world.edit_add_fine(mn, mx, c.x, c.y, c.z, int(f["pat"]), bool(f["glow"]))
	return {"id": id, "mn": mn, "mx": mx, "col": c, "pat": f["pat"], "glow": f["glow"]}


func _select_click(b: int) -> void:
	if b == 2:
		sel = {}
		sel_a_set = false
		return
	if not _hit_ok():
		return
	var add := Input.is_physical_key_pressed(KEY_SHIFT)
	var k: String = hit["kind"]
	if select_mode == 2:
		var c: Vector3i = hit["cell"]
		if not sel_a_set:
			sel_a = c
			sel_a_set = true
			_say("Esquina A lista: ahora apunta a la esquina B y haz clic.", 5.0)
			return
		sel_a_set = false
		var mn := Vector3(mini(sel_a.x, c.x), mini(sel_a.y, c.y), mini(sel_a.z, c.z))
		var mx := Vector3(maxi(sel_a.x, c.x) + 1, maxi(sel_a.y, c.y) + 1, maxi(sel_a.z, c.z) + 1)
		var g := _gr_in_box(mn, mx)
		_group_set(g["fines"], g["placed"], add)
		if sel.is_empty():
			_say("No hay cajas pequeñas ni objetos dentro de esa caja.", 4.0)
		return
	if k == "block":
		var c2: Vector3i = hit["cell"]
		if add and sel.get("type", "") == "region":
			var a: Vector3i = sel["mn"]
			var z: Vector3i = sel["mx"]
			sel = {"type": "region", "mn": Vector3i(mini(a.x, c2.x), mini(a.y, c2.y), mini(a.z, c2.z)), "mx": Vector3i(maxi(z.x, c2.x), maxi(z.y, c2.y), maxi(z.z, c2.z))}
		else:
			sel = {"type": "region", "mn": c2, "mx": c2}
		return
	var pid := int(hit.get("placed_id", 0))
	if pid <= 0 and k != "abox":
		_begin_txn()
		pid = world.edit_adopt_deco(hit)
		_flush()
		_end_txn()
		if pid <= 0:
			_say("Ese detalle no se puede elegir. Bórralo y ponlo desde el Catálogo.", 5.0)
			return
	if pid > 0:
		_group_set([], [pid], add)
		return
	var fid := int(hit["fine_id"])
	if select_mode == 1:
		var one := {"id": fid, "mn": Vector3(hit["bmin"]), "mx": Vector3(hit["bmax"]), "col": Vector3i(hit["color"]), "pat": int(hit["pat"]), "glow": bool(hit["glow"])}
		_group_set([one], [], add)
	else:
		var cl := _gr_cluster(fid)
		if cl.is_empty():
			cl = [{"id": fid, "mn": Vector3(hit["bmin"]), "mx": Vector3(hit["bmax"]), "col": Vector3i(hit["color"]), "pat": int(hit["pat"]), "glow": bool(hit["glow"])}]
		_group_set(cl, [], add)


func _group_move(d: Vector3i) -> void:
	var s: float = STEPS[step_i]
	var dv := Vector3(d) * s
	if not sel["placed"].is_empty() and s < 1.0:
		_say("Hay objetos del catálogo en el grupo: pon el paso en 1 bloque (V).", 4.0)
		return
	var nmn: Vector3 = Vector3(sel["mn"]) + dv
	if nmn.y < float(_fmin().y) - 0.001:
		_say("No se puede bajar del suelo.", 2.0)
		return
	_begin_txn()
	for f in sel["fines"]:
		_gr_erase_fine(f)
	var nf: Array = []
	for f in sel["fines"]:
		nf.append(_gr_add_fine(Vector3(f["mn"]) + dv, Vector3(f["mx"]) + dv, f))
	var np: Array = []
	for id in sel["placed"]:
		var p: Dictionary = world.edit_get_placed(int(id))
		if p.is_empty():
			continue
		var nid: int = world.edit_move_placed(int(id), Vector3(p["pos"]) + dv, int(p["rot"]))
		if nid > 0:
			np.append(nid)
	_flush()
	_end_txn()
	sel["fines"] = nf
	sel["placed"] = np
	_group_bounds()


func _sel_rotate() -> void:
	match String(sel.get("type", "")):
		"placed":
			_placed_move(Vector3i.ZERO, 1)
		"group":
			_group_rotate()
		_:
			_say("Elige un grupo u objeto para girarlo.", 3.0)


func _group_rotate() -> void:
	var c: Vector3 = (Vector3(sel["mn"]) + Vector3(sel["mx"])) * 0.5
	var cx := roundf(c.x)
	var cz := roundf(c.z)
	_begin_txn()
	for f in sel["fines"]:
		_gr_erase_fine(f)
	var nf: Array = []
	for f in sel["fines"]:
		var a: Vector3 = f["mn"]
		var b: Vector3 = f["mx"]
		var n0 := Vector3(cx - (b.z - cz), a.y, cz + (a.x - cx))
		var n1 := Vector3(cx - (a.z - cz), b.y, cz + (b.x - cx))
		nf.append(_gr_add_fine(n0, n1, f))
	var np: Array = []
	for id in sel["placed"]:
		var p: Dictionary = world.edit_get_placed(int(id))
		if p.is_empty():
			continue
		var pos: Vector3 = p["pos"]
		var npos := Vector3(cx - (pos.z + float(p["d"]) - cz), pos.y, cz + (pos.x - cx))
		var nid: int = world.edit_move_placed(int(id), npos, (int(p["rot"]) + 1) % 4)
		if nid > 0:
			np.append(nid)
	_flush()
	_end_txn()
	sel["fines"] = nf
	sel["placed"] = np
	_group_bounds()


func _n(v: float) -> String:
	return String.num(v, 3)


func _draw_sel() -> void:
	if sel.is_empty():
		if sel_label and tool == T_MOVE:
			sel_label.text = "Nada elegido. Clic en un detalle, objeto o bloque."
		if sel_label2 and tool == T_SELECT:
			sel_label2.text = "Nada elegido. Clic en un mueble, objeto o bloque."
		return
	var txt := ""
	match String(sel["type"]):
		"box":
			var mn: Vector3 = sel["mn"]
			var mx: Vector3 = sel["mx"]
			_box(mn - Vector3(0.01, 0.01, 0.01), mx + Vector3(0.01, 0.01, 0.01), Color(1, 0.3, 0.9), true, 0.22)
			var z := mx - mn
			txt = "Detalle %s x %s x %s bloques · en (%s, %s, %s)" % [_n(z.x), _n(z.y), _n(z.z), _n(mn.x), _n(mn.y), _n(mn.z)]
		"placed":
			var p: Dictionary = world.edit_get_placed(int(sel["id"]))
			if p.is_empty():
				sel = {}
				return
			var pos: Vector3 = p["pos"]
			_box(pos, pos + Vector3(p["w"], p["h"], p["d"]), Color(1, 0.3, 0.9), true, 0.2)
			var nm: String = cat_items.get(int(p["cat"]), {}).get("name", "objeto")
			txt = "Objeto: %s · en (%s, %s, %s) · giro %d" % [nm, _n(pos.x), _n(pos.y), _n(pos.z), int(p["rot"])]
		"group":
			var gmn: Vector3 = sel["mn"]
			var gmx: Vector3 = sel["mx"]
			var fl: Array = sel["fines"]
			if fl.size() <= 250:
				for f in fl:
					_box(Vector3(f["mn"]) - Vector3(0.005, 0.005, 0.005), Vector3(f["mx"]) + Vector3(0.005, 0.005, 0.005), Color(1, 0.3, 0.9), true, 0.25)
			_box(gmn - Vector3(0.03, 0.03, 0.03), gmx + Vector3(0.03, 0.03, 0.03), Color(1, 0.8, 0.2))
			var gz := gmx - gmn
			txt = "Grupo: %d cajas pequeñas + %d objetos · %s x %s x %s bloques · en (%s, %s, %s)" % [fl.size(), sel["placed"].size(), _n(gz.x), _n(gz.y), _n(gz.z), _n(gmn.x), _n(gmn.y), _n(gmn.z)]
		"region":
			var a: Vector3i = sel["mn"]
			var b: Vector3i = sel["mx"]
			_box(Vector3(a) - Vector3(0.01, 0.01, 0.01), Vector3(b) + Vector3.ONE + Vector3(0.01, 0.01, 0.01), Color(0.3, 0.9, 1), true, 0.14)
			txt = "Región %d x %d x %d bloques · desde (%d, %d, %d)" % [b.x - a.x + 1, b.y - a.y + 1, b.z - a.z + 1, a.x, a.y, a.z]
	if sel_label:
		sel_label.text = txt + "\nPaso: " + STEP_NAMES[step_i]
	if sel_label2:
		sel_label2.text = txt + "\nPaso: " + STEP_NAMES[step_i]



# ---------------------------------------------------------------------------------------------
# dibujo 3D
# ---------------------------------------------------------------------------------------------

func _box(mn: Vector3, mx: Vector3, col: Color, filled := false, fill_a := 0.25) -> void:
	_lines.append([mn, mx, col])
	if filled:
		_fills.append([mn, mx, Color(col.r, col.g, col.b, fill_a)])


func _grid(p: Vector3, n: Vector3i, g: float, half: int, col: Color, col_major: Color) -> void:
	# cuadricula sobre el plano de la cara apuntada (unidades de bloque); g = paso, half = celdas a cada lado
	var ax := 0 if n.x != 0 else (1 if n.y != 0 else 2)
	var u := 1 if ax == 0 else 0
	var v := 1 if ax == 2 else 2
	var plane: float = p[ax]
	plane = round(plane / g) * g if absf(plane / g - round(plane / g)) < 0.02 else plane
	var cu: float = floor(p[u] / g) * g
	var cv: float = floor(p[v] / g) * g
	var lo_u := cu - half * g
	var hi_u := cu + (half + 1) * g
	var lo_v := cv - half * g
	var hi_v := cv + (half + 1) * g
	var off := 0.012 * float(n[ax])
	for i in range(2 * half + 2):
		var a := lo_u + i * g
		var b := lo_v + i * g
		var major := g < 1.0 and absf(a - round(a)) < 0.001
		var majb := g < 1.0 and absf(b - round(b)) < 0.001
		var p0 := Vector3.ZERO
		var p1 := Vector3.ZERO
		p0[ax] = plane + off
		p1[ax] = plane + off
		p0[u] = a
		p1[u] = a
		p0[v] = lo_v
		p1[v] = hi_v
		_glines.append([p0, p1, col_major if (major or (g >= 1.0 and i % 4 == 0)) else col])
		var q0 := Vector3.ZERO
		var q1 := Vector3.ZERO
		q0[ax] = plane + off
		q1[ax] = plane + off
		q0[v] = b
		q1[v] = b
		q0[u] = lo_u
		q1[u] = hi_u
		_glines.append([q0, q1, col_major if (majb or (g >= 1.0 and i % 4 == 0)) else col])


func _draw_tool() -> void:
	_draw_taller()
	var ok := _hit_ok()
	if ok and grid_on:
		var gp: Vector3 = hit["point"]
		var gn: Vector3i = hit["normal"]
		match tool:
			T_BLOCK, T_BRUSH, T_BOX, T_DETAIL, T_CAT, T_PASTE, T_STRUCT:
				_grid(gp, gn, 1.0, 7, Color(1, 1, 1, 0.22), Color(1, 1, 1, 0.5))
			T_FINE:
				_grid(gp, gn, fine_size / 8.0 if fine_size < 8 else 1.0, 8 if fine_size < 8 else 4, Color(1, 0.95, 0.6, 0.28), Color(1, 1, 1, 0.6))
	if has_a and tool == T_BOX:
		var b: Vector3i = box_a
		var c: Vector3i = hit["cell"] if ok else b
		var mn := Vector3i(mini(b.x, c.x), mini(b.y, c.y), mini(b.z, c.z))
		var mx := Vector3i(maxi(b.x, c.x), maxi(b.y, c.y), maxi(b.z, c.z))
		_box(Vector3(mn) - Vector3(0.01, 0.01, 0.01), Vector3(mx) + Vector3(1.01, 1.01, 1.01), Color(1, 0.9, 0.2), true, 0.15)
		box_label.text = "Caja: %d x %d x %d (A en %d,%d,%d)" % [mx.x - mn.x + 1, mx.y - mn.y + 1, mx.z - mn.z + 1, b.x, b.y, b.z]
	elif tool == T_BOX:
		box_label.text = "Clic en la esquina A, luego en la B."
	_draw_sel()
	if sel_piece.has("x0"):
		var s: Dictionary = sel_piece
		_box(Vector3(s["x0"], s["ylo"], s["z0"]), Vector3(s["x1"], s["yhi"] + 1, s["z1"]), Color(1, 0.3, 0.9), false)
	if not ok:
		return
	var cell: Vector3i = hit["cell"]
	var adj: Vector3i = hit["adj"]
	var bmin: Vector3 = hit["bmin"]
	var bmax: Vector3 = hit["bmax"]
	match tool:
		T_BLOCK:
			if hit["kind"] == "block":
				_box(bmin - Vector3(0.01, 0.01, 0.01), bmax + Vector3(0.01, 0.01, 0.01), Color(1, 0.3, 0.3))
			_box(Vector3(adj), Vector3(adj) + Vector3.ONE, Color(0.4, 1, 0.4), true, 0.18)
		T_BRUSH:
			var c: Vector3i = cell
			var h := brush_n / 2
			var mn := c - Vector3i(h, h, h)
			_box(Vector3(mn), Vector3(mn) + Vector3.ONE * brush_n, Color(1, 0.6, 0.2), true, 0.12)
			var a2 := adj - Vector3i(h, h, h)
			_box(Vector3(a2), Vector3(a2) + Vector3.ONE * brush_n, Color(0.4, 1, 0.4), false)
		T_BOX:
			if not has_a:
				_box(bmin - Vector3(0.01, 0.01, 0.01), bmax + Vector3(0.01, 0.01, 0.01), Color(1, 0.9, 0.2))
		T_DETAIL:
			_box(bmin - Vector3(0.02, 0.02, 0.02), bmax + Vector3(0.02, 0.02, 0.02), Color(0.2, 1, 1) if hit["kind"] != "block" else Color(0.5, 0.5, 0.5), hit["kind"] != "block", 0.3)
		T_FINE:
			var f := _fine_box()
			if not f.is_empty():
				_box(f[0], f[1], fine_color, true, 0.6)
			if hit["kind"] == "abox" or hit["kind"] == "deco":
				_box(bmin - Vector3(0.01, 0.01, 0.01), bmax + Vector3(0.01, 0.01, 0.01), Color(1, 0.3, 0.3))
		T_CAT:
			var pz := _cat_pose()
			if not pz.is_empty():
				var c: Dictionary = cat_items[cat_id]
				var dims: Vector3i = pz["dims"]
				var pos: Vector3 = pz["pos"]
				_box(pos, pos + Vector3(dims), Color(0.4, 1, 0.5), false)
				if not bool(c["deco"]):
					var arr: PackedFloat32Array = world.catalog_boxes(cat_id, pos, int(pz["rot"]))
					var n := arr.size() / 9
					for i in range(n):
						var k := i * 9
						_fills.append([Vector3(arr[k], arr[k + 1], arr[k + 2]), Vector3(arr[k + 3], arr[k + 4], arr[k + 5]), Color(arr[k + 6], arr[k + 7], arr[k + 8], 0.7)])
				else:
					_fills.append([pos, pos + Vector3.ONE, Color(0.4, 1, 0.5, 0.35)])
			if hit["kind"] != "block":
				_box(bmin - Vector3(0.02, 0.02, 0.02), bmax + Vector3(0.02, 0.02, 0.02), Color(1, 0.3, 0.3))
		T_STRUCT:
			var info: Dictionary = world.piece_at(Vector3(hit["point"]) - Vector3(hit["normal"]) * 0.2)
			if not info.is_empty():
				_box(Vector3(info["x0"], info["ylo"], info["z0"]), Vector3(info["x1"], info["yhi"] + 1, info["z1"]), Color(1, 0.8, 1), false)
		T_PASTE:
			var sz: Vector3i = world.clipboard_size()
			if sz.x > 0:
				var dsz := sz
				if paste_rot % 2 == 1:
					dsz = Vector3i(sz.z, sz.y, sz.x)
				_box(Vector3(adj + cat_off), Vector3(adj + cat_off + dsz), Color(0.5, 0.8, 1), true, 0.15)
		T_STAMP:
			_draw_stamp()
		T_INSPECT:
			_box(bmin - Vector3(0.01, 0.01, 0.01), bmax + Vector3(0.01, 0.01, 0.01), Color(1, 1, 1))
		T_MOVE:
			_box(bmin - Vector3(0.01, 0.01, 0.01), bmax + Vector3(0.01, 0.01, 0.01), Color(1, 1, 0.4))
		T_SELECT:
			if select_mode == 2 and sel_a_set:
				var sa := Vector3i(mini(sel_a.x, cell.x), mini(sel_a.y, cell.y), mini(sel_a.z, cell.z))
				var sb := Vector3i(maxi(sel_a.x, cell.x), maxi(sel_a.y, cell.y), maxi(sel_a.z, cell.z))
				_box(Vector3(sa) - Vector3(0.01, 0.01, 0.01), Vector3(sb) + Vector3(1.01, 1.01, 1.01), Color(0.3, 1, 0.5), true, 0.14)
			else:
				_box(bmin - Vector3(0.01, 0.01, 0.01), bmax + Vector3(0.01, 0.01, 0.01), Color(0.3, 1, 0.8))


func _push_box_lines(st: ImmediateMesh, mn: Vector3, mx: Vector3, col: Color) -> void:
	var p := [Vector3(mn.x, mn.y, mn.z), Vector3(mx.x, mn.y, mn.z), Vector3(mx.x, mn.y, mx.z), Vector3(mn.x, mn.y, mx.z),
		Vector3(mn.x, mx.y, mn.z), Vector3(mx.x, mx.y, mn.z), Vector3(mx.x, mx.y, mx.z), Vector3(mn.x, mx.y, mx.z)]
	var e := [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]]
	st.surface_set_color(col)
	for pr in e:
		st.surface_add_vertex(p[pr[0]] * BS)
		st.surface_add_vertex(p[pr[1]] * BS)


func _push_box_tris(st: ImmediateMesh, mn: Vector3, mx: Vector3, col: Color) -> void:
	var p := [Vector3(mn.x, mn.y, mn.z), Vector3(mx.x, mn.y, mn.z), Vector3(mx.x, mn.y, mx.z), Vector3(mn.x, mn.y, mx.z),
		Vector3(mn.x, mx.y, mn.z), Vector3(mx.x, mx.y, mn.z), Vector3(mx.x, mx.y, mx.z), Vector3(mn.x, mx.y, mx.z)]
	var f := [[0, 1, 2, 3], [4, 7, 6, 5], [0, 4, 5, 1], [1, 5, 6, 2], [2, 6, 7, 3], [3, 7, 4, 0]]
	st.surface_set_color(col)
	for q in f:
		st.surface_add_vertex(p[q[0]] * BS)
		st.surface_add_vertex(p[q[1]] * BS)
		st.surface_add_vertex(p[q[2]] * BS)
		st.surface_add_vertex(p[q[0]] * BS)
		st.surface_add_vertex(p[q[2]] * BS)
		st.surface_add_vertex(p[q[3]] * BS)


func _flush_overlay() -> void:
	lines_mesh.clear_surfaces()
	fill_mesh.clear_surfaces()
	lines_mi.global_transform = Transform3D.IDENTITY
	fill_mi.global_transform = Transform3D.IDENTITY
	if _lines.size() > 0 or _glines.size() > 0:
		lines_mesh.surface_begin(Mesh.PRIMITIVE_LINES)
		for gl in _glines:
			lines_mesh.surface_set_color(gl[2])
			lines_mesh.surface_add_vertex(gl[0] * BS)
			lines_mesh.surface_add_vertex(gl[1] * BS)
		for b in _lines:
			_push_box_lines(lines_mesh, b[0], b[1], b[2])
		lines_mesh.surface_end()
	if _fills.size() > 0:
		fill_mesh.surface_begin(Mesh.PRIMITIVE_TRIANGLES)
		for b in _fills:
			_push_box_tris(fill_mesh, b[0], b[1], b[2])
		fill_mesh.surface_end()


func _update_barriers() -> void:
	var c: Vector3 = cam.global_position / BS
	var arr: PackedVector3Array = world.list_barriers(c, 16)
	var mm: MultiMesh = barrier_mm.multimesh
	mm.instance_count = arr.size()
	barrier_mm.global_transform = Transform3D.IDENTITY
	for i in range(arr.size()):
		mm.set_instance_transform(i, Transform3D(Basis(), (arr[i] + Vector3(0.5, 0.5, 0.5)) * BS))


# ---------------------------------------------------------------------------------------------
# texto informativo
# ---------------------------------------------------------------------------------------------

func _update_info() -> void:
	var cp: Vector3 = cam.global_position / BS
	var t := "TALLER · %s%s · Cámara bloques (%d, %d, %d) · nivel del mar y=192\n" % [TOOLS[tool], " · MIRANDO (Tab)" if captured else "", int(cp.x), int(cp.y), int(cp.z)]
	if _hit_ok():
		var c: Vector3i = hit["cell"]
		var k: String = hit["kind"]
		if k == "block":
			var rb := int(hit["block"])
			var bn: String = BLOCK_NAMES[rb & 0x7f] if (rb & 0x7f) < BLOCK_NAMES.size() else "?"
			t += "Apuntando: %s%s en (%d, %d, %d) · a %.1f m" % [bn, " (medio)" if (rb & SLAB) != 0 else "", c.x, c.y, c.z, float(hit["t"])]
		elif k == "abox":
			var col: Vector3i = hit["color"]
			var origin := "tuyo (voxel fino)" if int(hit["fine_id"]) > 0 else ("objeto del catálogo" if int(hit["placed_id"]) > 0 else "generado por el juego")
			t += "Apuntando: detalle %s · color %d,%d,%d · textura %d%s · cerca de (%d, %d, %d)" % [origin, col.x, col.y, col.z, int(hit["pat"]), " · brilla" if hit["glow"] else "", c.x, c.y, c.z]
		else:
			t += "Apuntando: objeto de decoración tipo %d en (%d, %d, %d)%s" % [int(hit["dkind"]), c.x, c.y, c.z, " · del catálogo" if int(hit["placed_id"]) > 0 else ""]
		if tool == T_INSPECT:
			var pi: Dictionary = world.piece_at(Vector3(hit["point"]) - Vector3(hit["normal"]) * 0.2)
			if not pi.is_empty():
				t += "\nEstructura: %s (idx %d)" % [pi["label"], pi["idx"]]
	else:
		t += "Apuntando: nada"
	if tool == T_BLOCK or tool == T_BRUSH or tool == T_BOX:
		t += "\nBloque actual: %s%s" % [BLOCK_NAMES[block], " (medio)" if slab else ""]
	info_label.text = t + _doc_info()


func _update_stats() -> void:
	var s: Dictionary = world.edits_stats()
	stats_label.text = "Ediciones:\n• cubos %d\n• voxeles finos %d\n• detalles borrados %d\n• objetos colocados %d\n• estructuras cambiadas %d de %d\nDeshacer: %d · Rehacer: %d\n%s" % [
		s.get("cubes", 0), s.get("fine", 0), s.get("erased", 0), s.get("placed", 0), s.get("pieces", 0), s.get("pieces_total", 0), s.get("undo", 0), s.get("redo", 0),
		"Guardado automático activo" if not dirty_save else "Guardando…"]


# ---------------------------------------------------------------------------------------------
# navegacion y mapa
# ---------------------------------------------------------------------------------------------

func goto_block(bx: int, bz: int, by: int) -> void:
	var gy: float = by
	if by == -9999:
		gy = world.ground_height(bx * BS, bz * BS) / BS
	var target := Vector3(bx * BS, gy * BS, bz * BS)
	var dist := 14.0
	cam.global_position = target + Vector3(0, dist * 0.8 + 3.0, dist)
	var d := target - cam.global_position
	yaw = atan2(-d.x, -d.z)
	pitch = clampf(atan2(d.y, Vector2(d.x, d.z).length()), -1.4, 1.4)
	_say("Teletransportado a (%d, %d)" % [bx, bz])


func goto_site(i: int) -> void:
	goto_block(sites[i * 9 + 2], sites[i * 9 + 3], sites[i * 9 + 4])
	select_site(i)


func open_map() -> void:
	pass


func close_map() -> void:
	pass


# ---------------------------------------------------------------------------------------------
# notas
# ---------------------------------------------------------------------------------------------

func _notes_path() -> String:
	return "user://editor_notes_%d.json" % int(main.cfg["seed"])


func _load_notes() -> void:
	notes = []
	if FileAccess.file_exists(_notes_path()):
		var f := FileAccess.open(_notes_path(), FileAccess.READ)
		var v: Variant = JSON.parse_string(f.get_as_text())
		if v is Array:
			notes = v


func add_note() -> void:
	var cp: Vector3 = cam.global_position / BS
	var x := int(cp.x)
	var y := int(cp.y)
	var z := int(cp.z)
	if _hit_ok():
		var c: Vector3i = hit["cell"]
		x = c.x
		y = c.y
		z = c.z
	notes.append({"x": x, "y": y, "z": z, "text": note_edit.text, "time": Time.get_datetime_string_from_system()})
	note_edit.text = ""
	_refresh_notes()
	var f := FileAccess.open(_notes_path(), FileAccess.WRITE)
	f.store_string(JSON.stringify(notes))
	_say("Nota guardada en (%d, %d, %d)" % [x, y, z])


# =============================================================================================
# TALLER: documento (estructura / zona), marco, rejilla, catalogo "Mis creaciones" y estampado
# =============================================================================================

const FLAT_Y := 200                       # el suelo llega hasta el bloque 199; lo construido empieza en y = 200
const LIM_STRUCT := Vector3i(96, 128, 96)  # estructura: casas x2 (hasta ~50 x 40), torres y arboles grandes
const LIM_ZONE := Vector3i(512, 320, 512) # zona: poblado grande o arbol gigante (256 x 160 x 256 m)
const FACING_NAMES := ["Norte (−Z)", "Este (+X)", "Sur (+Z)", "Oeste (−X)"]
const FACING_KEYS := ["norte", "este", "sur", "oeste"]
const KIND_KEYS := ["estructura", "zona"]
const KIND_DIRS := ["estructuras", "zonas"]

var doc_name := "mi_estructura"
var doc_kind := 0
var doc_size := Vector3i(24, 48, 20)
var doc_entry := Vector2i(12, 0)
var doc_facing := 0
var doc_desc := ""
var doc_stamps: Array = []
var doc_dirty := false
var size_spins: Array = []
var entry_spins: Array = []
var name_edit: LineEdit
var desc_edit: LineEdit
var kind_opt: OptionButton
var face_opt: OptionButton
var lim_label: Label
var doc_label: Label
var cr_list: ItemList
var cr_filter: OptionButton
var cr_search: LineEdit
var cr_info: Label
var cr_thumb: TextureRect
var cr_files: Array = []
var stamp_doc: Dictionary = {}
var stamp_path := ""
var stamp_rot := 0
var stamp_label: Label
var confirm_cb: Callable = Callable()
var floor_mi: MeshInstance3D
var floor1_mi: MeshInstance3D
var floor_mesh := ImmediateMesh.new()
var floor1_mesh := ImmediateMesh.new()
var floor1_cell := Vector2i(-999999, 0)
var cat_dir_cache := ""
var capturing := false


func begin() -> void:
	active = true
	ui.visible = true
	lines_mi.visible = true
	fill_mi.visible = true
	set_process(true)
	set_process_unhandled_input(true)
	tool_buttons[T_STRUCT].disabled = true
	fov = float(main.cfg["fov"])
	cam.fov = fov
	cam.make_current()
	_make_floor()
	_fill_catalog()
	if FileAccess.file_exists("user://taller_autosave.json"):
		var f := FileAccess.open("user://taller_autosave.json", FileAccess.READ)
		var err := load_doc_text(f.get_as_text())
		if err != "":
			push_warning("Autoguardado no cargado: " + err)
	_home_camera()
	_set_captured(false)
	_refresh_all()
	_refresh_creations()
	_sync_doc_ui()
	_say("Taller · Tab: mirar con el ratón · Clic der mantenido: girar · G: cuadrícula · Ctrl+S: guardar en el catálogo · H: ayuda", 8.0)


func on_quit() -> void:
	_end_txn()
	dirty_save = true
	_save_now()


func _home_camera() -> void:
	cam.global_position = Vector3(doc_size.x * 0.5, FLAT_Y + minf(doc_size.y * 0.5, 40.0) + 12.0, doc_size.z + minf(doc_size.z * 0.9, 70.0) + 14.0) * BS
	yaw = 0.0
	pitch = -0.3


func _fmin() -> Vector3i:
	return Vector3i(0, FLAT_Y, 0)


func _fmax() -> Vector3i:
	return Vector3i(doc_size.x - 1, FLAT_Y + doc_size.y - 1, doc_size.z - 1)


func _in_frame(c: Vector3i) -> bool:
	var a := _fmin()
	var b := _fmax()
	return c.x >= a.x and c.y >= a.y and c.z >= a.z and c.x <= b.x and c.y <= b.y and c.z <= b.z


func _hit_ok() -> bool:
	if hit.is_empty() or not hit.get("hit", false):
		return false
	return _in_frame(hit["cell"]) or _in_frame(hit["adj"])


func _lim() -> Vector3i:
	return LIM_ZONE if doc_kind == 1 else LIM_STRUCT


# ---------------------------------------------------------------------------------------------
# suelo, marco y rejilla
# ---------------------------------------------------------------------------------------------

func _line_mat(depth: bool) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.vertex_color_use_as_albedo = true
	m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	m.no_depth_test = not depth
	m.render_priority = 5
	return m


func _make_floor() -> void:
	floor_mi = MeshInstance3D.new()
	floor_mi.mesh = floor_mesh
	floor_mi.material_override = _line_mat(true)
	floor_mi.top_level = true
	floor_mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	main.add_child(floor_mi)
	floor1_mi = MeshInstance3D.new()
	floor1_mi.mesh = floor1_mesh
	floor1_mi.material_override = _line_mat(true)
	floor1_mi.top_level = true
	floor1_mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	main.add_child(floor1_mi)
	_rebuild_floor()


func _rebuild_floor() -> void:
	floor_mesh.clear_surfaces()
	var y := FLAT_Y * BS + 0.03
	var w := doc_size.x
	var d := doc_size.z
	floor_mesh.surface_begin(Mesh.PRIMITIVE_LINES)
	for x in range(0, w + 1, 4):
		var major := x % 16 == 0
		floor_mesh.surface_set_color(Color(1, 0.85, 0.3, 0.9) if major else Color(1, 1, 1, 0.38))
		floor_mesh.surface_add_vertex(Vector3(x * BS, y, 0))
		floor_mesh.surface_add_vertex(Vector3(x * BS, y, d * BS))
	for z in range(0, d + 1, 4):
		var major := z % 16 == 0
		floor_mesh.surface_set_color(Color(1, 0.85, 0.3, 0.9) if major else Color(1, 1, 1, 0.38))
		floor_mesh.surface_add_vertex(Vector3(0, y, z * BS))
		floor_mesh.surface_add_vertex(Vector3(w * BS, y, z * BS))
	# borde del marco
	floor_mesh.surface_set_color(Color(0.3, 1, 0.5, 1))
	var c := [Vector3(0, y, 0), Vector3(w * BS, y, 0), Vector3(w * BS, y, d * BS), Vector3(0, y, d * BS)]
	for i in range(4):
		floor_mesh.surface_add_vertex(c[i])
		floor_mesh.surface_add_vertex(c[(i + 1) % 4])
	floor_mesh.surface_end()
	floor1_cell = Vector2i(-999999, 0)


func _update_floor1() -> void:
	# lineas de 1 bloque solo cerca de la camara (y solo si estas a poca altura)
	var cp: Vector3 = cam.global_position / BS
	var cx := int(floorf(cp.x))
	var cz := int(floorf(cp.z))
	var low: bool = cp.y - FLAT_Y < 60.0
	var key := Vector2i(cx, cz) if low else Vector2i(-999998, 0)
	if key == floor1_cell:
		return
	floor1_cell = key
	floor1_mesh.clear_surfaces()
	if not low:
		return
	var r := 22
	var x0 := maxi(0, cx - r)
	var x1 := mini(doc_size.x, cx + r)
	var z0 := maxi(0, cz - r)
	var z1 := mini(doc_size.z, cz + r)
	if x1 <= x0 or z1 <= z0:
		return
	var y := FLAT_Y * BS + 0.025
	floor1_mesh.surface_begin(Mesh.PRIMITIVE_LINES)
	floor1_mesh.surface_set_color(Color(1, 1, 1, 0.16))
	for x in range(x0, x1 + 1):
		if x % 4 == 0:
			continue
		floor1_mesh.surface_add_vertex(Vector3(x * BS, y, z0 * BS))
		floor1_mesh.surface_add_vertex(Vector3(x * BS, y, z1 * BS))
	for z in range(z0, z1 + 1):
		if z % 4 == 0:
			continue
		floor1_mesh.surface_add_vertex(Vector3(x0 * BS, y, z * BS))
		floor1_mesh.surface_add_vertex(Vector3(x1 * BS, y, z * BS))
	floor1_mesh.surface_end()


func _facing_dir(f: int) -> Vector3:
	match f & 3:
		0:
			return Vector3(0, 0, -1)
		1:
			return Vector3(1, 0, 0)
		2:
			return Vector3(0, 0, 1)
	return Vector3(-1, 0, 0)


func _draw_entry(e: Vector2i, f: int, col: Color, org := Vector3i.ZERO) -> void:
	var o := Vector3(org.x, org.y if org.y != 0 else FLAT_Y, org.z)
	var base := o + Vector3(e.x, 0, e.y)
	_box(base + Vector3(0, 0.02, 0), base + Vector3(1, 0.3, 1), col, true, 0.5)
	var c := base + Vector3(0.5, 0.35, 0.5)
	var dv := _facing_dir(f)
	var tip := c + dv * 5.0
	var side := Vector3(-dv.z, 0, dv.x)
	_glines.append([c, tip, col])
	_glines.append([tip, tip - dv * 1.4 + side * 0.9, col])
	_glines.append([tip, tip - dv * 1.4 - side * 0.9, col])


func _draw_taller() -> void:
	_update_floor1()
	var a := _fmin()
	var b := _fmax()
	_box(Vector3(a), Vector3(b) + Vector3.ONE, Color(0.3, 1, 0.5), false)
	_draw_entry(doc_entry, doc_facing, Color(1, 0.85, 0.2))
	if tool == T_STAMP:
		stamp_label.text = ("Creación: %s\nGiro: %d°" % [stamp_doc.get("name", "?"), stamp_rot * 90]) if not stamp_doc.is_empty() else "Nada elegido: ve a «Mis creaciones» y pulsa Estampar."


func _stamp_dims() -> Vector3i:
	var s: Array = stamp_doc.get("size", [1, 1, 1])
	var d := Vector3i(int(s[0]), int(s[1]), int(s[2]))
	if stamp_rot % 2 == 1:
		d = Vector3i(d.z, d.y, d.x)
	return d


func _stamp_origin() -> Vector3i:
	var adj: Vector3i = hit["adj"]
	return adj + cat_off


func _draw_stamp() -> void:
	if stamp_doc.is_empty():
		return
	var dm := _stamp_dims()
	var o := _stamp_origin()
	var fits := _stamp_fits(o, dm)
	var col := Color(0.4, 0.9, 1.0) if fits else Color(1, 0.3, 0.3)
	_box(Vector3(o), Vector3(o + dm), col, true, 0.14)
	var en: Dictionary = stamp_doc.get("entry", {})
	if not en.is_empty():
		var sz: Array = stamp_doc["size"]
		var e := Vector2i(int(en.get("x", 0)), int(en.get("z", 0)))
		var f: int = FACING_KEYS.find(String(en.get("facing", "norte")))
		var W := int(sz[0])
		var D := int(sz[2])
		for i in range(stamp_rot):
			e = Vector2i(D - 1 - e.y, e.x)
			f = (f + 1) & 3
			var t := W
			W = D
			D = t
		_draw_entry(e, f, col, Vector3i(o.x, o.y, o.z))


func _stamp_fits(o: Vector3i, dm: Vector3i) -> bool:
	var a := _fmin()
	var b := _fmax()
	return o.x >= a.x and o.y >= a.y and o.z >= a.z and o.x + dm.x - 1 <= b.x and o.y + dm.y - 1 <= b.y and o.z + dm.z - 1 <= b.z


func _doc_info() -> String:
	var m := Vector3(doc_size) * BS
	return "\n%s «%s» · %d x %d x %d bloques (%.0f x %.0f x %.0f m) · altura sobre el suelo: %d%s" % [
		"ZONA" if doc_kind == 1 else "ESTRUCTURA", doc_name, doc_size.x, doc_size.y, doc_size.z, m.x, m.y, m.z,
		int(cam.global_position.y / BS) - FLAT_Y, "  ·  sin guardar" if doc_dirty else ""]


# ---------------------------------------------------------------------------------------------
# estampar una creacion del catalogo
# ---------------------------------------------------------------------------------------------

func _rot_cell(x: int, z: int, D: int) -> Vector2i:
	return Vector2i(D - 1 - z, x)


func _cat_wd(cat: int, rot: int) -> Vector2i:
	var c: Dictionary = cat_items.get(cat, {})
	var w := int(c.get("w", 1))
	var d := int(c.get("d", 1))
	return Vector2i(d, w) if (rot & 1) == 1 else Vector2i(w, d)


func _stamp_click(b: int) -> void:
	if b != 1:
		return
	if stamp_doc.is_empty():
		_say("Primero elige una creación en «Mis creaciones» → Estampar")
		return
	if not _hit_ok():
		return
	var dm := _stamp_dims()
	var o := _stamp_origin()
	if not _stamp_fits(o, dm):
		_say("No cabe ahí: la estampa se sale del marco del documento")
		return
	var n := stamp_apply(stamp_doc, o, stamp_rot)
	doc_stamps.append({"name": stamp_doc.get("name", "?"), "file": stamp_path.get_file(), "pos": [o.x, o.y - FLAT_Y, o.z], "rot": stamp_rot * 90})
	doc_dirty = true
	_say("Estampada «%s» (%d elementos)" % [stamp_doc.get("name", "?"), n])


func stamp_apply(sd: Dictionary, o: Vector3i, rot: int) -> int:
	var ed: Dictionary = sd.get("edits", {})
	var sz: Array = sd.get("size", [1, 1, 1])
	var W := int(sz[0])
	var D := int(sz[2])
	var cubes: Array = []
	for c in ed.get("cubes", []):
		cubes.append([int(c[0]), int(c[1]) - FLAT_Y, int(c[2]), int(c[3])])
	var fine: Array = []
	for f in ed.get("fine", []):
		fine.append([float(f[1]), float(f[2]) - FLAT_Y, float(f[3]), float(f[4]), float(f[5]) - FLAT_Y, float(f[6]), int(f[7]), int(f[8]), int(f[9]), int(f[10]), int(f[11])])
	var placed: Array = []
	for p in ed.get("placed", []):
		placed.append([int(p[1]), float(p[2]), float(p[3]) - FLAT_Y, float(p[4]), int(p[5]), int(p[6]), int(p[7]), int(p[8])])
	for i in range(rot):
		for c in cubes:
			var r := _rot_cell(c[0], c[2], D)
			c[0] = r.x
			c[2] = r.y
		for f in fine:
			var x0: float = f[0]
			var z0: float = f[2]
			var x1: float = f[3]
			var z1: float = f[5]
			f[0] = D - z1
			f[3] = D - z0
			f[2] = x0
			f[5] = x1
		for p in placed:
			var wd := _cat_wd(p[0], p[4])
			var px: float = p[1]
			var pz: float = p[3]
			p[1] = D - (pz + wd.y)
			p[3] = px
			p[4] = (p[4] + 1) & 3
		var t := W
		W = D
		D = t
	var n := 0
	_begin_txn()
	for c in cubes:
		var cc := Vector3i(o.x + c[0], o.y + c[1], o.z + c[2])
		n += world.edit_set_cubes(cc, cc, c[3], 0, 0, 0)
	for f in fine:
		var mn := Vector3(o) + Vector3(f[0], f[1], f[2])
		var mx := Vector3(o) + Vector3(f[3], f[4], f[5])
		if world.edit_add_fine(mn, mx, f[6], f[7], f[8], f[9], f[10] != 0) > 0:
			n += 1
	for p in placed:
		var pos := Vector3(o) + Vector3(p[1], p[2], p[3])
		if world.edit_place(p[0], pos, p[4], p[5], p[6], p[7] != 0) > 0:
			n += 1
	_flush()
	_end_txn()
	return n


# ---------------------------------------------------------------------------------------------
# documento <-> archivo
# ---------------------------------------------------------------------------------------------

func _slug(s: String) -> String:
	var o := ""
	for ch in s.strip_edges().to_lower():
		if (ch >= "a" and ch <= "z") or (ch >= "0" and ch <= "9") or ch == "_" or ch == "-":
			o += ch
		elif ch == " " or ch == ".":
			o += "_"
		elif ch == "á":
			o += "a"
		elif ch == "é":
			o += "e"
		elif ch == "í":
			o += "i"
		elif ch == "ó":
			o += "o"
		elif ch == "ú":
			o += "u"
		elif ch == "ñ":
			o += "n"
	return o


func build_doc_text() -> String:
	var ed: Variant = JSON.parse_string(world.export_edits(main.GAME_VERSION))
	if not (ed is Dictionary):
		return ""
	var a := _fmin()
	var b := _fmax()
	var dropped := 0
	var lines := PackedStringArray()
	var cube_n := 0
	var cs := PackedStringArray()
	for c in ed.get("cubes", []):
		var x := int(c[0])
		var y := int(c[1])
		var z := int(c[2])
		if x < a.x or y < a.y or z < a.z or x > b.x or y > b.y or z > b.z:
			dropped += 1
			continue
		cs.append("[%d,%d,%d,%d]" % [x, y, z, int(c[3])])
		cube_n += 1
	var cube_lines := PackedStringArray()
	var i := 0
	while i < cs.size():
		cube_lines.append(",".join(cs.slice(i, i + 12)))
		i += 12
	var fine_out := PackedStringArray()
	for f in ed.get("fine", []):
		var cx := (float(f[1]) + float(f[4])) * 0.5
		var cy := (float(f[2]) + float(f[5])) * 0.5
		var cz := (float(f[3]) + float(f[6])) * 0.5
		if cx < a.x or cy < a.y or cz < a.z or cx > b.x + 1 or cy > b.y + 1 or cz > b.z + 1:
			dropped += 1
			continue
		fine_out.append(JSON.stringify(f))
	var placed_out := PackedStringArray()
	for p in ed.get("placed", []):
		var px := float(p[2])
		var py := float(p[3])
		var pz := float(p[4])
		if px < a.x or py < a.y or pz < a.z or px > b.x + 1 or py > b.y + 1 or pz > b.z + 1:
			dropped += 1
			continue
		placed_out.append(JSON.stringify(p))
	var meta := PackedStringArray()
	meta.append("\"format\":\"farlands-taller\",\"version\":1,\"taller\":\"%s\"" % main.VERSION)
	meta.append("\"name\":%s,\"kind\":\"%s\"" % [JSON.stringify(doc_name), KIND_KEYS[doc_kind]])
	meta.append("\"description\":%s" % JSON.stringify(doc_desc))
	meta.append("\"size\":[%d,%d,%d]" % [doc_size.x, doc_size.y, doc_size.z])
	meta.append("\"origin\":[0,%d,0]" % FLAT_Y)
	meta.append("\"bbox_min\":[%d,%d,%d],\"bbox_max\":[%d,%d,%d]" % [a.x, a.y, a.z, b.x, b.y, b.z])
	meta.append("\"coords\":\"Bloques de 0,5 m. x,y,z absolutos de este archivo. Posicion local = (x, y-%d, z). El marco ocupa x 0..%d, z 0..%d, y %d..%d. y=%d es el primer bloque sobre el suelo plano.\"" % [FLAT_Y, doc_size.x - 1, doc_size.z - 1, FLAT_Y, b.y, FLAT_Y])
	meta.append("\"entry\":{\"x\":%d,\"z\":%d,\"facing\":\"%s\"}" % [doc_entry.x, doc_entry.y, FACING_KEYS[doc_facing]])
	meta.append("\"stamps\":%s" % JSON.stringify(doc_stamps))
	meta.append("\"counts\":{\"cubes\":%d,\"fine\":%d,\"placed\":%d,\"dropped_outside_frame\":%d}" % [cube_n, fine_out.size(), placed_out.size(), dropped])
	var o := "{\n" + ",\n".join(meta) + ",\n"
	o += "\"edits\":{\"format\":\"farlands-edits\",\"version\":1,\"game\":\"%s\",\"seed\":%d,\n" % [main.GAME_VERSION, int(main.cfg["seed"])]
	o += "\"cubes\":[\n" + ",\n".join(cube_lines) + "\n],\n"
	o += "\"fine\":[\n" + ",\n".join(fine_out) + "\n],\n"
	o += "\"erase\":[],\n"
	o += "\"placed\":[\n" + ",\n".join(placed_out) + "\n],\n"
	o += "\"pieces\":[]}\n}\n"
	return o


func load_doc_text(text: String) -> String:
	var d: Variant = JSON.parse_string(text)
	if not (d is Dictionary) or String(d.get("format", "")) != "farlands-taller":
		return "no es un archivo del Taller de Farlands"
	var sz: Array = d.get("size", [24, 48, 20])
	doc_name = String(d.get("name", "sin_nombre"))
	doc_kind = KIND_KEYS.find(String(d.get("kind", "estructura")))
	if doc_kind < 0:
		doc_kind = 0
	var lim := _lim()
	doc_size = Vector3i(clampi(int(sz[0]), 4, lim.x), clampi(int(sz[1]), 4, lim.y), clampi(int(sz[2]), 4, lim.z))
	doc_desc = String(d.get("description", ""))
	var en: Dictionary = d.get("entry", {})
	doc_entry = Vector2i(int(en.get("x", doc_size.x / 2)), int(en.get("z", 0)))
	doc_facing = maxi(0, FACING_KEYS.find(String(en.get("facing", "norte"))))
	doc_stamps = d.get("stamps", [])
	world.clear_edits()
	var ed: Variant = d.get("edits", {})
	if ed is Dictionary:
		var err: String = world.import_edits(JSON.stringify(ed), false)
		if err != "":
			return err
	doc_dirty = false
	_rebuild_floor()
	_sync_doc_ui()
	return ""


func new_doc() -> void:
	_end_txn()
	world.clear_edits()
	doc_name = "mi_estructura" if doc_kind == 0 else "mi_zona"
	doc_desc = ""
	doc_stamps = []
	doc_entry = Vector2i(doc_size.x / 2, 0)
	doc_facing = 0
	doc_dirty = false
	dirty_save = true
	save_t = 0.5
	_rebuild_floor()
	_sync_doc_ui()
	_home_camera()
	_say("Documento nuevo")


func catalog_dir() -> String:
	if cat_dir_cache != "":
		return cat_dir_cache
	var base := ""
	if OS.has_feature("editor"):
		base = ProjectSettings.globalize_path("res://").path_join("..").simplify_path().path_join("catalogo")
	else:
		base = OS.get_executable_path().get_base_dir().path_join("catalogo")
	DirAccess.make_dir_recursive_absolute(base)
	for k in KIND_DIRS:
		DirAccess.make_dir_recursive_absolute(base.path_join(k))
	var t := FileAccess.open(base.path_join(".escritura"), FileAccess.WRITE)
	if t == null:
		base = ProjectSettings.globalize_path("user://catalogo")
		for k in KIND_DIRS:
			DirAccess.make_dir_recursive_absolute(base.path_join(k))
	else:
		t.close()
		DirAccess.remove_absolute(base.path_join(".escritura"))
	cat_dir_cache = base
	return base


func _doc_path() -> String:
	return catalog_dir().path_join(KIND_DIRS[doc_kind]).path_join(_slug(doc_name) + ".json")


func save_doc() -> void:
	_end_txn()
	if _slug(doc_name) == "":
		_say("Ponle un nombre al documento (pestaña Taller)")
		return
	DirAccess.make_dir_recursive_absolute(catalog_dir().path_join(KIND_DIRS[doc_kind]))
	var text := build_doc_text()
	if text == "":
		_say("No se pudo generar el archivo")
		return
	var path := _doc_path()
	var f := FileAccess.open(path, FileAccess.WRITE)
	if f == null:
		_say("No se pudo escribir %s" % path, 8.0)
		return
	f.store_string(text)
	f.close()
	doc_dirty = false
	_say("Guardado en el catálogo: %s" % path, 8.0)
	_capture_thumb(path.get_basename() + ".png")
	_refresh_creations()


func _capture_thumb(png: String) -> void:
	if capturing:
		return
	capturing = true
	var vis := [ui.visible, lines_mi.visible, fill_mi.visible, floor1_mi.visible]
	ui.visible = false
	lines_mi.visible = false
	fill_mi.visible = false
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	var img: Image = get_viewport().get_texture().get_image()
	ui.visible = vis[0]
	lines_mi.visible = vis[1]
	fill_mi.visible = vis[2]
	capturing = false
	if img:
		var w := 480
		img.resize(w, int(float(img.get_height()) * w / img.get_width()), Image.INTERPOLATE_BILINEAR)
		img.save_png(png)
		_refresh_creations()


func _zip_add(zp: ZIPPacker, name: String, data: PackedByteArray) -> void:
	zp.start_file(name)
	zp.write_file(data)
	zp.close_file()


func _desktop() -> String:
	var d := OS.get_system_dir(OS.SYSTEM_DIR_DESKTOP)
	if d == "" or not DirAccess.dir_exists_absolute(d):
		d = ProjectSettings.globalize_path("user://")
	return d


func export_zip(all: bool) -> void:
	_end_txn()
	var dt := Time.get_datetime_dict_from_system()
	var stamp := "%04d%02d%02d_%02d%02d" % [dt["year"], dt["month"], dt["day"], dt["hour"], dt["minute"]]
	var zname := ("farlands_catalogo_%s.zip" % stamp) if all else ("farlands_%s_%s.zip" % [_slug(doc_name), stamp])
	var path := _desktop().path_join(zname)
	var zp := ZIPPacker.new()
	if zp.open(path) != OK:
		path = ProjectSettings.globalize_path("user://" + zname)
		if zp.open(path) != OK:
			_say("No se pudo crear el zip")
			return
	var n := 0
	if all:
		for k in KIND_DIRS:
			var dir := catalog_dir().path_join(k)
			for fn in DirAccess.get_files_at(dir):
				if fn.ends_with(".json") or fn.ends_with(".png"):
					_zip_add(zp, k + "/" + fn, FileAccess.get_file_as_bytes(dir.path_join(fn)))
					n += 1
	else:
		_zip_add(zp, _slug(doc_name) + ".json", build_doc_text().to_utf8_buffer())
		n = 1
		var png := _doc_path().get_basename() + ".png"
		if FileAccess.file_exists(png):
			_zip_add(zp, _slug(doc_name) + ".png", FileAccess.get_file_as_bytes(png))
	var rd := "Exportación del Taller de Farlands %s\n\nCada .json es una estructura o zona completa (formato: farlands-taller, ver docs/formato.md).\nEnvíame el .zip (o los .json) para pegarlos en la semilla fija.\n" % main.VERSION
	_zip_add(zp, "LEEME.txt", rd.to_utf8_buffer())
	zp.close()
	DisplayServer.clipboard_set(path)
	_say("Zip creado (%d archivos): %s" % [n, path], 10.0)


# ---------------------------------------------------------------------------------------------
# interfaz del Taller
# ---------------------------------------------------------------------------------------------

func _spin(lo: int, hi: int, val: int, cb: Callable) -> SpinBox:
	var s := SpinBox.new()
	s.min_value = lo
	s.max_value = hi
	s.step = 1
	s.value = val
	s.custom_minimum_size = Vector2(84, 0)
	s.value_changed.connect(cb)
	return s


func _build_dummies() -> void:
	# la pestaña de sitios/notas del editor de mundo no existe aqui: elementos sueltos para que el codigo comun no falle
	site_list = ItemList.new()
	site_search = LineEdit.new()
	site_filter = OptionButton.new()
	struct_label = Label.new()
	note_edit = LineEdit.new()
	note_list = ItemList.new()


func _build_dialogs() -> void:
	file_dlg = FileDialog.new()
	file_dlg.access = FileDialog.ACCESS_FILESYSTEM
	file_dlg.file_mode = FileDialog.FILE_MODE_OPEN_FILE
	file_dlg.use_native_dialog = true
	file_dlg.filters = PackedStringArray(["*.json ; Creación del Taller"])
	file_dlg.file_selected.connect(import_creation)
	root.add_child(file_dlg)
	confirm = ConfirmationDialog.new()
	confirm.confirmed.connect(func() -> void:
		if confirm_cb.is_valid():
			confirm_cb.call())
	root.add_child(confirm)


func _ask(text: String, cb: Callable) -> void:
	confirm.dialog_text = text
	confirm_cb = cb
	confirm.popup_centered()


func _build_tab_taller() -> void:
	var v := _tab("Taller")
	v.add_child(_lbl("Documento actual", 15, UI.ACCENT))
	name_edit = LineEdit.new()
	name_edit.placeholder_text = "nombre (ej. casa_del_herrero)"
	name_edit.text_changed.connect(func(t: String) -> void:
		doc_name = t
		doc_dirty = true)
	v.add_child(name_edit)
	desc_edit = LineEdit.new()
	desc_edit.placeholder_text = "descripción corta (opcional)"
	desc_edit.text_changed.connect(func(t: String) -> void:
		doc_desc = t
		doc_dirty = true)
	v.add_child(desc_edit)
	kind_opt = OptionButton.new()
	kind_opt.add_item("Estructura (tamaño de casa como máximo)")
	kind_opt.add_item("Zona (poblado, árbol gigante…)")
	kind_opt.item_selected.connect(func(i: int) -> void:
		doc_kind = i
		_clamp_size()
		_sync_doc_ui()
		doc_dirty = true)
	v.add_child(kind_opt)
	lim_label = _lbl("", 12, UI.DIM, 370.0)
	v.add_child(lim_label)
	v.add_child(_lbl("Tamaño del marco (bloques de 0,5 m): ancho X · alto Y · fondo Z", 13, Color(0.9, 0.95, 1.0), 370.0))
	var sr := HBoxContainer.new()
	for ax in range(3):
		var axi := ax
		var s := _spin(4, 512, doc_size[ax], func(x: float) -> void:
			var d := doc_size
			d[axi] = int(x)
			doc_size = d
			_clamp_size()
			_rebuild_floor()
			doc_dirty = true)
		size_spins.append(s)
		sr.add_child(s)
	v.add_child(sr)
	v.add_child(_btn("Tamaño máximo permitido", func() -> void:
		doc_size = _lim()
		_rebuild_floor()
		_sync_doc_ui()
		doc_dirty = true))
	v.add_child(_lbl("Entrada (celda local x, z) y hacia dónde mira la fachada:", 13, Color(0.9, 0.95, 1.0), 370.0))
	var er := HBoxContainer.new()
	for ax in range(2):
		var axi := ax
		var s := _spin(0, 511, doc_entry[ax], func(x: float) -> void:
			var e := doc_entry
			e[axi] = int(x)
			doc_entry = e
			doc_dirty = true)
		entry_spins.append(s)
		er.add_child(s)
	v.add_child(er)
	face_opt = OptionButton.new()
	for n in FACING_NAMES:
		face_opt.add_item(n)
	face_opt.item_selected.connect(func(i: int) -> void:
		doc_facing = i
		doc_dirty = true)
	v.add_child(face_opt)
	v.add_child(_btn("Entrada = celda que apunto", func() -> void:
		if hit.is_empty() or not hit.get("hit", false):
			_say("Apunta al suelo del marco")
			return
		var c: Vector3i = hit["adj"] if hit["cell"].y < FLAT_Y else hit["cell"]
		doc_entry = Vector2i(clampi(c.x, 0, doc_size.x - 1), clampi(c.z, 0, doc_size.z - 1))
		doc_dirty = true
		_sync_doc_ui()))
	doc_label = _lbl("", 12, UI.DIM, 370.0)
	v.add_child(doc_label)
	var sv := _btn("Guardar en el catálogo   [Ctrl+S]", func() -> void: save_doc())
	sv.add_theme_color_override("font_color", UI.GOOD)
	v.add_child(sv)
	v.add_child(_btn("Exportar este documento (zip en el Escritorio)", func() -> void: export_zip(false)))
	v.add_child(_btn("Exportar TODO el catálogo (zip en el Escritorio)", func() -> void: export_zip(true)))
	v.add_child(_btn("Abrir la carpeta del catálogo", func() -> void: OS.shell_open(catalog_dir())))
	v.add_child(_btn("Documento nuevo…", func() -> void: _ask("¿Empezar un documento nuevo? Se borra lo que hay en el marco (guarda antes en el catálogo).", func() -> void: new_doc())))
	v.add_child(_lbl("Todo lo que hagas se autoguarda; al guardar en el catálogo queda un .json (y una captura) que puedes enviarme. Lo que quede fuera del marco no se guarda.", 12, UI.DIM, 370.0))


func _clamp_size() -> void:
	var lim := _lim()
	doc_size = Vector3i(clampi(doc_size.x, 4, lim.x), clampi(doc_size.y, 4, lim.y), clampi(doc_size.z, 4, lim.z))
	doc_entry = Vector2i(clampi(doc_entry.x, 0, doc_size.x - 1), clampi(doc_entry.y, 0, doc_size.z - 1))


func _sync_doc_ui() -> void:
	if name_edit == null:
		return
	_clamp_size()
	var lim := _lim()
	name_edit.text = doc_name
	desc_edit.text = doc_desc
	kind_opt.select(doc_kind)
	face_opt.select(doc_facing)
	for i in range(3):
		size_spins[i].max_value = lim[i]
		size_spins[i].set_value_no_signal(doc_size[i])
	entry_spins[0].max_value = doc_size.x - 1
	entry_spins[1].max_value = doc_size.z - 1
	entry_spins[0].set_value_no_signal(doc_entry.x)
	entry_spins[1].set_value_no_signal(doc_entry.y)
	lim_label.text = "Límite de %s: %d x %d x %d bloques (%.0f x %.0f x %.0f m)." % [
		"zona" if doc_kind == 1 else "estructura", lim.x, lim.y, lim.z, lim.x * BS, lim.y * BS, lim.z * BS]
	doc_label.text = "Archivo: %s\nPegados desde otras creaciones: %d" % [_doc_path(), doc_stamps.size()]
	_rebuild_floor()


func _build_tab_creations() -> void:
	var o: VBoxContainer = tool_opts[T_STAMP]
	stamp_label = _lbl("", 13, Color(0.9, 0.95, 1.0), 370.0)
	o.add_child(stamp_label)
	o.add_child(_btn("Girar 90° (R)", func() -> void: stamp_rot = (stamp_rot + 1) % 4))
	var v := _tab("Casas")
	cr_filter = OptionButton.new()
	for t in ["Todas", "Estructuras", "Zonas"]:
		cr_filter.add_item(t)
	cr_filter.item_selected.connect(func(_i: int) -> void: _refresh_creations())
	v.add_child(cr_filter)
	cr_search = LineEdit.new()
	cr_search.placeholder_text = "Buscar por nombre…"
	cr_search.text_changed.connect(func(_t: String) -> void: _refresh_creations())
	v.add_child(cr_search)
	cr_list = ItemList.new()
	cr_list.custom_minimum_size = Vector2(0, 260)
	cr_list.item_selected.connect(func(i: int) -> void: _show_creation(i))
	cr_list.item_activated.connect(func(i: int) -> void: open_creation(String(cr_files[i])))
	v.add_child(cr_list)
	cr_thumb = TextureRect.new()
	cr_thumb.custom_minimum_size = Vector2(0, 150)
	cr_thumb.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	cr_thumb.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	v.add_child(cr_thumb)
	cr_info = _lbl("Elige una creación de la lista.", 12, Color(0.9, 0.95, 1.0), 370.0)
	v.add_child(cr_info)
	v.add_child(_btn("Estampar en el documento actual (herramienta −)", func() -> void:
		var i := cr_list.get_selected_items()
		if i.size() == 0:
			_say("Elige una creación de la lista")
			return
		stamp_from(String(cr_files[i[0]]))))
	v.add_child(_btn("Abrir para editar (reemplaza el documento actual)", func() -> void:
		var i := cr_list.get_selected_items()
		if i.size() == 0:
			_say("Elige una creación de la lista")
			return
		var p := String(cr_files[i[0]])
		_ask("¿Abrir «%s»? Se reemplaza lo que hay en el marco (guarda antes en el catálogo si lo necesitas)." % p.get_file(), func() -> void: open_creation(p))))
	v.add_child(_btn("Borrar del catálogo…", func() -> void:
		var i := cr_list.get_selected_items()
		if i.size() == 0:
			return
		var p := String(cr_files[i[0]])
		_ask("¿Borrar «%s» del catálogo?" % p.get_file(), func() -> void: delete_creation(p))))
	v.add_child(_btn("Importar un .json de creación…", func() -> void: file_dlg.popup_centered_ratio(0.6)))
	v.add_child(_btn("Actualizar lista", func() -> void: _refresh_creations()))
	v.add_child(_lbl("Estampar: elige la creación, ve al marco y haz clic donde quieras ponerla (R gira, flechas la mueven). Cabe en estructuras y en zonas.", 12, UI.DIM, 370.0))


func _build_tab_view() -> void:
	var v := _tab("Vista")
	stats_label = _lbl("", 13, Color(0.9, 0.95, 1.0), 370.0)
	v.add_child(stats_label)
	v.add_child(_btn("Cámara al centro del marco", func() -> void: _home_camera()))
	var sc := CheckBox.new()
	sc.text = "Mostrar colisiones invisibles (rojo)"
	sc.toggled.connect(func(on: bool) -> void:
		show_barriers = on
		barrier_mm.visible = on and active)
	v.add_child(sc)
	var sr := HBoxContainer.new()
	sr.add_child(_lbl("Velocidad de vuelo", 13))
	var ss := HSlider.new()
	ss.min_value = 2
	ss.max_value = 120
	ss.value = speed
	ss.custom_minimum_size = Vector2(120, 0)
	ss.value_changed.connect(func(x: float) -> void: speed = x)
	sr.add_child(ss)
	v.add_child(sr)
	var tr := HBoxContainer.new()
	tr.add_child(_lbl("Hora del día", 13))
	var ts := HSlider.new()
	ts.min_value = 0.0
	ts.max_value = 1.0
	ts.step = 0.005
	ts.value = main.time_of_day
	ts.custom_minimum_size = Vector2(120, 0)
	ts.value_changed.connect(func(x: float) -> void: main.time_of_day = x)
	tr.add_child(ts)
	v.add_child(tr)
	v.add_child(_btn("Salir del Taller", func() -> void:
		on_quit()
		get_tree().quit()))
	v.add_child(_lbl("Atajos: 1-9, 0, − herramientas · Tab mirar con el ratón · Clic der. mantenido girar · Rueda: tamaño/giro · G rejilla · V paso · Ctrl+Z / Ctrl+Y · Ctrl+S guardar", 12, UI.DIM, 370.0))


func _scan_creations() -> Array:
	var out: Array = []
	var q := cr_search.text.strip_edges().to_lower() if cr_search else ""
	var flt := cr_filter.selected if cr_filter else 0
	for k in range(2):
		if flt != 0 and flt - 1 != k:
			continue
		var dir := catalog_dir().path_join(KIND_DIRS[k])
		for fn in DirAccess.get_files_at(dir):
			if not fn.ends_with(".json"):
				continue
			if q != "" and q not in fn.to_lower():
				continue
			out.append(dir.path_join(fn))
	out.sort()
	return out


func _peek_size(path: String) -> String:
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		return "?"
	var head := f.get_buffer(900).get_string_from_utf8()
	var rx := RegEx.new()
	rx.compile("\"size\":\\[(\\d+),(\\d+),(\\d+)\\]")
	var m := rx.search(head)
	return "%sx%sx%s" % [m.get_string(1), m.get_string(2), m.get_string(3)] if m else "?"


func _refresh_creations() -> void:
	if cr_list == null:
		return
	cr_files = _scan_creations()
	cr_list.clear()
	for p in cr_files:
		var kind := "zona" if "/zonas/" in String(p).replace("\\", "/") else "estructura"
		cr_list.add_item("%s   ·   %s   ·   %s" % [String(p).get_file().get_basename(), kind, _peek_size(p)])


func _show_creation(i: int) -> void:
	var p := String(cr_files[i])
	var png := p.get_basename() + ".png"
	if FileAccess.file_exists(png):
		var img := Image.load_from_file(png)
		cr_thumb.texture = ImageTexture.create_from_image(img) if img else null
	else:
		cr_thumb.texture = null
	cr_info.text = "%s\n%s" % [p.get_file(), p]


func _read_creation(path: String) -> Dictionary:
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		return {}
	var d: Variant = JSON.parse_string(f.get_as_text())
	if d is Dictionary and String(d.get("format", "")) == "farlands-taller":
		return d
	return {}


func stamp_from(path: String) -> void:
	var d := _read_creation(path)
	if d.is_empty():
		_say("No se pudo leer esa creación")
		return
	stamp_doc = d
	stamp_path = path
	stamp_rot = 0
	cat_off = Vector3i.ZERO
	set_tool(T_STAMP)
	_say("Estampa lista: «%s». Clic en el marco para ponerla · R gira" % d.get("name", "?"))


func open_creation(path: String) -> void:
	_end_txn()
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		_say("No se pudo abrir")
		return
	var err := load_doc_text(f.get_as_text())
	if err != "":
		_say("No se pudo abrir: " + err, 8.0)
		return
	dirty_save = true
	save_t = 0.5
	_home_camera()
	_say("Abierto «%s»" % doc_name)


func delete_creation(path: String) -> void:
	DirAccess.remove_absolute(path)
	var png := path.get_basename() + ".png"
	if FileAccess.file_exists(png):
		DirAccess.remove_absolute(png)
	cr_thumb.texture = null
	_refresh_creations()
	_say("Borrado del catálogo")


func import_creation(path: String) -> void:
	var d := _read_creation(path)
	if d.is_empty():
		_say("Ese archivo no es una creación del Taller")
		return
	var k := maxi(0, KIND_KEYS.find(String(d.get("kind", "estructura"))))
	var dir := catalog_dir().path_join(KIND_DIRS[k])
	DirAccess.make_dir_recursive_absolute(dir)
	var slug := _slug(String(d.get("name", path.get_file().get_basename())))
	if slug == "":
		slug = "importada"
	var dst := dir.path_join(slug + ".json")
	DirAccess.copy_absolute(path, dst)
	var png := path.get_basename() + ".png"
	if FileAccess.file_exists(png):
		DirAccess.copy_absolute(png, dir.path_join(slug + ".png"))
	_refresh_creations()
	_say("Importada: %s" % dst)


# autoguardado del documento
func _save_now() -> void:
	if not dirty_save:
		return
	dirty_save = false
	doc_dirty = true
	var f := FileAccess.open("user://taller_autosave.json", FileAccess.WRITE)
	if f:
		f.store_string(build_doc_text())
