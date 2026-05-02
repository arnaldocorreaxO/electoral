#!/bin/bash

echo "Borrando base de datos actual"
sudo rm -r /home/tics/jair/factora/app/db/factora.sqlite3

echo "Restaurando base de datos nueva"
sudo cp /home/tics/jair/factora/app/deploy/data/factora.sqlite3 /home/tics/jair/factora/app/db/factora.sqlite3

sudo chmod 7777 /home/tics/jair/factora/app/db/factora.sqlite3

sudo supervisorctl restart heytest

echo "Terminado proceso"
