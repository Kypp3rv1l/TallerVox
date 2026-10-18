// Farlands: funciones compartidas del sistema de graficos (v0.12.0).
// Parametros globales (los registra look.gd): fl_q = preset (0 Clasico, 1 Suave, 2 Rico),
// fl_sun_dir = direccion HACIA el sol, fl_sun_col = color de la luz, fl_sky_col = color del horizonte,
// fl_time = segundos, fl_day = 0 noche .. 1 dia.
global uniform float fl_q;
global uniform vec3 fl_sun_dir;
global uniform vec3 fl_sun_col;
global uniform vec3 fl_sky_col;
global uniform float fl_time;
global uniform float fl_day;

float fl_h21(vec2 c) {
	return fract(sin(dot(c, vec2(12.9898, 78.233))) * 43758.5453);
}

// escalon de luz: 3 bandas con borde suave (0 sombra, 0.5 media, 1 luz)
float fl_cel(float ndl) {
	float x = clamp(ndl * 0.5 + 0.5, 0.0, 1.0);
	float a = smoothstep(0.30, 0.36, x);
	float b = smoothstep(0.58, 0.64, x);
	return (a + b) * 0.5;
}

// lineas finas entre bloques de medio metro (solo cerca): da el aspecto de voxel dibujado
float fl_block_edge(vec3 p, vec3 n, float dist) {
	vec3 b = p / 0.5;
	vec2 q;
	if (abs(n.y) > 0.5) q = b.xz;
	else if (abs(n.x) > 0.5) q = b.zy;
	else q = b.xy;
	vec2 f = abs(fract(q + 0.5) - 0.5);
	float e = min(f.x, f.y);
	float w = 0.035 + dist * 0.0006;
	float line = 1.0 - smoothstep(0.0, w, e);
	return line * clamp(1.0 - (dist - 22.0) / 40.0, 0.0, 1.0);
}

// color de luz y sombra del sol sobre un color base (tonos calidos en la luz, frios en la sombra)
vec3 fl_grade(vec3 base, float band, float day) {
	vec3 warm = mix(vec3(1.0), fl_sun_col, 0.55);
	vec3 cool = vec3(0.80, 0.88, 1.06);
	vec3 shade = mix(cool, vec3(1.0), 1.0 - day);
	float k = mix(0.84, 1.06, band);
	return base * k * mix(shade, warm, band);
}

// viento: desplazamiento horizontal suave segun la posicion, con rafagas lentas que cruzan el mapa (v0.13)
float fl_gust(vec3 wp, float t) {
	return 0.75 + 0.45 * sin(wp.x * 0.045 + wp.z * 0.031 - t * 0.55) * sin(wp.z * 0.05 - wp.x * 0.02 + t * 0.31);
}
vec2 fl_wind(vec3 wp, float t) {
	float a = sin(wp.x * 0.35 + wp.z * 0.21 + t * 1.3);
	float b = sin(wp.x * 0.9 - wp.z * 0.7 + t * 2.1) * 0.5;
	vec2 w = vec2(a + b, cos(wp.z * 0.3 + t * 1.1) * 0.6);
	return w * fl_gust(wp, t);
}
