extends Node
## Genera las capturas (.png) que falten en el catálogo: xvfb-run godot --rendering-driver opengl3 --path taller -- --thumbs
var main: Node


func _ready() -> void:
	var ed: Node = main.editor
	var t0 := Time.get_ticks_msec()
	while not main.ready_world and Time.get_ticks_msec() - t0 < 60000:
		await get_tree().process_frame
	await get_tree().create_timer(1.0).timeout
	ed.grid_on = false
	var n := 0
	for k in ed.KIND_DIRS:
		var dir: String = ed.catalog_dir().path_join(k)
		for fn in DirAccess.get_files_at(dir):
			if not fn.ends_with(".json"):
				continue
			var png: String = dir.path_join(fn.get_basename() + ".png")
			if FileAccess.file_exists(png):
				continue
			ed.open_creation(dir.path_join(fn))
			await get_tree().create_timer(2.5).timeout
			var s: Vector3 = Vector3(ed.doc_size) * 0.5
			var c := Vector3(s.x, 200.0 + s.y * 0.45, s.z) * 0.5
			var r := maxf(s.x, maxf(s.y, s.z)) * 0.5
			var p := c + Vector3(-0.55, 0.45, 1.0).normalized() * (r * 2.1 + 4.0)
			ed.cam.global_position = p
			var d := c - p
			ed.yaw = atan2(-d.x, -d.z)
			ed.pitch = atan2(d.y, Vector2(d.x, d.z).length())
			await get_tree().create_timer(1.2).timeout
			await ed._capture_thumb(png)
			await get_tree().create_timer(0.3).timeout
			n += 1
			print("THUMB ", png)
	print("THUMBS LISTAS ", n)
	get_tree().quit()
