extends Node
## Pruebas del Taller: godot --headless --path taller -- --selftest   (o con xvfb para las capturas: --shots)
var main: Node
var ok_n := 0
var bad_n := 0


func _chk(c: bool, what: String) -> void:
	if c:
		ok_n += 1
		print("PASS  ", what)
	else:
		bad_n += 1
		print("FAIL  ", what)


func _ready() -> void:
	await get_tree().create_timer(0.3).timeout
	var w: Node = main.world
	var t0 := Time.get_ticks_msec()
	while not main.ready_world and Time.get_ticks_msec() - t0 < 60000:
		await get_tree().process_frame
	_chk(main.ready_world, "el mundo plano carga")
	var ed: Node = main.editor
	_chk(w.is_solid_at(Vector3(6.0, 99.8, 6.0)), "suelo: sólido bajo y=200 bloques")
	_chk(not w.is_solid_at(Vector3(6.0, 100.3, 6.0)), "suelo: aire sobre y=200 bloques")
	_chk(not w.is_solid_at(Vector3(300.0, 100.3, -300.0)), "suelo plano también lejos")
	# --- construir algo
	ed.doc_kind = 0
	ed.doc_size = Vector3i(24, 48, 20)
	ed.doc_name = "prueba_casa"
	ed._begin_txn()
	w.edit_set_cubes(Vector3i(2, 200, 3), Vector3i(9, 205, 7), 9, 0, 0, 0)    # caja de piedra 8x6x5
	w.edit_set_cubes(Vector3i(3, 201, 4), Vector3i(8, 204, 6), 0, 0, 0, 0)    # hueco
	w.edit_add_fine(Vector3(1.0, 200.0, 1.0), Vector3(1.5, 202.0, 1.5), 200, 100, 50, 0, false)
	var pid: int = w.edit_place(121, Vector3(10, 200, 8), 0, 0, 0, false)
	ed._flush()
	ed._end_txn()
	var st: Dictionary = w.edits_stats()
	_chk(int(st["cubes"]) > 100, "ediciones: cubos en el mundo plano (%d)" % int(st["cubes"]))
	_chk(int(st["fine"]) == 1, "ediciones: 1 voxel fino")
	_chk(pid > 0, "ediciones: objeto del catálogo colocado")
	# --- archivo
	var text: String = ed.build_doc_text()
	var d: Variant = JSON.parse_string(text)
	_chk(d is Dictionary and d.get("format", "") == "farlands-taller", "archivo: formato farlands-taller")
	_chk(d is Dictionary and d["size"] == [24.0, 48.0, 20.0] or (d is Dictionary and d["size"] == [24, 48, 20]), "archivo: tamaño")
	_chk(int(d["counts"]["cubes"]) == int(st["cubes"]), "archivo: mismos cubos que el mundo")
	_chk(int(d["counts"]["dropped_outside_frame"]) == 0, "archivo: nada fuera del marco")
	# fuera del marco se descarta
	ed._begin_txn()
	w.edit_set_cubes(Vector3i(40, 200, 40), Vector3i(41, 201, 41), 9, 0, 0, 0)
	ed._flush()
	ed._end_txn()
	var d2: Variant = JSON.parse_string(ed.build_doc_text())
	_chk(int(d2["counts"]["dropped_outside_frame"]) >= 8, "archivo: lo de fuera del marco se descarta")
	# --- ida y vuelta
	w.clear_edits()
	_chk(int(w.edits_stats()["cubes"]) == 0, "clear_edits limpia")
	var err: String = ed.load_doc_text(text)
	_chk(err == "", "cargar el archivo: " + err)
	_chk(int(w.edits_stats()["cubes"]) == int(st["cubes"]), "ida y vuelta: mismos cubos")
	_chk(w.edit_block_at(2, 200, 3) == 9 and w.edit_block_at(5, 202, 5) == 0, "ida y vuelta: bloque y hueco")
	# --- estampar (giro 0 y 1) en un documento zona
	var sd: Dictionary = d
	ed.doc_kind = 1
	ed.doc_size = Vector3i(120, 80, 100)
	ed._clamp_size()
	ed._rebuild_floor()
	w.clear_edits()
	var n0: int = ed.stamp_apply(sd, Vector3i(50, 200, 40), 0)
	_chk(n0 > 100, "estampa giro 0: %d elementos" % n0)
	_chk(w.edit_block_at(52, 200, 43) == 9 and w.edit_block_at(55, 202, 45) == 0, "estampa giro 0: posiciones")
	w.clear_edits()
	var n1: int = ed.stamp_apply(sd, Vector3i(50, 200, 40), 1)
	_chk(n1 > 100, "estampa giro 1: %d elementos" % n1)
	# (x,z)->(D-1-z, x) con D=20: la celda local (2,3) -> (16,2); origen (50,200,40) => (66,200,42)
	_chk(w.edit_block_at(66, 200, 42) == 9, "estampa giro 1: la esquina gira (x,z)->(D-1-z,x)")
	_chk(w.edit_block_at(52, 200, 43) == 0, "estampa giro 1: lo de antes ya no está")
	w.clear_edits()
	var n3: int = ed.stamp_apply(sd, Vector3i(10, 200, 10), 3)
	_chk(n3 > 100, "estampa giro 3: %d elementos" % n3)
	w.clear_edits()
	var n2a: int = ed.stamp_apply(sd, Vector3i(10, 200, 10), 2)
	var s2: Dictionary = w.edits_stats()
	_chk(int(s2["placed"]) == 1 and int(s2["fine"]) == 1, "estampa giro 2: objeto y voxel fino")
	# --- catalogo en disco
	ed.doc_kind = 0
	ed.doc_size = Vector3i(24, 48, 20)
	ed.doc_name = "zz_prueba_taller"
	ed.load_doc_text(text)
	ed.doc_name = "zz_prueba_taller"
	ed.save_doc()
	await get_tree().create_timer(0.5).timeout
	var p: String = ed._doc_path()
	_chk(FileAccess.file_exists(p), "catálogo: archivo guardado en " + p)
	ed._refresh_creations()
	_chk(ed.cr_files.has(p), "catálogo: aparece en la lista")
	ed.delete_creation(p)
	_chk(not FileAccess.file_exists(p), "catálogo: borrar")
	print("TALLER SELFTEST: %d ok, %d fallos" % [ok_n, bad_n])
	if "--keep" not in OS.get_cmdline_user_args():
		get_tree().quit(1 if bad_n > 0 else 0)
