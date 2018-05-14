#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    create role loraserver with login password 'loraserver';
    create database loraserver_ns with owner loraserver;
EOSQL