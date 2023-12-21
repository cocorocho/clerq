#!/bin/bash

cd /code

pip install -r requirements/base.txt

cd clerq

python manage.py migrate --no-input
python manage.py collectstatic --no-input

daphne -b 0.0.0.0 -p 8000 clerq.asgi:application
