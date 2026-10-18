extends Node3D
## Farlands Taller: editor de estructuras y zonas, aparte del juego.
## Mundo plano vacio (nucleo C++ de Farlands con suelo plano) + el editor de bloques, voxeles finos y objetos.

const Look = preload("res://look.gd")
const TallerEditor := preload("res://editor.gd")
const VERSION := "0.1.3"
const GAME_VERSION := "taller-0.1.0"
const FLAT_Y := 200            # el suelo termina en el bloque 199: lo que se construye empieza en y = 200
const SEED := 7777

var world: VoxelWorld
var player: Node3D = Node3D.new()      # el editor lo usa como "cuerpo" de la camara
var env := Environment.new()
var sky_mat := ProceduralSkyMaterial.new()
var sun := DirectionalLight3D.new()
var mat_t := ShaderMaterial.new()
var mat_w := ShaderMaterial.new()
var mat_d := ShaderMaterial.new()
var editor: Node
var time_of_day := 0.5
var cfg := {"seed": SEED, "half": false, "sens": 1.0, "fov": 70.0, "view": 200.0, "look": 1, "ui_scale": 1.0}
var ready_world := false


func _ready() -> void:
	_load_cfg()
	_build_env()
	Look.setup(sun, env, int(cfg.get("look", 1)))
	mat_t.shader = load("res://terrain.gdshader")
	mat_w.shader = load("res://water.gdshader")
	mat_d.shader = load("res://deco.gdshader")
	world = VoxelWorld.new()
	add_child(world)
	world.set_materials(mat_t, mat_w, mat_d)
	add_child(player)
	world.setup_flat(SEED, FLAT_Y)
	world.set_deco_range(40.0)
	get_window().content_scale_factor = clampf(float(cfg.get("ui_scale", 1.0)), 0.6, 1.8)
	editor = TallerEditor.new()
	editor.main = self
	add_child(editor)
	editor.begin()
	_apply_view(editor.cam)
	_update_sky(Vector3.ZERO)
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--shots="):
			var sh: Node = load("res://dev_shots.gd").new()
			sh.set("main", self)
			add_child(sh)
		if a == "--thumbs":
			var th: Node = load("res://dev_thumbs.gd").new()
			th.set("main", self)
			add_child(th)
		if a == "--ejemplo":
			var ej: Node = load("res://dev_ejemplo.gd").new()
			ej.set("main", self)
			add_child(ej)
		if a == "--selftest":
			var st: Node = load("res://selftest.gd").new()
			st.set("main", self)
			add_child(st)


func _process(_delta: float) -> void:
	var p: Vector3 = editor.cam.global_position
	world.update(p)
	if not ready_world and world.is_area_ready(p, 20.0):
		ready_world = true
	_update_sky(p)
	mat_w.set_shader_parameter("time_s", Time.get_ticks_msec() / 1000.0)
	mat_t.set_shader_parameter("lamp_pos", p)


func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_CLOSE_REQUEST and editor:
		editor.on_quit()


func _apply_view(cam: Camera3D) -> void:
	var v := clampf(float(cfg["view"]), 100.0, 400.0)
	var r := clampi(ceili(0.95 * v / 32.0), 2, 6)
	var lv := 1
	while r * 32.0 * pow(2.0, lv - 1) < v and lv < 6:
		lv += 1
	world.set_view(lv, r)
	world.set_reach(v * 1.04)
	cam.far = v * 1.1 + 120.0
	env.fog_depth_begin = v * 0.57
	env.fog_depth_end = v


func _load_cfg() -> void:
	var p := "user://taller.cfg"
	if FileAccess.file_exists(p):
		var f := FileAccess.open(p, FileAccess.READ)
		var v: Variant = JSON.parse_string(f.get_as_text())
		if v is Dictionary:
			for k in v.keys():
				cfg[k] = v[k]
	cfg["seed"] = SEED


func save_cfg() -> void:
	var f := FileAccess.open("user://taller.cfg", FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(cfg))


func _build_env() -> void:
	var sky := Sky.new()
	sky_mat.sky_curve = 0.18
	sky_mat.sun_angle_max = 18.0
	sky.sky_material = sky_mat
	env.background_mode = Environment.BG_SKY
	env.sky = sky
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.6, 0.68, 0.85)
	env.ambient_light_energy = 0.8
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	env.fog_enabled = true
	env.fog_mode = Environment.FOG_MODE_DEPTH
	env.fog_depth_begin = 90.0
	env.fog_depth_curve = 1.3
	env.fog_density = 1.0
	env.fog_sky_affect = 0.0
	var we := WorldEnvironment.new()
	we.environment = env
	add_child(we)
	sun.rotation_degrees = Vector3(-55, 35, 0)
	sun.light_energy = 1.0
	sun.shadow_enabled = false
	add_child(sun)


func daylight() -> float:
	var elev := sin(TAU * (time_of_day - 0.25))
	return clampf((elev + 0.2) / 0.45, 0.0, 1.0)


func _update_sky(_p: Vector3) -> void:
	var day := daylight()
	var elev := sin(TAU * (time_of_day - 0.25))
	var dusk := clampf(1.0 - absf(elev) / 0.28, 0.0, 1.0) * (1.0 if elev > -0.25 else 0.0)
	var top := Color(0.02, 0.04, 0.12).lerp(Color(0.0, 0.40, 0.75), day)
	var hor := Color(0.05, 0.08, 0.18).lerp(Color(0.0, 0.55, 0.82), day).lerp(Color(0.95, 0.55, 0.35), dusk * 0.6)
	sky_mat.sky_top_color = top
	sky_mat.sky_horizon_color = hor
	sky_mat.ground_horizon_color = hor
	sky_mat.ground_bottom_color = hor.darkened(0.3)
	env.fog_light_color = hor.lerp(Color(1, 1, 1), 0.10 * day)
	var tint := Color(0.28, 0.32, 0.5).lerp(Color(1, 1, 1), day).lerp(Color(1.0, 0.82, 0.7), dusk * 0.4)
	var tv := Vector3(tint.r, tint.g, tint.b)
	mat_t.set_shader_parameter("tint", tv)
	mat_d.set_shader_parameter("tint", tv)
	mat_w.set_shader_parameter("tint", tv)
	mat_t.set_shader_parameter("lamp", 0.0)
	sun.rotation_degrees = Vector3(-rad_to_deg(asin(clampf(maxf(elev, 0.1), -1.0, 1.0))), 35.0 + time_of_day * 120.0, 0)
	sun.light_energy = lerpf(0.22, 0.72, day)
	var sun_col := Color(1.0, 0.97, 0.9).lerp(Color(1.0, 0.62, 0.38), dusk * 0.7).lerp(Color(0.5, 0.6, 0.95), 1.0 - day)
	sun.light_color = sun_col
	Look.update(sun.global_transform.basis.z.normalized(), sun_col, hor, day, Time.get_ticks_msec() / 1000.0)
	env.ambient_light_energy = lerpf(0.35, 0.66, day)
