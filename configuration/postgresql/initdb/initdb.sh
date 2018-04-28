#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    create role lorawan with login password 'lorawan';
    create database test with owner lorawan;
    create extension pg_trgm;
EOSQL
