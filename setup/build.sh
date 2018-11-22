#!/bin/sh
## ---------------------------------------------------------------------------- ##
## Build Docker images
## ---------------------------------------------------------------------------- ##

RDATE=`date +%Y%m%d`
RVERSION=1.0.0
RENV=Release

# Remove old docker container images
docker rm $(docker ps -a -q)
docker rmi $(docker images -f "dangling=true" -q)

cd ./../src/app_customermgmt

docker build -t py-microservices-api-customers:$RVERSION .