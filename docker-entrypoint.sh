#!/bin/bash
set -e

echo "collectstatic"
poetry run Dshop/manage.py collectstatic --noinput
# Apply database migrations
echo "Apply database migrations"
poetry run Dshop/manage.py migrate

# force running in background but not as a daemon - disabled in supervisord.conf
supervisord &
# Start server
echo "Starting server"
WORKERS=${1:-4}

exec poetry run uwsgi --http-timeout 300 --http-socket :8000 --gevent 1000 --master --workers=$WORKERS --module wsgi_api --enable-threads --buffer-size=65535 -H /www/.venv/ --ignore-sigpipe --ignore-write-errors --disable-write-exception
