@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
call "%~dp0config.bat"
title Farlands Taller - 1 chequeo

rem Importa el proyecto y corre las pruebas automaticas del Taller (sin ventana). Resultado en salida\chequeo.txt
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
echo Importando ...
"!GODOT!" --headless --path "!PROYECTO!" --import > "!SALIDA!\chequeo.txt" 2>&1
echo Probando ...
"!GODOT!" --headless --path "!PROYECTO!" -- --selftest >> "!SALIDA!\chequeo.txt" 2>&1
echo.
powershell -NoProfile -Command "Get-Content '!SALIDA!\chequeo.txt' | Where-Object { $_ -match 'PASS|FAIL|SELFTEST|ERROR' } | Select-Object -Last 45"
echo.
echo Registro completo: salida\chequeo.txt

:fin
echo.
pause
endlocal
