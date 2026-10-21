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
	w.clear_edits()   # el autoguardado de una sesion anterior no debe ensuciar las pruebas
	await get_tree().create_timer(1.0).timeout
	_chk(w.is_solid_at(Vector3(6.0, 99.8, 6.0)), "suelo: sólido bajo y=200 bloques")
	_chk(not w.is_solid_at(Vector3(6.0, 100.3, 6.0)), "suelo: aire sobre y=200 bloques")
	_chk(not w.is_solid_at(Vector3(300.0, 100.3, -300.0)), "suelo plano también lejos")
	# --- construir algo
	ed.doc_kind = 0
	ed.doc_size = Vector3i(24, 48, 20)
	ed.doc_name = "prueba_casa"
	w.clear_edits()
	ed._begin_txn()
	w.edit_set_cubes(Vector3i(2, 200, 3), Vector3i(9, 205, 7), 9, 0, 0, 0)    # caja de piedra 8x6x5
	w.edit_set_cubes(Vector3i(3, 201, 4), Vector3i(8, 204, 6), 0, 0, 0, 0)    # hueco
	w.edit_add_fine(Vector3(1.0, 200.0, 1.0), Vector3(1.5, 202.0, 1.5), 200, 100, 50, 0, false)
	var pid: int = w.edit_place(121, Vector3(10, 200, 8), 0, 0, 0, false)
	ed._flush()
	ed._end_txn()
	var st: Dictionary = w.edits_stats()
	_chk(int(st["cubes"]) > 100, "ediciones: cubos en el mundo plano (%d)" % int(st["cubes"]))
	_chk(int(st["fine"]) == 1, "ediciones: 1 voxel fino (%s)" % str(st))
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
	# --- seleccionar objetos (grupos de cajas pequenas)
	ed.doc_kind = 0
	ed.doc_size = Vector3i(24, 48, 20)
	w.clear_edits()
	ed._begin_txn()
	var b1: int = w.edit_add_fine(Vector3(2, 200, 2), Vector3(4, 200.5, 3), 200, 50, 50, 0, false)
	var b2: int = w.edit_add_fine(Vector3(2, 200.5, 2), Vector3(2.5, 201, 3), 100, 50, 50, 0, false)
	var b3: int = w.edit_add_fine(Vector3(3.5, 200.5, 2), Vector3(4, 201, 3), 100, 50, 50, 0, false)
	var c1: int = w.edit_add_fine(Vector3(10, 200, 10), Vector3(11, 200.5, 11), 90, 90, 200, 0, false)
	ed._flush()
	ed._end_txn()
	var cl: Array = ed._gr_cluster(b2)
	_chk(cl.size() == 3, "seleccionar: el objeto completo agrupa sus 3 cajas (%d)" % cl.size())
	_chk(ed._gr_cluster(c1).size() == 1, "seleccionar: el cofre aparte es otro objeto")
	ed.tool = ed.T_SELECT
	ed._group_set(cl, [], false)
	_chk(ed.sel.get("type", "") == "group" and Vector3(ed.sel["mn"]).is_equal_approx(Vector3(2, 200, 2)), "seleccionar: grupo con su caja envolvente")
	ed.step_i = 0
	ed._group_move(Vector3i(1, 0, 0))
	var after: Array = ed._all_fines()
	var minx := 999.0
	for f in after:
		if Vector3(f["mn"]).z < 5.0:
			minx = minf(minx, Vector3(f["mn"]).x)
	_chk(after.size() == 4 and is_equal_approx(minx, 3.0), "seleccionar: mover el grupo 1 bloque (x=%s)" % str(minx))
	ed.step_i = 2
	ed._group_move(Vector3i(0, 0, 1))
	var zmin := 999.0
	for f in ed._all_fines():
		if Vector3(f["mn"]).x < 8.0:
			zmin = minf(zmin, Vector3(f["mn"]).z)
	_chk(is_equal_approx(zmin, 2.125), "seleccionar: paso fino 1/8 (z=%s)" % str(zmin))
	var bb0: Vector3 = Vector3(ed.sel["mx"]) - Vector3(ed.sel["mn"])
	ed._group_rotate()
	var bb1: Vector3 = Vector3(ed.sel["mx"]) - Vector3(ed.sel["mn"])
	_chk(is_equal_approx(bb0.x, bb1.z) and is_equal_approx(bb0.z, bb1.x) and ed.sel["fines"].size() == 3, "seleccionar: girar intercambia ancho y fondo")
	ed._group_move(Vector3i(0, -1, 0))
	_chk(Vector3(ed.sel["mn"]).y >= 200.0, "seleccionar: no baja del suelo")
	var y0: float = Vector3(ed.sel["mn"]).y
	ed.step_i = 0
	ed._pad_move(KEY_PAGEUP)
	_chk(is_equal_approx(Vector3(ed.sel["mn"]).y, y0 + 1.0), "seleccionar: botón Subir sube 1 bloque")
	ed._pad_move(KEY_PAGEDOWN)
	_chk(is_equal_approx(Vector3(ed.sel["mn"]).y, y0), "seleccionar: botón Bajar baja 1 bloque")
	var g2: Dictionary = ed._gr_in_box(Vector3(0, 200, 0), Vector3(8, 205, 8))
	_chk(g2["fines"].size() == 3 and g2["placed"].is_empty(), "seleccionar: caja elige lo de dentro")
	ed._delete_sel()
	_chk(ed._all_fines().size() == 1, "seleccionar: borrar el grupo deja solo el cofre")
	w.edit_undo()
	_chk(ed._all_fines().size() == 4, "seleccionar: deshacer devuelve el grupo")
	ed.sel = {}
	ed.tool = ed.T_BLOCK
	_chk(ed._ray_flags() == 1, "rayo: bloques solos con la herramienta Bloque")
	ed.tool = ed.T_MOVE
	_chk((ed._ray_flags() & 12) == 12, "rayo: Mover ve cajas pequeñas y objetos")
	ed.tool = ed.T_BLOCK
	# --- caja fina
	w.clear_edits()
	ed.fine_color = Color8(180, 40, 40)
	ed.fb_action = 0
	ed.fb_hollow = false
	var nb: int = ed.fbox_apply(Vector3(2, 200, 2), Vector3(4.5, 202.125, 3.25))
	_chk(nb == 1 and ed._all_fines().size() == 1, "caja fina: rellena con una sola caja")
	var f0: Dictionary = ed._all_fines()[0]
	_chk(Vector3(f0["mx"]).is_equal_approx(Vector3(4.5, 202.125, 3.25)), "caja fina: medidas finas (1/8)")
	w.clear_edits()
	ed.fb_hollow = true
	ed.fb_wall = 8
	var parts: Array = ed._fbox_parts(Vector3(0, 200, 0), Vector3(6, 205, 5))
	var vol := 0.0
	for q in parts:
		var dq: Vector3 = Vector3(q[1]) - Vector3(q[0])
		vol += dq.x * dq.y * dq.z
	_chk(parts.size() == 6 and is_equal_approx(vol, 6.0 * 5.0 * 5.0 - 4.0 * 3.0 * 3.0), "caja fina: hueca = solo paredes (vol %s)" % str(vol))
	_chk(ed._fbox_parts(Vector3(0, 200, 0), Vector3(2, 205, 5)).size() == 1, "caja fina: muy delgada queda maciza")
	ed.fbox_apply(Vector3(0, 200, 0), Vector3(6, 205, 5))
	_chk(ed._all_fines().size() == 6, "caja fina: hueca crea 6 cajas")
	ed.fb_action = 1
	ed.fbox_apply(Vector3(0, 200, 0), Vector3(6, 205, 5))
	_chk(ed._all_fines().is_empty(), "caja fina: borrar quita las cajas de dentro")
	ed.fb_action = 0
	ed.fb_hollow = false
	w.clear_edits()
	# --- casa del juego: los muebles se agrupan por objeto
	var hp: String = ed.catalog_dir() + "/estructuras/cw_casa_2_plantas.json"
	if FileAccess.file_exists(hp):
		w.clear_edits()
		ed.load_doc_text(FileAccess.get_file_as_string(hp))
		var hf: Array = ed._all_fines()
		var seen := {}
		var sizes: Array = []
		for f in hf:
			if seen.has(int(f["id"])):
				continue
			var c2: Array = ed._gr_cluster(int(f["id"]))
			for q in c2:
				seen[int(q["id"])] = true
			sizes.append(c2.size())
		sizes.sort()
		print("INFO casa: %d cajas finas en %d objetos; mayores: %s" % [hf.size(), sizes.size(), str(sizes.slice(maxi(0, sizes.size() - 5)))])
		_chk(sizes.size() > 5 and sizes[sizes.size() - 1] < hf.size(), "casa real: las cajas finas se separan en varios objetos")
		w.clear_edits()
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
