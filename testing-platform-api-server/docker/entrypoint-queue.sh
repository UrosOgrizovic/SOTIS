#!/bin/sh

set -e

celery -A src.config worker --loglevel=debug --pool=solo
