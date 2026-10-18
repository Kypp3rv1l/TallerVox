extends Node
## Capturas de desarrollo: xvfb-run godot --rendering-driver opengl3 --path taller -- --shots=/ruta
var main: Node
var out := "/tmp/shots_t"


func _shot(name: String) -> void:
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("%s/%s.png" % [out, name])


func _ready() -> void:
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--shots="):
			out = a.substr(8)
	DirAccess.make_dir_recursive_absolute(out)
	var w: Node = main.world
	var ed: Node = main.editor
	var t0 := Time.get_ticks_msec()
	while not main.ready_world and Time.get_ticks_msec() - t0 < 60000:
		await get_tree().process_frame
	await get_tree().create_timer(1.5).timeout
	ed.doc_name = "casa_demo"
	ed._begin_txn()
	w.edit_set_cubes(Vector3i(3, 200, 3), Vector3i(20, 215, 14), 9, 0, 0, 0)
	w.edit_set_cubes(Vector3i(4, 200, 4), Vector3i(19, 214, 13), 0, 0, 0, 0)
	w.edit_set_cubes(Vector3i(11, 200, 3), Vector3i(12, 205, 3), 0, 0, 0, 0)
	w.edit_set_cubes(Vector3i(3, 216, 3), Vector3i(20, 216, 14), 7, 0, 0, 0)
	w.edit_place(121, Vector3(8, 200, 6), 0, 0, 0, false)
	ed._flush()
	ed._end_txn()
	await get_tree().create_timer(1.5).timeout
	ed._home_camera()
	await get_tree().create_timer(0.8).timeout
	await _shot("1_vista")
	# apuntando al suelo con el ratón capturado (centro de pantalla)
	ed.cam.global_position = Vector3(6.0, 112.0, 14.0)
	ed.yaw = 0.0
	ed.pitch = -0.7
	ed._set_captured(true)
	ed.set_tool(ed.T_BOX)
	await get_tree().create_timer(0.8).timeout
	await _shot("2_suelo")
	ed.tabs.current_tab = 3
	ed._set_captured(false)
	await get_tree().create_timer(0.3).timeout
	await _shot("3_panel_taller")
	ed.tabs.current_tab = 4
	await get_tree().create_timer(0.3).timeout
	await _shot("4_panel_creaciones")
	# zona con estampa
	var txt: String = ed.build_doc_text()
	var d: Dictionary = JSON.parse_string(txt)
	ed.doc_kind = 1
	ed.doc_size = Vector3i(160, 100, 140)
	ed.doc_name = "aldea_demo"
	ed._clamp_size()
	ed._rebuild_floor()
	ed.stamp_doc = d
	ed.stamp_path = "casa_demo.json"
	ed.stamp_rot = 1
	ed._home_camera()
	ed.cam.global_position = Vector3(40.0, 125.0, 90.0)
	ed.yaw = 0.0
	ed.pitch = -0.5
	ed.tabs.current_tab = 0
	ed._set_captured(true)
	ed.set_tool(ed.T_STAMP)
	await get_tree().create_timer(1.5).timeout
	await _shot("5_estampa")
	ed._stamp_click(1)
	await get_tree().create_timer(1.5).timeout
	await _shot("6_estampada")
	# seleccion de un mueble en una casa del juego
	var hp: String = ed.catalog_dir() + "/estructuras/casa_2_plantas_2.json"
	if FileAccess.file_exists(hp):
		w.clear_edits()
		ed.load_doc_text(FileAccess.get_file_as_string(hp))
		var hf: Array = ed._all_fines()
		var best: Dictionary = hf[0]
		for f in hf:
			if Vector3(f["mn"]).y < Vector3(best["mn"]).y + 0.1 and Vector3(f["mn"]).y > 200.0:
				best = f
		ed.set_tool(ed.T_SELECT)
		ed._group_set(ed._gr_cluster(int(best["id"])), [], false)
		var c: Vector3 = (Vector3(ed.sel["mn"]) + Vector3(ed.sel["mx"])) * 0.5
		ed.cam.global_position = (c + Vector3(0, 6, 9)) * ed.BS
		ed.yaw = 0.0
		ed.pitch = -0.5
		ed.tabs.current_tab = 0
		ed._set_captured(false)
		await get_tree().create_timer(1.5).timeout
		await _shot("7_seleccion")
	print("SHOTS LISTOS en ", out)
	get_tree().quit()
