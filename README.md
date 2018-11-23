# py_microSERVICES

This project is developed along the same principles as  https://github.com/bbcCorp/microSERVICES
It explores a simple event-driven microservice architecture using a Python3 stack with multiple databases and a messaging layer. 

Developed by: Bedabrata Chatterjee


**WARNING: This is an actively developed project so things may be broken.**


## Introduction
This application explores a simple service based architecture involving an extremely simple Customer Entity.  

We have a simple web application that is used to manage Customers. The application does not convern itself with the business of storing and retrieving entities, or enforcing any other functionalities like notification or data replication. Instead it relies on simple REST apis.

Customer API exposes simple CRUD APIs. APIs commiy changes to a data repository which is responsible for generating a stream of events. In this app, we will be working with two types of events - one for CRUD and other for notification. 

The CRUD events are designed to be self contained and can be used to propagate application state. Both before and after change information is contained in the same event message. We can use this for data replication.


There will be one or more services that will pick up the events and trigger the required actions. 

The idea is to have simple decoupled systems that is event driven. Each component is individually scalable.


Note: 
1. With this kind of design, the notification and data replication services are not closely coupled with online/CRUD operations. 
2. We can recover from some service disruption without any issues. We can also scale these processes and run multiple copies of the mail or data replication service if load is high. 

3. We are using a single partition for the data replication queue so message order is guaranteed. For larger systems, this may not work. You can use a combination of id and timestamp to determine what needs to be done. 

4. In these kind of architecture we gain scale but add complexity and data staleness. We are settling for eventual consistency of data with event based replication. 

### Components

The application has the following high-level components
* Python 3
* Kafka 

* Django and Django REST Framework 
* PostgreSQL as data repository

There is an alternate implementation using the following 
* Flask and flask_restful 
* MongoDB as data repository

* We use Docker containers to host the application.

## Application Setup

The `setup` folder has all the scripts required to build and start the production-like environment with all the infrastructure pieces. 

Use the `build.sh` script to build the docker images for application and `startup.sh` to bring up all the containers required to test the application. You can bring down the setup by running the script `shutdown.sh`

For development, you can use the scripts `dev-startup.sh` and `dev-shutdown.sh` to bring up and tear down the dependent components like databases and messaging server. 

For unit tests, you can use the scripts `test-startup.sh` and `test-shutdown.sh`