
#!/bin/sh

set -o errexit
set -o nounset

celery flower -A api.tasks --port=5555 --basic_auth=${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}
