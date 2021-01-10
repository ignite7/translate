#!/bin/sh

set -o errexit
set -o nounset

celery flower -A api.tasks --port=5555
