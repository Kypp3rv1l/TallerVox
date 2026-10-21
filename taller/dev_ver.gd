extends Node
## Vistas de un .json: --ver=ARCHIVO --out=CARPETA  [--views=nombre:x,y,z,yawgrados,pitchgrados;...]
var main: Node
func _ready() -> void:
	var file := ""
	var out := "/tmp/ver"
	var views := ""
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--ver="): file = a.substr(6)
		if a.begins_with("--out="): out = a.substr(6)
		if a.begins_with("--views="): views = a.substr(8)
	DirAccess.make_dir_recursive_absolute(out)
	var ed: Node = main.editor
	var t0 := Time.get_ticks_msec()
	while not main.ready_world and Time.get_ticks_msec() - t0 < 60000:
		await get_tree().process_frame
	await get_tree().create_timer(1.0).timeout
	ed.grid_on = false
	var files := file.split(",")
	if views == "auto":
		for fn in files:
			ed.open_creation(fn)
			await get_tree().create_timer(2.5).timeout
			var sz: Vector3 = Vector3(ed.doc_size) * 0.5
			var c := Vector3(sz.x, 200.0 + sz.y * 0.45, sz.z) * 0.5
			var r := maxf(sz.x, maxf(sz.y, sz.z)) * 0.5
			var base := fn.get_file().get_basename()
			var k := 0
			for dir in [Vector3(-0.55, 0.45, 1.0), Vector3(0.55, 0.45, -1.0)]:
				var p: Vector3 = c + dir.normalized() * (r * 2.1 + 4.0)
				ed.cam.global_position = p
				var dd := c - p
				ed.yaw = atan2(-dd.x, -dd.z)
				ed.pitch = atan2(dd.y, Vector2(dd.x, dd.z).length())
				await get_tree().create_timer(1.3).timeout
				await RenderingServer.frame_post_draw
				await RenderingServer.frame_post_draw
				get_viewport().get_texture().get_image().save_png("%s/%s_%d.png" % [out, base, k])
				k += 1
		get_tree().quit()
		return
	ed.open_creation(file)
	await get_tree().create_timer(3.0).timeout
	for v in views.split(";"):
		var p := v.split(":")
		var n := p[0]
		var q := p[1].split(",")
		ed.cam.global_position = Vector3(float(q[0]), float(q[1]), float(q[2]))
		ed.yaw = deg_to_rad(float(q[3]))
		ed.pitch = deg_to_rad(float(q[4]))
		await get_tree().create_timer(1.5).timeout
		await RenderingServer.frame_post_draw
		await RenderingServer.frame_post_draw
		get_viewport().get_texture().get_image().save_png("%s/%s.png" % [out, n])
	get_tree().quit()
