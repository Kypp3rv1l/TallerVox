shader_type spatial;
render_mode unshaded, cull_disabled, blend_mix, depth_draw_opaque;
#include "res://fl_common.gdshaderinc"

uniform vec3 tint = vec3(1.0);
uniform float time_s = 0.0;
varying vec3 wpos;

void vertex() {
	wpos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
}

void fragment() {
	// ondas de bloques: celdas de medio metro que cambian de tono despacio
	vec2 cell = floor(wpos.xz / 0.5);
	float n = sin(cell.x * 1.7 + cell.y * 2.3 + time_s * 0.9) * 0.5 + 0.5;
	vec3 c = COLOR.rgb * (0.93 + n * 0.1);
	float alpha = 0.78;
	if (fl_q > 0.5) {
		// reflejo del cielo segun el angulo, brillos del sol y olas mas lentas y amplias
		vec3 v = normalize(CAMERA_POSITION_WORLD - wpos);
		float fres = pow(1.0 - clamp(v.y, 0.0, 1.0), 3.0);
		c = mix(c, fl_sky_col * 1.1, fres * 0.55);
		vec2 big = floor(wpos.xz / 1.5);
		float swell = sin(big.x * 0.9 + big.y * 1.3 + time_s * 0.6) * 0.5 + 0.5;
		c *= 0.94 + swell * 0.08;
		float sp = fl_h21(cell + floor(time_s * 1.5));
		float sun_align = pow(clamp(dot(reflect(-fl_sun_dir, vec3(0.0, 1.0, 0.0)), -v), 0.0, 1.0), 6.0);
		float glint = step(0.93, sp) * (0.35 + 0.65 * sun_align) * fl_day;
		c += fl_sun_col * glint * 0.35;
		alpha = mix(0.78, 0.9, fres);
	}
	ALBEDO = c * tint;
	ALPHA = alpha;
}
