#!/bin/bash

NAME="factora"
DIRECTORY=$(cd `dirname $0` && pwd)
DJANGODIR=`dirname $DIRECTORY`
DJANGO_SETTINGS_MODULE=config.settings
DJANGO_WSGI_MODULE=config.wsgi

echo "Iniciando la aplicación $NAME con el usuario `whoami`"

cd $DJANGODIR
echo "La ruta del proyecto es $DJANGODIR"

source ../env/bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

exec python manage.py runserver 0.0.0.0:9098
