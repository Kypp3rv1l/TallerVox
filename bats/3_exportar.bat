@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
call "%~dp0config.bat"
title Farlands Taller - 3 exportar el .exe

rem Exporta FarlandsTaller.exe con Godot y arma salida\FarlandsTaller_v<version>\ (+ zip) con:
rem   FarlandsTaller.exe, la DLL del nucleo y la carpeta catalogo\ (tus creaciones).
if not exist "!PROYECTO!\project.godot" (
  echo No encuentro "!PROYECTO!\project.godot"
  goto :fin
)
set "VER="
for /f "tokens=2 delims==" %%a in ('findstr /b /c:"config/version=" "!PROYECTO!\project.godot"') do set "VER=%%~a"
if not defined VER (
  echo No pude leer la version de project.godot
  goto :fin
)
set "VER=!VER:"=!"
echo Version: !VER!
if not exist "!PROYECTO!\bin\farlands.windows.template_release.x86_64.dll" (
  echo Falta la DLL en "!PROYECTO!\bin"
  goto :fin
)
call "%~dp0_godot.bat"
if not defined GODOT goto :fin
echo Godot: !GODOT!

if not exist "!SALIDA!" mkdir "!SALIDA!"
if not exist "!PROYECTO!\build" mkdir "!PROYECTO!\build"
if exist "!PROYECTO!\build\FarlandsTaller.exe" del /q "!PROYECTO!\build\FarlandsTaller.exe"

echo.
echo [1/2] Exportando FarlandsTaller.exe ...
"!GODOT!" --headless --path "!PROYECTO!" --import > "!SALIDA!\exportar_log.txt" 2>&1
"!GODOT!" --headless --path "!PROYECTO!" --export-release "Windows Desktop" "!PROYECTO!\build\FarlandsTaller.exe" >> "!SALIDA!\exportar_log.txt" 2>&1
if not exist "!PROYECTO!\build\FarlandsTaller.exe" (
  echo No se creo FarlandsTaller.exe. Ultimas lineas del registro ^(salida\exportar_log.txt^):
  echo ----------------------------------------
  powershell -NoProfile -Command "Get-Content -Tail 15 '!SALIDA!\exportar_log.txt'"
  echo ----------------------------------------
  echo Si dice que faltan las plantillas de exportacion: en Godot, Editor ^> Administrar plantillas de exportacion ^> Descargar e instalar.
  goto :fin
)

echo.
echo [2/2] Armando la carpeta y el zip ...
set "OUT=!SALIDA!\FarlandsTaller_v!VER!"
if exist "!OUT!" rmdir /s /q "!OUT!"
mkdir "!OUT!"
copy /y "!PROYECTO!\build\FarlandsTaller.exe" "!OUT!\" >nul
copy /y "!PROYECTO!\bin\farlands.windows.template_release.x86_64.dll" "!OUT!\" >nul
xcopy /e /i /y "!REPO!\catalogo" "!OUT!\catalogo" >nul
copy /y "!REPO!\README.md" "!OUT!\LEEME.md" >nul
set "ZIP=!SALIDA!\FarlandsTaller_v!VER!_Windows.zip"
if exist "!ZIP!" del /q "!ZIP!"
powershell -NoProfile -Command "Compress-Archive -Path '!OUT!\*' -DestinationPath '!ZIP!' -CompressionLevel Optimal"

echo.
echo Listo en "!SALIDA!":
echo   FarlandsTaller_v!VER!\FarlandsTaller.exe   ^(abrelo desde esa carpeta: necesita la DLL y catalogo\ al lado^)
echo   FarlandsTaller_v!VER!_Windows.zip

:fin
echo.
pause
endlocal
