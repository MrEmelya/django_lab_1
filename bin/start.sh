#!/usr/bin/env bash
# Скрипт запуска для Render.com
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn news_portal.wsgi --log-file -
