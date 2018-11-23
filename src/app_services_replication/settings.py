import os
import logging

MESSAGE_TOPIC = os.getenv('MICROSERVICES_KafkaService__Topic') or 'MICROSERVICE-CUSTOMER-UPDATES'

KafkaService = {
    "bootstrap.servers": os.getenv('MICROSERVICES_KafkaService__Servers') or "localhost:9092",
    "auto.commit.interval.ms": 5000,
    "auto.offset.reset": "earliest",
    "group.id": os.getenv('MICROSERVICES_NotificationService_ID') or "consumer-update-group-1"    
} 

Logging = {
    "LogFolder" : os.getenv('MICROSERVICES_Logging__LogFolder') or './../../setup/dev-data/services-replication/logs',
    "LogFile"   : os.getenv('MICROSERVICES_Logging__LogFile') or 'message_processor_1.log',
    "LogLevel" : os.getenv('MICROSERVICES_Logging__LogLevel') or logging.DEBUG,
}

MongoDB={
    "Url" : os.getenv('MICROSERVICES_MongoDB__Url') or "mongodb://root:pwd123@localhost",
    "Port": int( os.getenv('MICROSERVICES_MongoDB__Port') or 27017),
    "Db"  : os.getenv('MICROSERVICES_MongoDB__Db') or "py_microservices_api_customer",
    "Collection"  : os.getenv('MICROSERVICES_MongoDB__Collection') or "customers"
}