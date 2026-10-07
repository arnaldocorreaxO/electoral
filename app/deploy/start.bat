@echo off
set NAME=aminc
set DIRECTORY=%~dp0
for %%I in ("%DIRECTORY%..") do set DJANGODIR=%%~fI
set DJANGO_SETTINGS_MODULE=config.settings
set DJANGO_WSGI_MODULE=config.wsgi

echo Iniciando la aplicacion %NAME% con el usuario %USERNAME%

cd /d %DJANGODIR%
echo La ruta del proyecto es %DJANGODIR%

call %DJANGODIR%\..\env\Scripts\activate.bat

set DJANGO_SETTINGS_MODULE=%DJANGO_SETTINGS_MODULE%
set PYTHONPATH=%DJANGODIR%;%PYTHONPATH%

python manage.py runserver 0.0.0.0:8000