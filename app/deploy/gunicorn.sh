#!/bin/bash

NAME="electoral"
# La raíz de ejecución debe ser donde está manage.py
DJANGODIR="/home/acor/electoral/app"
# El entorno virtual está un nivel arriba de la app
VENV_PATH="/home/acor/electoral/.env/bin/activate"

SOCKFILE="/tmp/gunicorn.sock"
LOGDIR="/home/acor/electoral/logs/gunicorn.log"
USER="acor"
GROUP="acor"
NUM_WORKERS=5

# Verifica si es production.py o settings.py.
# Si no existe production.py, usa config.settings
DJANGO_SETTINGS_MODULE="config.production"
DJANGO_WSGI_MODULE="config.wsgi"

# Limpiar socket previo
rm -f $SOCKFILE

echo "Iniciando $NAME"
echo "Directorio de trabajo: $DJANGODIR"

# Entrar a la carpeta donde está manage.py
cd $DJANGODIR

# Activar el entorno virtual
if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
else
    echo "ERROR: Entorno virtual no encontrado en $VENV_PATH"
    exit 1
fi

# Exportar variables de entorno
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Crear carpeta de logs si no existe
mkdir -p /home/acor/electoral/logs

# Ejecutar Gunicorn
# Importante: el módulo es config.wsgi
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=$LOGDIR
