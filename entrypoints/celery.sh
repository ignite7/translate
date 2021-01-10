#!/bin/sh

set -o errexit
set -o nounset

celery -A api.tasks worker -l INFO
