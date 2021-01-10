#!/bin/sh

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
celery -A api.tasks beat -l INFO -s api/data/celery/celerybeat-schedule.db
