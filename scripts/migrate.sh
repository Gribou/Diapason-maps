#!/bin/bash

set -e;

python manage.py wait_for_db

echo "Migrating database..."
python manage.py migrate

echo "Creating superuser if needed..."
python manage.py createsuperuser_custom \
    --username ${SU_USERNAME:-admin} \
    --password ${SU_PASSWORD:-*@dm1n*} \
    --email ${SU_EMAIL:-blank@email.fr} \
    --noinput --preserve

echo "Populating database with default data if needed..."
python manage.py populate

if [ "${UPDATE_AT_STARTUP}" == "yes" ]; then
  echo "Updating AZBA maps..."
  python manage.py download_azba
  echo "Updating data from last AIP..."
  python manage.py download_last_airac
fi
