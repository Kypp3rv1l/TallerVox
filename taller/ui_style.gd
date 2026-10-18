extends RefCounted
## Estilo comun de las ventanas (arbol, equipo): fondo azul oscuro, bordes cian, botones planos.

const BG := Color(0.03, 0.06, 0.13, 0.96)
const PANEL := Color(0.05, 0.1, 0.2, 1.0)
const LINE := Color(0.18, 0.5, 0.78, 1.0)
const ACCENT := Color(0.35, 0.85, 1.0, 1.0)
const GOOD := Color(0.45, 1.0, 0.6, 1.0)
const DIM := Color(0.5, 0.58, 0.7, 1.0)


static func box(bg: Color, border: Color, bw := 1, r := 3) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = bg
	s.border_color = border
	s.set_border_width_all(bw)
	s.set_corner_radius_all(r)
	s.content_margin_left = 8
	s.content_margin_right = 8
	s.content_margin_top = 6
	s.content_margin_bottom = 6
	return s


static func panel(border := LINE) -> PanelContainer:
	var p := PanelContainer.new()
	p.add_theme_stylebox_override("panel", box(PANEL, border, 1, 4))
	return p


static func button(b: Button, accent := LINE) -> void:
	b.add_theme_stylebox_override("normal", box(PANEL, accent))
	b.add_theme_stylebox_override("hover", box(Color(0.1, 0.2, 0.36), ACCENT))
	b.add_theme_stylebox_override("pressed", box(Color(0.14, 0.3, 0.5), ACCENT))
	b.add_theme_stylebox_override("disabled", box(Color(0.04, 0.07, 0.13), Color(0.14, 0.2, 0.3)))
	b.add_theme_color_override("font_disabled_color", DIM)


# wrap > 0: el texto se parte en lineas de ese ancho (sin ancho, un Label con autowrap se encoge a 1 letra por linea)
static func label(text: String, size := 14, col := Color(0.9, 0.95, 1.0), wrap := 0.0) -> Label:
	var l := Label.new()
	l.text = text
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", col)
	if wrap > 0.0:
		l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		l.custom_minimum_size = Vector2(wrap, 0)
	return l


# tema para ventanas con muchos botones (menu): los hijos lo heredan
static func theme() -> Theme:
	var t := Theme.new()
	t.set_stylebox("normal", "Button", box(PANEL, LINE))
	t.set_stylebox("hover", "Button", box(Color(0.1, 0.2, 0.36), ACCENT))
	t.set_stylebox("pressed", "Button", box(Color(0.14, 0.3, 0.5), ACCENT))
	t.set_stylebox("disabled", "Button", box(Color(0.04, 0.07, 0.13), Color(0.14, 0.2, 0.3)))
	return t
