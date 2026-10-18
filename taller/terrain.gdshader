shader_type spatial;
render_mode cull_back, diffuse_lambert, specular_disabled;
#include "res://fl_common.gdshaderinc"

// Color horneado en los vertices (luz, sombra de esquinas, cuevas) x tinte del dia, mas una lampara
// alrededor del jugador. UV.x = patron del material (piedra, tablas, tejas...); UV.y = 1 en hojas (viento).
// Presets (fl_q): 0 Clasico = igual que antes; 1 Suave = bandas de luz segun el sol, tonos calidos/frios,
// lineas de bloque y borde de luz; 2 Rico = ademas sombras reales del sol y viento en las hojas.
uniform vec3 tint = vec3(1.0);
uniform vec3 lamp_pos = vec3(0.0);
uniform float lamp = 0.0;
varying vec3 wpos;
varying vec3 wnrm;
varying float pat;
varying float leaf;

void vertex() {
	vec3 wp = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	leaf = step(0.5, UV.y);                       // v0.14: UV.y = 0 no es hoja; 1 + peso (0 pegado a tronco/suelo .. 1 libre)
	float lw = clamp(UV.y - 1.0, 0.0, 1.0);
	if (fl_q > 0.5 && leaf > 0.5 && lw > 0.0) {
		vec2 w = fl_wind(wp, fl_time);
		float flut = sin(wp.x * 2.9 + wp.z * 2.3 + fl_time * 2.7);
		VERTEX.x += (w.x * 0.05 + flut * 0.01) * lw;
		VERTEX.z += (w.y * 0.05 - flut * 0.008) * lw;
		VERTEX.y += sin(wp.x * 1.3 + wp.z * 1.1 + fl_time * 2.4) * 0.008 * lw;
		wp = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	}
	wpos = wp;
	wnrm = normalize((MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz);
	pat = UV.x;
}

float pattern(float id, vec3 p, vec3 n) {
	vec3 b = p / 0.5;
	vec2 q;
	bool top = abs(n.y) > 0.5;
	if (top) q = b.xz;
	else if (abs(n.x) > 0.5) q = vec2(b.z, b.y);
	else q = vec2(b.x, b.y);
	int k = int(id + 0.5);
	if (k == 1) {   // piedra: sillares chicos trabados con junta oscura
		vec2 s = q * 2.0;
		float row = floor(s.y);
		s.x += mod(row, 2.0) * 0.5;
		vec2 f = fract(s);
		float e = min(min(f.x, 1.0 - f.x), min(f.y, 1.0 - f.y));
		float t = 0.93 + 0.12 * fl_h21(floor(s));
		return e < 0.07 ? 0.78 : t;
	}
	if (k == 2) {   // tablas
		vec2 s = vec2(q.x, q.y * 4.0);
		float row = floor(s.y);
		float seg = floor((s.x + fl_h21(vec2(row, 3.0)) * 4.0) / 3.0);
		float f = fract(s.y);
		float t = 0.92 + 0.1 * fl_h21(vec2(row, seg));
		float grain = 0.97 + 0.03 * sin(s.x * 9.0 + row * 1.7);
		return (f < 0.1 ? 0.8 : t * grain);
	}
	if (k == 3) {   // tejas
		vec2 s = q * 4.0;
		float row = floor(s.y);
		s.x += mod(row, 2.0) * 0.5;
		vec2 f = fract(s);
		float t = 0.92 + 0.12 * fl_h21(floor(s));
		if (f.y < 0.16) return 0.76;
		if (f.x < 0.07) return 0.88;
		return t * (0.94 + f.y * 0.08);
	}
	if (k == 4) {   // revoque / adobe
		return 0.95 + 0.07 * fl_h21(floor(q * 8.0));
	}
	if (k == 5) {   // troncos
		float f = fract(q.y);
		float v = 0.92 + 0.12 * fl_h21(vec2(floor(q.x * 8.0), floor(q.y)));
		return (f < 0.08 || f > 0.92) ? 0.78 : v;
	}
	if (k == 6) {   // paja
		return 0.86 + 0.18 * fl_h21(vec2(floor(q.x * 8.0), floor(q.y * 2.0)));
	}
	if (k == 7) {   // sillares grandes
		vec2 s = vec2(q.x * 0.5, q.y);
		float row = floor(s.y);
		s.x += mod(row, 2.0) * 0.5;
		vec2 f = fract(s);
		float e = min(min(f.x, 1.0 - f.x) * 2.0, min(f.y, 1.0 - f.y));
		return e < 0.06 ? 0.72 : 0.94 + 0.1 * fl_h21(floor(s));
	}
	if (k == 9) {   // hojas (v0.14): hojitas suaves de 1/6 m, sin huecos oscuros; poco contraste para que no se sienta ruidoso
		vec2 s = q * 3.0;
		vec2 cell = floor(s);
		vec2 f = fract(s) - 0.5;
		float t = fl_h21(cell);
		float cl = fl_h21(floor(q * 0.9) + 7.0);
		float blob = 1.0 - smoothstep(0.15, 0.62, length(f));      // centro de la hojita mas claro
		float v = 0.90 + 0.09 * t + 0.05 * cl + 0.06 * blob;
		if (t > 0.9) v *= 1.06;
		return v;
	}
	if (k == 10) {   // v0.14: detalle sutil en superficies naturales planas (pasto, tierra, arena, nieve, roca)
		vec2 s = q * 4.0;                                           // celdas de 1/8 m
		float t = fl_h21(floor(s));
		float t2 = fl_h21(floor(q * 1.0) + 31.0);                   // mancha grande, un bloque
		float v = 0.955 + 0.06 * t + 0.03 * t2;
		if (!top) {                                                 // estratos en caras verticales
			v *= 0.97 + 0.04 * sin(q.y * 6.0 + t2 * 6.0);
		}
		return v;
	}
	if (k == 8) {   // hueso
		return 0.94 + 0.06 * sin((q.x + q.y) * 3.0);
	}
	return 1.0;
}

void fragment() {
	vec3 c = COLOR.rgb;
	float dist = length(wpos - CAMERA_POSITION_WORLD);
	vec3 n = normalize(wnrm);
	if (pat > 0.5) {
		float m = pattern(pat, wpos, n);
		c *= mix(1.0, m, clamp(1.0 - (dist - 25.0) / 60.0, 0.0, 1.0));
	} else if (COLOR.a > 0.5 && fl_q > 0.5) {   // v0.14: textura sutil en lo plano natural (desde Suave)
		float m = pattern(10.0, wpos, n);
		c *= mix(1.0, m, clamp(1.0 - (dist - 18.0) / 40.0, 0.0, 1.0));
	}
	float d = distance(wpos, lamp_pos);
	float k = lamp * clamp(1.0 - d / 14.0, 0.0, 1.0);
	float dark = 1.0 - clamp(max(max(c.r, c.g), c.b) * 2.2, 0.0, 1.0);
	c += vec3(1.0, 0.85, 0.6) * k * k * dark * 0.55;
	float glow_mask = 1.0 - COLOR.a;                  // alfa 0: faroles y fuego (brillan solos)
	vec3 lit_tint = mix(vec3(1.0), tint, COLOR.a);
	vec3 col = c * lit_tint;                           // resultado del preset Clasico
	if (fl_q < 0.5) {
		ALBEDO = vec3(0.0);
		EMISSION = col;
	} else {
		float band = fl_cel(dot(n, fl_sun_dir));
		if (leaf > 0.5) band = mix(band, max(band, 0.6), 0.85);   // v0.14: el follaje no se ve negro/azul por debajo
		float edge = pat > 0.5 ? 0.0 : fl_block_edge(wpos, n, dist);
		vec3 g = fl_grade(c, band, fl_day) * lit_tint;
		g *= 1.0 - edge * 0.10;
		float rim = pow(1.0 - clamp(dot(n, normalize(CAMERA_POSITION_WORLD - wpos)), 0.0, 1.0), 3.0);
		g += fl_sky_col * rim * 0.07 * fl_day * COLOR.a;
		g = mix(g, col, glow_mask);
		if (fl_q < 1.5) {
			ALBEDO = vec3(0.0);
			EMISSION = g;
		} else {
			// Rico: la luz del sol (con sombras reales) se calcula en light(); aqui va la base y lo que brilla
			ALBEDO = c * lit_tint * 0.85 * COLOR.a;
			// relleno que evita sombras negras + lo que brilla solo + lineas de bloque
			EMISSION = col * glow_mask * (fl_q > 2.5 ? 1.5 : 1.0) + c * lit_tint * (0.30 + 0.16 * step(0.5, leaf)) * COLOR.a * (1.0 - edge * 0.12);
		}
	}
}

void light() {
	if (fl_q > 1.5) {
		float band = fl_cel(dot(NORMAL, LIGHT));
		float sh = smoothstep(0.15, 0.6, ATTENUATION);
		DIFFUSE_LIGHT += LIGHT_COLOR * band * sh * 0.50 / 3.14159;
	}
}
