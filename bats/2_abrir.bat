@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
call "%~dp0config.bat"
title Farlands Taller - 2 abrir

rem Abre el Taller directamente desde el proyecto (sin exportar). El catalogo es la carpeta catalogo\ del repo.
if not exist "!PROYECTO!\project.godot" (
  echo No encuentro "!PROYECTO!\project.godot"
  goto :fin
)
call "%~dp0_godot.bat"
if not defined GODOT goto :fin
if not exist "!PROYECTO!\bin\farlands.windows.template_release.x86_64.dll" (
  echo Falta la DLL en "!PROYECTO!\bin". Usa 4_actualizar_dll.bat.
  goto :fin
)
if not exist "!SALIDA!" mkdir "!SALIDA!"
if not exist "!PROYECTO!\.godot" (
  echo Importando el proyecto ^(solo la primera vez^) ...
  "!GODOT!" --headless --path "!PROYECTO!" --import > "!SALIDA!\abrir_import_log.txt" 2>&1
)
echo Abriendo el Taller ... ^(no cierres esta ventana negra^)
"!GODOT!" --path "!PROYECTO!" > "!SALIDA!\taller_out.txt" 2>&1
echo Cerrado. Registro: salida\taller_out.txt

:fin
echo.
pause
endlocal
