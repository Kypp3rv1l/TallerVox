rem Ayudante comun: deja en GODOT la ruta del .exe de Godot (la pide solo si falta) y la guarda en godot_ruta.bat.
if exist "%~dp0godot_ruta.bat" call "%~dp0godot_ruta.bat"
if defined GODOT set "GODOT=!GODOT:"=!"
if defined GODOT if not exist "!GODOT!" (
  echo La ruta guardada de Godot ya no existe: !GODOT!
  set "GODOT="
)
if not defined GODOT (
  set "NEW="
  set /p "NEW=Arrastra aqui el .exe de Godot 4.7.1 y presiona Enter: "
  if defined NEW set "GODOT=!NEW!"
)
if defined GODOT set "GODOT=!GODOT:"=!"
if defined GODOT if /i not "!GODOT:~-4!"==".exe" (
  echo Eso no es un .exe: "!GODOT!"
  echo Si usas Godot de Steam: clic derecho en Godot Engine ^> Administrar ^> Examinar archivos locales.
  set "GODOT="
)
if defined GODOT if not exist "!GODOT!" (
  echo No encuentro Godot en "!GODOT!"
  set "GODOT="
)
if defined GODOT > "%~dp0godot_ruta.bat" echo set "GODOT=!GODOT!"
