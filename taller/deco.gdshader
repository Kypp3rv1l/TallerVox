shader_type spatial;
render_mode unshaded, cull_disabled;
#include "res://fl_common.gdshaderinc"

uniform vec3 tint = vec3(1.0);
uniform float time_s = 0.0;
varying vec3 wpos;
varying vec3 wnrm;

void vertex() {
	vec3 wp = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	// UV.y = peso de balanceo (0 en la raiz, 1 en la punta); solo plantas. Desde el preset Suave.
	float sw = UV.y;
	if (fl_q > 0.5 && sw > 0.001) {
		vec2 w = fl_wind(wp, fl_time);
		float bend = sw * sw;
		float flutter = sin(wp.x * 4.3 + wp.z * 3.7 + fl_time * 3.1) * 0.012 * sw;
		VERTEX.x += w.x * 0.075 * bend + flutter;
		VERTEX.z += w.y * 0.075 * bend - flutter * 0.7;
		VERTEX.y -= abs(w.x) * 0.012 * bend;   // al doblarse la punta baja un poco
		wp = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	}
	wpos = wp;
	wnrm = normalize((MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz);
}

void fragment() {
	vec3 col = COLOR.rgb * mix(vec3(1.0), tint, COLOR.a);   // alfa 0: faroles que brillan de noche
	if (fl_q > 0.5) {
		float band = fl_cel(dot(normalize(wnrm), fl_sun_dir));
		vec3 g = fl_grade(COLOR.rgb, band, fl_day) * mix(vec3(1.0), tint, COLOR.a);
		col = mix(col, g, COLOR.a);
	}
	ALBEDO = col;
}
