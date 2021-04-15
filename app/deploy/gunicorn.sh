#!/bin/bash

NAME="factora"
DIRECTORY=$(cd `dirname $0` && pwd)
DJANGODIR=`dirname $DIRECTORY`
SOCKFILE=/tmp/gunicorn.sock
LOGDIR=${DJANGODIR}/logs/gunicorn.log
USER=jair
GROUP=jair
NUM_WORKERS=5
DJANGO_SETTINGS_MODULE=config.production
DJANGO_WSGI_MODULE=config.wsgi

rm -frv $SOCKFILE

echo "Iniciando la aplicación $NAME con el usuario `whoami`"

cd $DJANGODIR

exec /home/jair/factora/env/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=$LOGDIR
