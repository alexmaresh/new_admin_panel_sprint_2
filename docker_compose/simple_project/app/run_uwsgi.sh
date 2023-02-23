#!/usr/bin/env bash

export DJANGO_SUPERUSER_USERNAME=testname
export DJANGO_SUPERUSER_EMAIL=test@test.com
export DJANGO_SUPERUSER_PASSWORD=testpass1234
python manage.py createsuperuser --no-input || true

python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

python manage.py compilemessages -l en -l ru

set -e
chown www-data:www-data /var/log


uwsgi --strict --ini uwsgi.ini