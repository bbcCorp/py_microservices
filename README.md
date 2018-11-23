# py_microSERVICES

This project is developed along the same principles as  https://github.com/bbcCorp/microSERVICES
It explores microservices using a Python3 stack with multiple databases and a messaging layer. 

Developed by: Bedabrata Chatterjee


**WARNING: This is an actively developed project so things may be broken.**


## Introduction
This application explores a simple service based architecture involving an extremely simple Customer Entity.  


### Components

The application has the following high-level components
* Python 3
* Django and Django REST Framework 
* PostgreSQL as data repository

There is an alternate implementation using the following 
* Flask and flask_restful 
* MongoDB as data repository

* We use Docker containers to host the application.

## Application Setup

The `setup` folder has all the scripts required to build and start the production-like environment with all the infrastructure pieces. 

Use the `build.sh` script to build the docker images for application and `startup.sh` to bring up all the containers required to test the application. You can bring down the setup by running the script `shutdown.sh`