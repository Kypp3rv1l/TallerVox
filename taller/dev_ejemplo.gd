extends Node
## Genera la creación de ejemplo del catálogo: xvfb-run godot --rendering-driver opengl3 --path taller -- --ejemplo
var main: Node


func _fill(w: Node, a: Vector3i, b: Vector3i, blk: int) -> void:
	w.edit_set_cubes(a + Vector3i(0, 200, 0), b + Vector3i(0, 200, 0), blk, 0, 0, 0)


func _ready() -> void:
	var w: Node = main.world
	var ed: Node = main.editor
	var t0 := Time.get_ticks_msec()
	while not main.ready_world and Time.get_ticks_msec() - t0 < 60000:
		await get_tree().process_frame
	await get_tree().create_timer(1.0).timeout
	ed.doc_kind = 0
	ed.doc_name = "ejemplo_caseta"
	ed.doc_desc = "Caseta de ejemplo: zócalo de piedra, muros de yeso, tejado a dos aguas, puerta al norte."
	ed.doc_size = Vector3i(16, 20, 14)
	ed.doc_entry = Vector2i(7, 0)
	ed.doc_facing = 0
	w.clear_edits()
	ed._begin_txn()
	_fill(w, Vector3i(1, 0, 1), Vector3i(14, 0, 12), 53)          # suelo de adoquín
	_fill(w, Vector3i(1, 1, 1), Vector3i(14, 2, 12), 53)          # zócalo
	_fill(w, Vector3i(1, 3, 1), Vector3i(14, 8, 12), 50)          # muros de yeso
	_fill(w, Vector3i(2, 1, 2), Vector3i(13, 8, 11), 0)           # interior hueco
	_fill(w, Vector3i(7, 1, 1), Vector3i(8, 4, 1), 0)             # puerta (hueco)
	_fill(w, Vector3i(3, 5, 1), Vector3i(4, 6, 1), 0)             # ventanas
	_fill(w, Vector3i(11, 5, 1), Vector3i(12, 6, 1), 0)
	_fill(w, Vector3i(1, 5, 6), Vector3i(1, 6, 7), 0)
	_fill(w, Vector3i(14, 5, 6), Vector3i(14, 6, 7), 0)
	# tejado a dos aguas (escalones de 1 bloque, cresta a lo largo de X)
	for i in range(6):
		_fill(w, Vector3i(0, 9 + i, i), Vector3i(15, 9 + i, 13 - i), 55)
		if i > 0:
			_fill(w, Vector3i(1, 9 + i, i + 1), Vector3i(14, 9 + i, 12 - i), 0)
	_fill(w, Vector3i(1, 9, 1), Vector3i(14, 9, 12), 28)          # viga de remate bajo el tejado
	_fill(w, Vector3i(2, 9, 2), Vector3i(13, 9, 11), 0)
	ed._flush()
	ed._end_txn()
	w.edit_begin()
	w.edit_place(121, Vector3(5, 201, 6), 0, 0, 0, false)
	w.edit_add_fine(Vector3(6.5, 201.0, 2.0), Vector3(7.0, 203.0, 2.25), 170, 120, 60, 0, false)
	ed._flush()
	w.edit_commit()
	await get_tree().create_timer(1.5).timeout
	ed.cam.global_position = Vector3(2.0, 105.2, -7.5)
	ed.yaw = PI + 0.35
	ed.pitch = -0.28
	ed._sync_doc_ui()
	ed.save_doc()
	await get_tree().create_timer(3.0).timeout
	print("EJEMPLO LISTO: ", ed._doc_path())
	get_tree().quit()
