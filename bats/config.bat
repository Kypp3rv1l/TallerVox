@echo off
rem Rutas del Taller. El repo es la carpeta que contiene esta carpeta bats\.
for %%i in ("%~dp0..") do set "REPO=%%~fi"
set "PROYECTO=!REPO!\taller"
set "SALIDA=!REPO!\salida"
rem Repositorio de GitHub donde se sube el Taller
set "REPO_URL=https://github.com/Kypp3rv1l/TallerVox.git"
