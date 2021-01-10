#!/bin/sh

set -o errexit
set -o nounset

export COMPOSE_FILE=dev.yml
docker-compose up -d
docker rm -f api
docker-compose run --rm --service-ports api
