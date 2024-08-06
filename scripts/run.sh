#!/bin/sh

# any command that fails will fail the whole script
set -e

python manage.py wait_for_db
# collect all static files and store them in collectstatic directory
python mange.py collectstatic --noinput


