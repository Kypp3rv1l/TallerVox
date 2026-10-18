extends RefCounted
# Sistema de graficos (v0.12.0): presets 0 Clasico, 1 Suave (cel-shading), 2 Rico (cel + sombras + viento).
# Los shaders leen parametros globales (fl_*) que se actualizan aqui; los personajes usan materiales toon
# con contorno que este script registra y cambia con el preset.

const NAMES := ["Clásico", "Suave", "Rico", "Ultra"]
const NOTES := [
	"Como antes: colores planos, sin sombras del sol.",
	"Luz por bandas según el sol, tonos cálidos y fríos, contorno en personajes. Casi sin coste.",
	"Todo lo de Suave más sombras reales del sol y viento en hojas y plantas. Pide más a la tarjeta gráfica.",
	"Todo lo de Rico más sombras en cascada hasta 180 m con bordes suaves, brillo (bloom) en faroles y fuego, tonos tipo cine, niebla con luz del sol y color más vivo. El más exigente.",
]
static var q := 1
static var _globals_ready := false
static var _mats: Array = []       # WeakRef de StandardMaterial3D de personajes
static var _outline: ShaderMaterial
static var sun: DirectionalLight3D
static var env: Environment


static func init_globals() -> void:
	if _globals_ready:
		return
	_globals_ready = true
	var defs := {
		"fl_q": [RenderingServer.GLOBAL_VAR_TYPE_FLOAT, 1.0],
		"fl_sun_dir": [RenderingServer.GLOBAL_VAR_TYPE_VEC3, Vector3(0.4, 0.8, 0.4)],
		"fl_sun_col": [RenderingServer.GLOBAL_VAR_TYPE_VEC3, Vector3(1.0, 0.95, 0.85)],
		"fl_sky_col": [RenderingServer.GLOBAL_VAR_TYPE_VEC3, Vector3(0.5, 0.7, 0.9)],
		"fl_time": [RenderingServer.GLOBAL_VAR_TYPE_FLOAT, 0.0],
		"fl_day": [RenderingServer.GLOBAL_VAR_TYPE_FLOAT, 1.0],
	}
	for k in defs.keys():
		RenderingServer.global_shader_parameter_add(k, defs[k][0], defs[k][1])


static func setup(sun_light: DirectionalLight3D, environment: Environment, quality: int) -> void:
	init_globals()
	sun = sun_light
	env = environment
	apply(quality)


static func apply(quality: int) -> void:
	q = clampi(quality, 0, 3)
	RenderingServer.global_shader_parameter_set("fl_q", float(q))
	if sun != null:
		sun.shadow_enabled = q >= 2
		if q >= 3:
			sun.directional_shadow_mode = DirectionalLight3D.SHADOW_PARALLEL_4_SPLITS
			sun.directional_shadow_max_distance = 180.0
			sun.directional_shadow_split_1 = 0.06
			sun.directional_shadow_split_2 = 0.18
			sun.directional_shadow_split_3 = 0.45
			sun.directional_shadow_blend_splits = true
			sun.shadow_bias = 0.05
			sun.shadow_normal_bias = 1.4
			sun.shadow_blur = 1.8
		else:
			sun.directional_shadow_mode = DirectionalLight3D.SHADOW_ORTHOGONAL
			sun.directional_shadow_max_distance = 70.0
			sun.shadow_bias = 0.06
			sun.shadow_normal_bias = 1.2
			sun.shadow_blur = 1.4
	if env != null:
		var u := q >= 3
		env.tonemap_mode = Environment.TONE_MAPPER_REINHARDT if u else Environment.TONE_MAPPER_LINEAR
		env.tonemap_exposure = 1.1 if u else 1.0
		env.tonemap_white = 2.2
		env.glow_enabled = u
		env.glow_intensity = 0.8
		env.glow_strength = 1.0
		env.glow_bloom = 0.15
		env.glow_hdr_threshold = 0.7
		env.glow_blend_mode = Environment.GLOW_BLEND_MODE_SOFTLIGHT
		env.adjustment_enabled = u
		env.adjustment_saturation = 0.92
		env.adjustment_contrast = 1.05
		env.fog_sun_scatter = 0.15 if u else 0.0
	var alive: Array = []
	for w in _mats:
		var m = (w as WeakRef).get_ref()
		if m != null:
			_style(m as StandardMaterial3D)
			alive.append(w)
	_mats = alive


# llamado cada cuadro desde main: direccion y color del sol, color del cielo, hora
static func update(sun_dir_to: Vector3, sun_col: Color, sky_col: Color, day: float, t: float) -> void:
	RenderingServer.global_shader_parameter_set("fl_sun_dir", sun_dir_to)
	RenderingServer.global_shader_parameter_set("fl_sun_col", Vector3(sun_col.r, sun_col.g, sun_col.b))
	RenderingServer.global_shader_parameter_set("fl_sky_col", Vector3(sky_col.r, sky_col.g, sky_col.b))
	RenderingServer.global_shader_parameter_set("fl_day", day)
	RenderingServer.global_shader_parameter_set("fl_time", t)


# material de un personaje/enemigo: se registra para cambiar de estilo con el preset
static func char_mat(m: StandardMaterial3D) -> StandardMaterial3D:
	_mats.append(weakref(m))
	_style(m)
	return m


static func _style(m: StandardMaterial3D) -> void:
	if q == 0:
		m.diffuse_mode = BaseMaterial3D.DIFFUSE_LAMBERT
		m.rim_enabled = false
		m.next_pass = null
	else:
		m.diffuse_mode = BaseMaterial3D.DIFFUSE_LAMBERT   # el toon de Godot satura las pieles claras: el estilo lo da el contorno
		m.rim_enabled = true
		m.rim = 0.25
		m.rim_tint = 0.5
		m.next_pass = _outline_mat()


static func _outline_mat() -> ShaderMaterial:
	if _outline == null:
		_outline = ShaderMaterial.new()
		_outline.shader = load("res://outline.gdshader")
	return _outline
