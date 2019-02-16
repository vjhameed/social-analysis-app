#!/bin/bash

set -e

python manage.py makemigrations

python manage.py migrate

# python manage.py create_users
# python manage.py create_profiles

python manage.py runserver_plus 0.0.0.0:80
#python manage.py runsslserver 0.0.0.0:80
