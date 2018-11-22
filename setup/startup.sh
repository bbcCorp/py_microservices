#!/bin/bash

# create the mapped directories used by docker the container volumes
mkdir -p ./data/postgres/db
mkdir -p ./data/postgres/logs
mkdir -p ./data/mongo/db
mkdir -p ./data/mongo/logs
mkdir -p ./data/api-customers/logs

docker-compose up -d