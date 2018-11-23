#!/bin/bash

# create the mapped directories used by docker the container volumes
mkdir -p ./dev-data/postgres/db
mkdir -p ./dev-data/postgres/logs
mkdir -p ./dev-data/mongo/db
mkdir -p ./dev-data/mongo/logs
mkdir -p ./dev-data/api-customers/logs
mkdir -p ./dev-data/service-replication/logs

docker-compose  -f dev-docker-compose.yml up -d