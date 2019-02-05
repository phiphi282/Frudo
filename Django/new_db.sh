#!/bin/bash

[[ -f db.sqlite3 ]] && rm db.sqlite3
[[ -d dcp/migrations ]] && rm -rf dcp/migrations
[[ -d dcp/__pycache__ ]] && rm -rf dcp/__pycache__
python3 manage.py makemigrations
python3 manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('${ADMIN_NAME:-admin}', '${ADMIN_MAIL:-admin@dcp.org}', '${ADMIN_PASSWORD:-hunter2}')" | python3 manage.py shell
