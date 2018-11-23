#!/bin/sh
## ---------------------------------------------------------------------------- ##
## Build Docker images
## ---------------------------------------------------------------------------- ##

RDATE=`date +%Y%m%d`
RVERSION=1.0.0
RENV=Release

# Remove old docker container images
# docker rm $(docker ps -a -q)
# docker rmi $(docker images -f "dangling=true" -q)

cd ./../src

## ----------------------- Build Customer Management WebApp --------------------------- ##
docker build -t py-microservices-api-customers:$RVERSION  -f api-customer.Dockerfile .
echo "[`date +%Y%m%d_%H:%M:%S`] Created Docker image py-microservices-api-customers:$RVERSION"


## ----------------------- Build Data Replication Service --------------------------- ##
docker build -t py-microservices-service-replication:$RVERSION -f service-replication.Dockerfile . 
echo "[`date +%Y%m%d_%H:%M:%S`] Created Docker image py-microservices-service-replication:$RVERSION"
