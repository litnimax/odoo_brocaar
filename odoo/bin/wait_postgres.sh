#!/bin/bash
#
# Wait until postgresql is running.
#
set -e


dockerize -timeout 30s -wait tcp://${DB_HOST:-postgresql}:${DB_PORT:-5432}

# now the port is up but sometimes postgres is not totally ready yet:
# 'createdb: could not connect to database template1: FATAL:  the database system is starting up'
# we retry if we get this error

while [ "$(PGPASSWORD=${DB_PASSWORD:-loraserver_as} psql -h ${DB_HOST:-postgresql} -U ${DB_USER:-loraserver_as} -c '' postgres 2>&1)" = "psql: FATAL:  the database system is starting up" ]
do
  echo "Waiting for the database system to start up"
  sleep 0.1
done