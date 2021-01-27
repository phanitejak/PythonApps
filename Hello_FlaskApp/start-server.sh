#!/usr/bin/env bash
# start-server.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd app; python app.py createsuperuser --no-input)
fi
(cd app; gunicorn app.wsgi --user www-data --bind 0.0.0.0:5000 --workers 3) &
nginx -g "daemon off;"