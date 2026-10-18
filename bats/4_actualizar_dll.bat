@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
call "%~dp0config.bat"
title Farlands Taller - 4 actualizar la DLL

rem Copia la DLL del nucleo desde tu repo de Farlands (codigo\game\bin) al proyecto del Taller.
rem Uso: 4_actualizar_dll.bat "C:\ruta\a\Farlands"      (si no pasas la ruta, la pide)
set "FL=%~1"
if not defined FL set /p "FL=Ruta del repo de Farlands (la carpeta que contiene codigo\): "
set "FL=!FL:"=!"
set "SRC=!FL!\codigo\game\bin\farlands.windows.template_release.x86_64.dll"
if not exist "!SRC!" (
  echo No encuentro "!SRC!"
  goto :fin
)
if not exist "!PROYECTO!\bin" mkdir "!PROYECTO!\bin"
copy /y "!SRC!" "!PROYECTO!\bin\" >nul
echo Copiada la DLL a "!PROYECTO!\bin"

:fin
echo.
pause
endlocal
