shader_type spatial;
render_mode unshaded, cull_front;

// Contorno de los personajes y enemigos (casco invertido). Las piezas son cajas centradas en su origen:
// agrandar cada vertice en su signo las infla parejo sin abrir las esquinas.
uniform vec4 line_color : source_color = vec4(0.05, 0.04, 0.08, 1.0);
uniform float width = 0.022;

void vertex() {
	VERTEX += sign(VERTEX) * width;
}

void fragment() {
	ALBEDO = line_color.rgb;
}
