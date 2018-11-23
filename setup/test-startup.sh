#!/bin/bash

sudo rm -rf ./test-data

# create the mapped directories used by docker the container volumes
mkdir -p ./test-data/postgres/db
mkdir -p ./test-data/postgres/logs
mkdir -p ./test-data/mongo/db
mkdir -p ./test-data/mongo/logs
mkdir -p ./test-data/api-customers/logs
mkdir -p ./test-data/service-replication/logs

docker-compose  -f test-docker-compose.yml up -d