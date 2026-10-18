@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
call "%~dp0config.bat"
title Farlands Taller - 5 subir a git

rem Sube el Taller al repo TallerVox (REPO_URL de config.bat) con TU usuario de git. No agrega a nadie como coautor.
where git >nul 2>&1
if errorlevel 1 (
  echo Falta git en el PATH.
  goto :fin
)
set "VER=?"
for /f "tokens=2 delims==" %%a in ('findstr /b /c:"config/version=" "!PROYECTO!\project.godot"') do set "VER=%%~a"
set "VER=!VER:"=!"

pushd "!REPO!"
if not exist ".git" (
  echo Iniciando el repo local ...
  git init -b main
)
git remote get-url origin >nul 2>&1
if errorlevel 1 (
  git remote add origin "!REPO_URL!"
) else (
  git remote set-url origin "!REPO_URL!"
)
set "GN="
set "GE="
for /f "delims=" %%u in ('git config user.name') do set "GN=%%u"
for /f "delims=" %%u in ('git config user.email') do set "GE=%%u"
if not defined GN goto :sinusuario
if not defined GE goto :sinusuario
echo Repo: !REPO_URL!
echo Commit como: !GN! / !GE!
echo.
git add -A
git status --short
echo.
set "R="
set /p "R=Hacer commit y push de la v!VER!? (S/N): "
if /i not "!R!"=="S" goto :salir
set "MSG=Taller v!VER!"
set /p "MSG=Mensaje del commit [Taller v!VER!]: "
git commit -m "!MSG!"
git branch -M main
git push -u origin main
if errorlevel 1 (
  echo.
  echo El push fue rechazado ^(el repo remoto ya tenia contenido, por ejemplo un README^). Intento unir y subir otra vez ...
  git pull --rebase --allow-unrelated-histories origin main
  git push -u origin main
)
if errorlevel 1 (
  echo.
  echo No se pudo subir. Revisa tu sesion de GitHub o que el repo "!REPO_URL!" exista.
  goto :salir
)
echo.
echo Listo: subido a !REPO_URL!
goto :salir

:sinusuario
echo Git no tiene tu usuario configurado. Ejecuta una sola vez:
echo   git config --global user.name "Tu Nombre"
echo   git config --global user.email "tu@correo"

:salir
popd

:fin
echo.
pause
endlocal
