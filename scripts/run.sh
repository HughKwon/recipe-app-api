#!/bin/sh

# any command that fails will fail the whole script
set -e

python manage.py wait_for_db
# collect all static files and store them in collectstatic directory
python manage.py collectstatic --noinput
# make migrations if necessary
python manage.py migrate

# socket 9000 --> TCP socket on port 9000
# our NGINX server will use the TCP socket on port 9000 to connect to our app
# app.wsgi --> run app.app.wsgi.py
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi


