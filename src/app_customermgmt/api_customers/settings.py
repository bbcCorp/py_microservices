
import os

message_topic = os.getenv('MICROSERVICES_KafkaService__Topic') or 'MICROSERVICE-CUSTOMER-UPDATES'
message_producer = {
    "bootstrap.servers" : os.getenv('MICROSERVICES_KafkaService__Servers') or "localhost:9092"
}